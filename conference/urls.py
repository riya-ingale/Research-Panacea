from django.urls import path
from . import views

urlpatterns = [
    path('upcoming_conf',views.upcoming_conf),
    path('registeration',views.registeration),
    path('upcoming_event',views.upcoming_event),
    path('event_details/<event_id>', views.event_details),
    path('conf_details/<conf_id>',views.conference_details),
    path('journals',views.journals),
    # path('journal-details/<j_id>',views.journal_details)
    path('calender/', views.calender)
]