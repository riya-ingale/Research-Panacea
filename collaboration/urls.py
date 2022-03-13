from unicodedata import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.collabfeed,name = "collabfeed"),
    path('postcollab/', views.postcollab, name = "postcollab"),

    path('viewcollaborations/',views.viewcollaborations, name = 'viewcollaborations'),
    path('viewcollab/<cid>', views.viewcollab, name='viewcollab'),
    path('postproposal/<collab_id>', views.postproposal, name = 'postproposal'),
    path('chat/', views.chat,name= 'chat'),
    path('viewproposals/',views.viewproposals, name = 'viewproposals'),
    path('viewcoverletter/<pid>',views.viewcoverletter, name = 'viewcoverletter')
]