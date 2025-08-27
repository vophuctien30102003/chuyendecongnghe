from django.urls import path, re_path, register_converter
from polls.views import home, about
from polls.models import LogMessage
from polls import converters

register_converter(converters.YearConverter, 'yyyy')

home_list_view = home.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  
    context_object_name="message_list",
    template_name="polls/home.html",
)

app_name = 'polls'
urlpatterns = [
    path("", home_list_view, name="home"),
    path("messages/", home_list_view, name="message_list"),
    path("about/", about.AboutView.as_view(), name="about"),
    path("log/", home.log_message, name="log"),
    path("now/", home.current_datetime, name="current_datetime"),
    path("archive/<yyyy:year>/", home.yearly_archive, name="yearly_archive"),
    path("archive/<yyyy:year>/<int:month>/", home.monthly_archive, name="monthly_archive"),
    re_path(r'^api/messages/(?P<year>[0-9]{4})/$', home.api_yearly_messages, name="api_yearly_messages"),
]