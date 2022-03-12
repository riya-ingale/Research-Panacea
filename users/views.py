from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import os
import cv2
from io import BytesIO
from collaboration.models import *

# Create your views here.

def home(request):
    return HttpResponse('HOME PAGE')
    return render(request,'home.html')

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            t = Users.objects.get(username = username)
            print(t)
            if check_password(password, t.password):
                if 'username' in request.session:
                    del request.session['username']
                request.session['username'] = username
                print(request.session['username'])
                return redirect('/feed/')
            else:
                print("Password Incorrect") 
                return redirect('/login/')   
            # redirect to success page
        except:    
            print("LOGIN failed")
            return HttpResponse("LOGIN FAILED")        


def register(request):
    if request.method == "POST":
        username = request.POST.get('susername')
        email = request.POST.get('semail')
        password = request.POST.get('spassword')
        hashed_pwd = make_password(password)
        print(username,email,hashed_pwd)
        try:
            t = Users.objects.get(username = username)
            print("USER EXISTS")
            return redirect('/login/')
        except:    
            db = Users(username = username, password = hashed_pwd, email= email )
            db.save()
            print('NEW USER CREATED')
            return redirect('/login/')


def dashboardfeed(request):
    if 'username' in request.session:
        cuser = Users.objects.filter(username = request.session['username'])[0]
        if request.method == 'GET':
            papers = ResearchPapers.objects.all().order_by("created_at")
            conferences = Conference.objects.all()
            collabs = CollaborationRequests.objects.all().order_by("created_at")
            usernames = []
            skills = []
            for r in papers:
                r.abstract = r.abstract[:300]+"...."
            for c in collabs:
                c.description = c.description[:300]+"...."
                user = Users.objects.filter(id = c.user)[0]
                skills.append(c.skills.split(';'))
                usernames.append(user.username)
            context = {
                'papers':papers,
                'conferences':conferences,
                'collabs':collabs,
                'usernames':usernames,
                'skills':skills,
                'cuser':cuser
            }
            
            # feed = papers
            # feed.extend(conferences)
            # feed.extend(collabs)
            # print(feed)
            # context = {
            #     'feed':feed,

            # }
            return render(request,'feed.html',context)
        # return HttpResponse(f"HELLO,{request.session['username']}, YOU ARE LOGGED IN")
    else:
        return render(request, '404.html')    

# Show ALL and SAVED Research Papers
def researchpapers(request):
    if 'username' in request.session:
        username = request.session['username']
        cuser = Users.objects.filter(username = username)[0]
        if request.method == "GET":
            allpapers = ResearchPapers.objects.all()
            r_usernames = []
            for r in allpapers:
                r.abstract = r.abstract[:300]+"...."
                r_user = UserResearch.objects.filter(research_id= r.id)[0]
                user = Users.objects.filter(id= r_user.user_id)[0]
                r_usernames.append(user.username)
            user = Users.objects.filter(username = username)[0]
            saved_papers = []
            saved_papers_ids = UserResearch.objects.filter(user_id= user.id).all()
            for ppr in saved_papers_ids:
                paper = ResearchPapers.objects.filter(id= ppr.research_id)[0]
                saved_papers.append(paper)
            print(saved_papers)
            context = {
                'allpapers':allpapers,
                'saved_papers':saved_papers,
                'r_usernames':r_usernames,
                'cuser':cuser
            }    
            return render(request,'researchpaper.html',context)
    else:
        return redirect('/login/')

#View a Expanded Research Paper Page
def viewresearchpaper(request, rid):
    if request.method == "GET":
        paper = ResearchPapers.objects.filter(id = rid)[0]
        context = {
            'paper':paper
        }
        return HttpResponse(paper.title)
        # return render(request, 'viewresearchpaper.html',context)

def addresearchpaper(request):
    if 'username' in request.session:
        cuser = Users.objects.filter(username = request.session['username'])
        if request.method== "POST":
            title = request.POST.get('title')
            abstract = request.POST.get('abstract')
            conference_name = request.POST.get('conference_name')
            journal_name = request.POST.get('journal_name')
            keywords = request.POST.get('keywords')
            domain = request.POST.get('domain')
            doi = request.POST.get('doi')
            published_date = request.POST.get('published_date')

            # Add User Collaborators
            
            new_paper = ResearchPapers(title= title, abstract = abstract,conference_name = conference_name, journal_name = journal_name, keywords=keywords, domain = domain, doi = doi,published_date = published_date)
            new_paper.save()
            return redirect('/addresearchpaper/')
        elif request.method == 'GET':

            return HttpResponse("ADD RESEARCH PAPER FORM")
        else:
            return render(request,'404.html')    
    else:
        return redirect('/login')        

def saverspaper(request,rid):
    if 'username' in request.session:
        user = Users.objects.filter(username = request.session['username'])[0]
    if request.method == "POST":
        db = SavedResearchPapers(user_id = user.id, r_id = rid)
        db.save()
        print(" RESEARCH PAPER SAVED")
        return redirect('/researchpapers/')


def addeducation(request):
    if 'username' in request.session:
        user  = Users.objects.filter(username = request.session['username'])
        if request.method == "POST":
            username = user.username
            institution = request.POST.get('institution')
            degree = request.POST.get('degree')
            grade = request.POST.get('grade')
            description = request.POST.get('description')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            media = request.FILES['media']
            _, f_ext = os.path.splitext(media.name)
            media_filename = username+institution+f_ext
            print(media_filename)
            media.name = media_filename

            db = Education(user_id = user.id ,institution = institution,degree = degree, grade = grade, description = description, start_date = start_date, end_date = end_date, media = media)
            db.save()
            print("EDUCATION HISTORY ADDED")
        elif request.method == "GET":
            pass
    else:
        return render(request,'404.html')

def addworkexp(request):
    if 'username' in request.session:
        user = Users.objects.filter(username = request.session['username'])[0]
        if request.method == "GET":
            return HttpResponse("ADD WORK EXPERIENCE INTERFACE")
        elif request.method == "POST":
            organization = request.POST.get('organization')
            position = request.POST.get('position')
            employment_type = request.POST.get('employment_type')
            location = request.POST.get('location')
            description = request.POST.get('description')
            ongoing = request.POST.get('ongoing')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            media = request.FILES['organization']
            _, f_ext = os.path.splitext(media.name)
            media_filename = user.username+organization+f_ext
            print(media_filename)
            media.name = media_filename

            db = WorkExp(user_id = user.id, organization = organization, position=position, employment_type = employment_type, location = location, description = description, ongoing = ongoing, start_date = start_date, end_date = end_date)
            db.save()
        else:
            return render(request, '404.html')       
    else:
        return redirect('/login/')        


def editprofile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        usertype = request.POST.get('usertype')
        organization_name = request.POST.get('organization_name')
        profession = request.POST.get('profession')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        skills = request.POST.get('skilss')
        description = request.POST.get('description')
        languages = request.POST.get('languages')
        scholar = request.POST.get('scholar')
        orchid = request.POST.get('orchid')

        image = request.FILES['profile_pic']
        _, f_ext = os.path.splitext(image.name)
        image_filename = username + f_ext
        print(image_filename)
        image.name = image_filename

        db = Users(first_name= first_name, last_name = last_name, username = username, email = email, contactno = contactno, usertype = usertype, organization_name = organization_name, profession = profession, city = city, state = state, country = country,skills = skills, description = description, languages = languages, scholar = scholar, orchid = orchid, profile_pic = image)
        db.save()
        return redirect('/dashboard/')
    elif request.method == "GET":
        return HttpResponse("EDIT USER GENERAL INFO PAGE")    
    

def addcertifications(request):
    if 'username' in request.session:
        user = Users.objects.filter(username = request.session['username'])
        if request.method == 'GET':
            return HttpResponse("ADD CERTIFICATIONS PAGE")
        elif request.method == "POST":
            course_name = request.POST.get('course_name')
            organization = request.POST.get('organization')
            link = request.POST.get('link')
            credential_id = request.POST.get('credential_id')
            completition_date = request.POST.get('completition_date') 
            db = Certification(user_id = user.id, course_name = course_name, organization = organization, link = link, credential_id = credential_id, completition_date = completition_date)
            db.save()
            print("CERTIFICATION ADDED")
            return redirect('/userprofile/')
        else:
            return render(request, '404.html')
    else:
        print("USER NOT LOGGED IN")
        return redirect('/login/')            

def userprofile(request):
    if "username" in request.session:
        username = request.session['username']
        if request.method == "GET":
            user = Users.objects.filter(username = username)[0]
            workexps = WorkExp.objects.filter(user_id = user.id).all()
            educations = Education.objects.filter(user_id = user.id).all()
            certifications  = Certification.objects.filter(user_id = user.id).all()
            user_rs = UserResearch.objects.filter(user_id = user.id).all()
            papers = []
            for u in user_rs:
                paper = ResearchPapers.objects.filter(id = u.research_id)[0]
                papers.append(paper)
            for p in papers:
                p.abstract = p.abstract[:300]+"...."    
            context = {
                'user':user,
                'papers':papers,
                'workexps' : workexps,
                'educations' : educations,
                'certifications':certifications
            }
            return render(request,'userprofile.html',context)  
    else:
        print("USER NOT LOGGED IN")
        return redirect('/login/')          


def otherprofile(request,uid):
    if "username" in request.session:
        username = request.session['username']
        if request.method == "GET":
            user = Users.objects.filter(id = uid)[0]
            uskills = user.skills.split(';')
            workexps = WorkExp.objects.filter(user_id = user.id).all()
            educations = Education.objects.filter(user_id = user.id).all()
            certifications  = Certification.objects.filter(user_id = user.id).all()
            user_rs = UserResearch.objects.filter(user_id = user.id).all()
            papers = []
            for u in user_rs:
                paper = ResearchPapers.objects.filter(id = u.research_id)[0]
                papers.append(paper)
            for p in papers:
                p.abstract = p.abstract[:300]+"...."    
            context = {
                'user':user,
                'papers':papers,
                'workexps' : workexps,
                'educations' : educations,
                'certifications':certifications,
                'uskills':uskills
            }
            return render(request,'otherprofile.html',context)  
    else:
        print("USER NOT LOGGED IN")
        return redirect('/login/')


def logout(request):
    if request.method == "POST":
        del request.session['username']
        return redirect('/login/')