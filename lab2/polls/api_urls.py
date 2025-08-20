from django.urls import path
from . import views

urlpatterns = [
    path("people/search", views.people_search, name="people_search"),
    path("people/active", views.active_people, name="active_people"),
    path("people/no-group", views.people_no_group, name="people_no_group"),
    path("people/by-year", views.people_by_year, name="people_by_year"),
    path("people/last-regex", views.people_lastname_regex, name="people_lastname_regex"),
    path("groups/top", views.groups_top, name="groups_top"),
]
