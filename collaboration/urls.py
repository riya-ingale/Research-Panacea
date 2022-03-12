from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.collabfeed,name = "collabfeed"),
    path('postcollab/', views.postcollab, name = "postcollab"),

    path('viewcollaborations/',views.viewcollaborations, name = 'viewcollaborations'),
    path('viewcollab/<cid>', views.viewcollab, name='viewcollab'),
    path('postproposal/<collab_id>', views.postproposal, name = 'postproposal'),
    path('chat/', views.chat,name= 'chat')
]