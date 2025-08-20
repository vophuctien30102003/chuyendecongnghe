from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Count
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Person, Group


def _person_dict(p: Person):
	return {
		"id": p.id,
		"first_name": p.first_name,
		"last_name": p.last_name,
		"status": p.status,
		"slug": p.slug,
	}


@require_GET
def people_search(request):
	term = request.GET.get("q", "")
	qs = Person.objects.search(term).order_by("last_name").select_related()
	return JsonResponse({"results": [_person_dict(p) for p in qs[:50]]})


@require_GET
def groups_top(request):
	qs = Group.objects.top_by_member_count(limit=10)
	return JsonResponse({"groups": [{"name": g.name, "slug": g.slug, "members": g.n} for g in qs]})


@require_GET
def active_people(request):
	qs = Person.objects.active().prefetch_related("groups")
	return JsonResponse({"active": [_person_dict(p) for p in qs[:50]]})


@require_GET
def people_no_group(request):
	qs = Person.objects.without_groups().order_by("last_name")
	return JsonResponse({"results": [_person_dict(p) for p in qs[:50]]})


@require_GET
def people_by_year(request):
	"""Example: filter people created in a given year using the __year lookup.
	GET /api/people/by-year?year=2025
	"""
	year_param = request.GET.get("year")
	if not year_param:
		return JsonResponse({"error": "Missing year param"}, status=400)
	try:
		year = int(year_param)
	except ValueError:
		return JsonResponse({"error": "Year must be integer"}, status=400)
	start = timezone.datetime(year, 1, 1, tzinfo=timezone.get_current_timezone())
	qs = Person.objects.filter(created_at__year=year).order_by("id")
	return JsonResponse({
		"year": year,
		"count": qs.count(),
		"results": [_person_dict(p) for p in qs[:50]],
		"from": start.isoformat(),
	})


@require_GET
def people_lastname_regex(request):
	"""Example: regex lookup on last_name.
	GET /api/people/last-regex?pattern=^Ti(en|ền)$
	"""
	pattern = request.GET.get("pattern")
	if not pattern:
		return JsonResponse({"error": "Missing pattern param"}, status=400)
	try:
		qs = Person.objects.filter(last_name__regex=pattern)[:50]
	except Exception:
		return JsonResponse({"error": "Invalid regex pattern"}, status=400)
	return JsonResponse({
		"pattern": pattern,
		"results": [_person_dict(p) for p in qs],
	})
