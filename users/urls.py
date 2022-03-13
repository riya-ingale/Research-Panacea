from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name = "home"),
    path('login/',views.login, name = "login"),
    path('logout/', views.logout, name = 'logout'),
    path('feed/',views.dashboardfeed, name = 'feed'),
    path('register/',views.register, name='register'),
    path('userprofile/',views.userprofile, name = 'userprofile'),
    path('otherprofile/<uid>',views.otherprofile, name = 'otherprofile'),
    path('researchpapers/',views.researchpapers, name = "researchpapers"),
    path('addworkexp/', views.addworkexp,name = 'addworkexp'),
    path('addeducation/',views.addeducation, name = "addeducation"),
    path('addcertification/', views.addcertification, name= 'addcertification'),
    path('addresearchpaper/',views.addresearchpaper, name = 'addresearchpaper'),
    path('viewresearchpaper/<rid>',views.viewresearchpaper, name = "viewresearchpaper"),
    path('saverspaper<rid>',views.saverspaper, name = "saverspaper"),
    path('editprofile/',views.editprofile, name = "editprofile")
]
