from tkinter import CASCADE
from django.db import models
from users.models import *

# Create your models here.
class CollaborationRequests(models.Model):
    user = models.IntegerField(null=True)#pk of Users
    title = models.CharField(max_length=500)
    description = models.TextField()
    domain = models.CharField(max_length=500, null=True)
    skills = models.CharField(max_length=500, null=True)
    pref_workplace = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=500, null=True)
    country = models.CharField(max_length=500, null=True)
    deadline = models.DateField(null=True)
    organisation = models.CharField(max_length=500, null=True)
    media = models.FileField(upload_to='users_media/collabfiles', null=True)
    duration = models.CharField(max_length=500, null=True)
    work_type = models.CharField(max_length=500, null=True) #Part time or Full time
    created_at = models.DateTimeField(auto_now_add=True)

class Proposals(models.Model):
    user = models.IntegerField(null=True) #pk of Users
    collabrequest = models.IntegerField(null=True) #pk of CollaborationRequests 
    cover_letter = models.TextField()
    media = models.FileField(upload_to='users_media/proposalfiles',null=True)
    created_at = models.DateTimeField(auto_now_add=True)

