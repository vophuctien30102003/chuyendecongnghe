from django.utils.timezone import datetime
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.urls import reverse
from django.utils import timezone
import json

from polls.forms import LogMessageForm
from polls.models import LogMessage

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage
    template_name = 'polls/home.html'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_messages'] = LogMessage.objects.count()
        context['recent_messages'] = LogMessage.objects.order_by('-log_date')[:3]
        
        now = timezone.now()
        context['current_year'] = now.year
        context['current_month'] = now.month
        
        return context

def about(request):
    """About page view."""
    return render(request, "polls/about.html", {
        'title': 'About Our Application',
        'description': 'This is a Django application demonstrating views, templates, URLs, and forms.'
    })

@require_http_methods(["GET", "POST"])
def log_message(request):
    """Handle both GET and POST for logging messages."""
    if request.method == "POST":
        form = LogMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            messages.success(request, 'Your message has been logged successfully!')
            return redirect("polls:home")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LogMessageForm()
    
    # Thêm recent messages để hiển thị trong template
    recent_messages = LogMessage.objects.order_by('-log_date')[:3]
    
    return render(request, "polls/log_message.html", {
        "form": form,
        "recent_messages": recent_messages
    })

@cache_page(60 * 15)  # Cache for 15 minutes
def current_datetime(request):
    """Return current datetime as HTML."""
    now = datetime.now()
    html = '''
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Current Time</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            .time { font-size: 2em; color: #333; }
        </style>
    </head>
    <body>
        <h1>Current Date and Time</h1>
        <p class="time">%s</p>
        <a href="%s">Back to Home</a>
    </body>
    </html>
    ''' % (now.strftime('%A, %B %d, %Y at %I:%M:%S %p'), reverse('polls:home'))
    return HttpResponse(html)

def message_list(request):
    """Display paginated list of all messages."""
    messages_queryset = LogMessage.objects.order_by('-log_date')
    paginator = Paginator(messages_queryset, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'polls/message_list.html', {
        'page_obj': page_obj,
        'total_count': messages_queryset.count()
    })

def yearly_archive(request, year):
    """Display messages from a specific year."""
    messages_for_year = LogMessage.objects.filter(
        log_date__year=year
    ).order_by('-log_date')
    
    if not messages_for_year.exists():
        raise Http404(f"No messages found for year {year}")
    
    return render(request, 'polls/yearly_archive.html', {
        'year': year,
        'messages': messages_for_year,
        'count': messages_for_year.count()
    })

def monthly_archive(request, year, month):
    """Display messages from a specific month and year."""
    messages_for_month = LogMessage.objects.filter(
        log_date__year=year,
        log_date__month=month
    ).order_by('-log_date')
    
    if not messages_for_month.exists():
        raise Http404(f"No messages found for {month}/{year}")
    
    month_names = [
        '', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    return render(request, 'polls/monthly_archive.html', {
        'year': year,
        'month': month,
        'month_name': month_names[month],
        'messages': messages_for_month,
        'count': messages_for_month.count()
    })

def api_yearly_messages(request, year):
    """API endpoint returning JSON data for messages in a year."""
    messages_for_year = LogMessage.objects.filter(
        log_date__year=year
    ).order_by('-log_date')
    
    data = {
        'year': year,
        'count': messages_for_year.count(),
        'messages': [
            {
                'id': msg.id,
                'message': msg.message,
                'log_date': msg.log_date.isoformat(),
            }
            for msg in messages_for_year
        ]
    }
    
    return JsonResponse(data)
