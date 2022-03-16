from http.client import HTTPResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from collaboration.models import CollaborationRequests
import numpy as np
import os
from users.models import Users, ResearchPapers
from collaboration.models import CollaborationRequests
import json
from django.http import HttpResponse


# Create your views here.

with open('skills.json') as file:
    data = json.load(file)
    keys = data.keys()
# query = 'select id , skills from users'
def rec_matrix(data):
    user_skill = Users.objects.all() #users.object.filter
    skill_match = np.zeros((user_skill[len(user_skill)-1].id+1 , 26))
    for user in user_skill:
        if user.skills == None:
            continue
        li = user.skills.split(';')
        for ele in li:
            skill_match[user.id][data[ele]] = 1

    project = CollaborationRequests.objects.all()
    collab_match = np.zeros((project[len(project)-1].id+1 , 26))
    collab_owner = np.zeros((project[len(project)-1].id+1 , 1))

    for p in project:
        collab_owner[p.id] = p.user
        li = p.domain.split(';')
        li.extend(p.skills.split(';'))
        for ele in li:
            try:
                collab_match[p.id][data[ele]] += 1
            except:
                collab_match[p.id][data[ele]] = 1

    research_papers = ResearchPapers.objects.all()

    research_match = np.zeros((research_papers[len(research_papers)-1].id+1 , 26))
    research_owner = np.zeros((research_papers[len(research_papers)-1].id+1 , 1))

    for r in research_papers:
        # research_owner[r.id] = r.user
        li = r.domain.split(';')
        li.extend(r.keywords.split(';'))
        for ele in li:
            if ele in keys:
                try:
                    research_match[r.id][data[ele]]+=1
                except:
                    research_match[r.id][data[ele]] = 1
    
    return skill_match, collab_match ,collab_owner, research_match
        
def recommendation(request):
    if 'username' in request.session:
        user =  Users.objects.filter(username = request.session['username'])[0]
        id = user.id
        if request.method == "GET":
            skill_match , collab_match , collab_owner , research_match = rec_matrix(data)
            user_user = np.dot(skill_match , skill_match.T)
            output = user_user[id]
            users = [idx for idx in range(len(output)) if output[idx]>1 and idx!=id]
            user_collab = np.dot(skill_match , collab_match.T)
            output = user_collab[id]
            collab = [idx for idx in range(len(output)) if output[idx]>1 and collab_owner[idx]!=id]
            user_research = np.dot(skill_match , research_match.T)
            output = user_research[id]
            res_project = [idx for idx in range(len(output)) if output[idx]>=1]
            print(collab,users , res_project)
            # return HttpResponse([collab , users])
            collabs = []
            userss = []
            skills = []
            res_papers = []
            for r in res_project:
                r = ResearchPapers.objects.filter(id = r)[0]
                res_papers.append(r)

            for i in collab:
                c = CollaborationRequests.objects.filter(id = i)[0]
                collabs.append(c)
                v = c.skills.split(';')
                skills.append(v if len(v)<=2 else v[:2]) 
            uskills = []    
            for u in users:
                u = Users.objects.filter(id = u)[0]
                userss.append(u)
                uskills.append(u.skills.split(';'))
            context = {
                'collabs':collabs,
                'userss':userss,
                'skills':skills,
                'res_papers':res_papers,
                'uskills':uskills
            }
            return render(request, 'recommendation.html', context)
            

