from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import tile
from collaboration.models import CollaborationRequests, Proposals
from users.models import *
import os
import json

# Create your views here.

def collabfeed(request):
    if 'username' in request.session:
        user = Users.objects.filter(username = request.session['username'])
        if request.method == "GET":
            collabrequests = CollaborationRequests.objects.all()
    return HttpResponse("COLLAB FEED, WHERE ALL THE COLLABORATION REQUESTS WILL BE LISTED")


def postcollab(request):
    if 'username' in request.session:
        user = Users.objects.filter(username = request.session['username'])[0]
        print(user.username)
        if request.method == "GET":
            return render(request, 'postcollab.html')
        elif request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            domain = request.POST.get('domain')
            skills = request.POST.get('skills')
            duration = request.POST.get('duration')
            work_type = request.POST.get('work_type')
            pref_workplace = request.POST.get('pref_workplace')
            state = request.POST.get('state')
            country = request.POST.get('country')
            deadline = request.POST.get('deadline')
            organisation = request.POST.get('organisation')

            # if request.FILES['media']:
            #     media = request.FILES['media']
            #     _, f_ext = os.path.splitext(media.name)
            #     media_filename = user.username+title+f_ext
            #     print(media_filename)
            #     media.name = media_filename

            db = CollaborationRequests(user=user.id, title = title, description = description, duration = duration, domain = domain, skills = skills, work_type= work_type, pref_workplace = pref_workplace, state = state, country = country, deadline = deadline, organisation = organisation)
            db.save()
            print("NEW COLLAB REQUEST ADDED")
            return redirect('/feed/')
    else:
        return render(request, '404.html')
    
        
def viewcollaborations(request):
    if request.method == 'GET':
        collabs = CollaborationRequests.objects.all()
        print(collabs)
        usernames = []
        skills = []
        for c in collabs:
            c.description = c.description[:200]+"...."
            user = Users.objects.filter(id = c.user)[0]
            skills.append(c.skills.split(';'))
            usernames.append(user.username) 
        context = {
            'collabs':collabs,
            'usernames':usernames,
            'skills':skills
        }
        print(usernames)
        print(skills)
        return render(request, 'collabrequestcards.html',context)

def viewcollab(request,cid):
    if request.method == "GET":
        collab = CollaborationRequests.objects.filter(id = cid)[0]
        user = Users.objects.filter(id= collab.user)[0]
        skills = collab.skills.split(';')
        context = {
            'collab':collab,
            'username':user.username,
            'skills':skills
        }
        return render(request, 'collabdetails.html', context)
        return HttpResponse('EXPAND PAGE FOR COLLABOATION REQUEST')


def postproposal(request,collab_id):
    if 'username' in request.session:
        user = Users.objects.filter(username = request.session['username'])[0]
        collab = CollaborationRequests.objects.filter(id = collab_id)[0]
        if request.method == "POST":
            cover_letter = request.POST.get('proposal')

            media  = request.FILES['cv']
            _, f_ext = os.path.splitext(media.name)
            media_filename = user.username+str(collab_id)+'_cv'+f_ext
            print(media_filename)
            media.name = media_filename

            db = Proposals(user = user.id, collabrequest = collab.id, cover_letter = cover_letter, media = media )
            db.save()
            return redirect('/collaboration/viewcollaborations/')
            return HttpResponse(f'PROPOSAL for collab id - {db.collabrequest} is Sent')        

def chat(request):
    return render(request, 'chat.html')

# def searchcollabs(request):
    