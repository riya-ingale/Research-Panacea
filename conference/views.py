from multiprocessing import context
import re
from time import strftime
from django.shortcuts import render
from django.http import HttpResponse
import json
from users.models import Conference
from datetime import datetime
from users.models import Users
from users.models import Events
import os
from users.models import Journals
# Create your views here.
def upcoming_conf(request):
    try:
        if 'username' in request.session:
            if request.method == 'GET':
                if datetime.now().time().hour == 12:
                    # print(datetime.now().time().hour)
                    Title, Date, Venue, Web_link = insert_conf_db(request,'./conference.json')
                df = datetime.now()
                day = df.strftime('%d')
                month = df.strftime('%b')
                year = df.strftime('%Y')
                d = str(day) + " " + str(month) + " " + str(year)
                date =  datetime.strptime(d, '%d %b %Y')
                filt = Conference.objects.distinct().filter(timedate__gte = date)
                print(len(filt))
                context = {
                    'allconf':filt
                }    
                return render(request,'upcomingconf.html',context)
            else:
                return render(request,'404.html')
        else:
            return render(request,'login.html')
    except:
        return render(request,'404.html')

def insert_conf_db(request,name):
    f = open(name)
    data = json.load(f)
    key = data.keys()
    for k in key:
        temp = data[k]
        Title = temp['Title']
        Date = temp['Date']
        Venue = temp['Venue']
        Web_link = temp['Web_link']
        info = temp['Info']
        date = int(Date[:2])
        mon = Date.split(',')[0][-3:]
        year = Date.split(',')[1]

        d = str(date) + " " + str(mon) + " " + str(year)
        timedate =  datetime.strptime(d, '%d %b %Y')
        try:
            t = Conference.objects.get(name = Title,timedate=timedate)
            print(Title, date)
            
        except:
            db = Conference(name = Title, date=date,month = mon,year = year, website = Web_link, address = Venue, saves = 0, image = "/",info = info,timedate = timedate)
            db.save()

    return Title, Date, Venue, Web_link

#Conference Details
def conference_details(request,conf_id):
    try:
        if 'username' in request.session:
            print(conf_id)
            conf = Conference.objects.filter(id = conf_id)
            context = {
                'conf_details':conf
            }
            print(conf)
            return render(request,'conferencedetails.html',context)
        else:
            return render(request,'login.html')
    except :
        return render(request,'404.html')

def upcoming_event(request):
    if 'username' in request.session:
        if request.method == 'GET':
            df = datetime.now()
            day = df.strftime('%d')
            month = df.strftime('%b')
            year = df.strftime('%Y')
            d = str(day) + " " + str(month) + " " + str(year)
            date =  datetime.strptime(d, '%d %b %Y')
            filt = Events.objects.distinct().filter(dates__gte = date)
            
            print(len(filt))
            context = {
                'allconf':filt
            }  
            return render(request,'academicevents.html',context)
        else:
            return render(request,'404.html')
    # return render(request,'404.html')

def registeration(request) :
    try:
        if 'username' in request.session:
            if type(Users.objects.get(username = request.session['username']).user_type)==str:
                if request.method == 'GET':
                    return render(request,'events_form.html')
                elif request.method == 'POST':
                    event_name = request.POST.get('event_name')
                    date = request.POST.get('date')
                    venue = request.POST.get('venue')
                    contact = request.POST.get('contact')
                    about = request.POST.get('about')
                    speaker = request.POST.get('speaker')
                    website = request.POST.get('website')
                    domain = ""
                    count = 1
                    while(1):
                        if type(request.POST.get('domain'+str(count))) != str:
                            break
                        else:
                            domain+=request.POST.get('domain'+str(count)) +'; '
                        count+=1
                    
                    # print(request.session['username'],event_name,date,venue,contact,about,speaker,website,domain)
                    poster =  logo = proposal = add1 = add2 = add3 = None
                    if 'poster' in request.FILES:
                        poster = request.FILES['poster']
                        poster = name_changer(request,poster,event_name)
                    if 'Sponsorship Logo' in request.FILES:
                        logo = request.FILES['Sponsorship Logo']
                        logo = name_changer(request,logo,event_name)
                    if 'proposal' in request.FILES:
                        proposal = request.FILES['proposal']
                        proposal = name_changer(request,proposal,event_name)
                    if 'additional_1' in request.FILES:
                        add1 = request.FILES['additional_1']
                        add1 = name_changer(request,add1,event_name)
                    if 'additional_2' in request.FILES:
                        add2 = request.FILES['additional_2']
                        add2 = name_changer(request,add2,event_name)
                    if 'additional_3' in request.FILES:
                        add3 = request.FILES['additional_3']
                        add3 = name_changer(request,add3,event_name)
                    org_id = Users.objects.get(username = request.session['username']).id
                    events_db = Events(organizer = org_id,dates = date,address = venue,contact_number = contact, event_details = about, event_name = event_name, media = poster,media_1 = logo,media_2 = add1,media_3 = add2, media_4 = add3, pdf = proposal,speaker = speaker, domain = domain,website = website)
                    events_db.save()
                    return render(request,'events_form.html')
                else:
                    return render(request,'404.html')
            else:
                return render(request,'404.html')
        else:
            return render(request,'login.html')
    except:
        return render(request,'404.html')
def name_changer(request,file,event_name):
    _, f_ext = os.path.splitext(file.name)
    filename = (request.session['username']) + "_" + event_name+  f_ext
    print(filename)
    file.name = filename
    return file

<<<<<<< HEAD
def journals(request):
    if 'username' in request.session:
        # add_journals(request,'journal_ranking.json')
        # conf = Conference.objects.filter(id = conf_id)
        # context = {
        #     'conf_details':conf
        # }
        # print(conf)
        journal = Journals.objects.all()
        number = len(journal)
        context = {
            'number' :number,
            'journal_data' : journal
        }
        return render(request,'research-rank.html',context)
    else:
        return render(request,'login.html')


def add_journals(request,name):
    f = open(name)
    data = json.load(f)
    domains= data.keys()
    # print(domains)
    for domain in domains:
        domain_data = data[domain]
        for journal_data in domain_data:
            try:
                j_data = data[domain][journal_data]
                img = j_data['image']
                aim = j_data['aim']
                impact_score = float(j_data['metrics']['Research Impact Score:'])
                impact_factor = float(j_data['metrics']['Impact Factor:'])
                sjr = float(j_data['metrics']['SCIMAGO SJR:'])
                cite_score = float(j_data['metrics']['Citescore:'])
                h_index = float(j_data['metrics']['SCIMAGO H-index:'])
                rank = int(j_data['metrics']['Research Ranking (Computer Science)'])
                top_scientist = int(j_data['metrics']['Number of Top scientists:'])
                top_docs = int(j_data['metrics']['Documents by top scientists:'])
                editor = j_data['info']['Editors-in-Chief:']
                issn = j_data['info']['ISSN:']
                period = j_data['info']['Periodicity:']
                journal_url = j_data['info']['Journal & Submission Website:']
                # print(domain)
                # break
            except Exception as e:
                print(e) 
                print(j_data)
            try:
                t = Journals.objects.get(domain=domain,journal_name=journal_data)
                # print(Title, date) 
            except:
                db = Journals(domain=domain,journal_name=journal_data,aim=aim,image_url=img,period=period,issn=issn,\
                    journal_link=journal_url,editor=editor,impact_score=impact_score,\
                        impact_factor=impact_factor,sjr=sjr,cite=cite_score,\
                            h_index=h_index,ranking=rank,top_scientist=top_scientist,top_docs=top_docs)
                db.save()
=======
def calender(request):
    return render(request, 'calender.html')    
>>>>>>> 4bd8312be145b8e5b643797eee68b9eea2a5f999
