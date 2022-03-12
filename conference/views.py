from multiprocessing import context
from time import strftime
from django.shortcuts import render
from django.http import HttpResponse
import json
from users.models import Conference
from datetime import datetime
from users.models import Users
import os
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
                # conf_names = []
                # for conf in filt:
                #     conf_names.append(conf.name)
                context = {
                    'allconf':filt
                }    
                # print(conf_names)
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
    
    return render(request,'404.html')

def registeration(request) :
    # try:
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
                domain = request.POST.get('domain')
                # image = request.FILES['profile_pic']
                print(event_name,date,venue,contact,about,speaker,website,domain)
                # _, f_ext = os.path.splitext(image.name)
                # image_filename = username + f_ext
                # print(image_filename)
                # image.name = image_filename
                # db = Users(first_name= first_name, last_name = last_name, username = username, email = email, contactno = contactno, usertype = usertype, organization_name = organization_name, profession = profession, city = city, state = state, country = country,skills = skills, description = description, languages = languages, scholar = scholar, orchid = orchid, profile_pic = image)
                # db.save()
                return render(request,'events_form.html')
            else:
                return render(request,'404.html')
        else:
            return render(request,'404.html')
    else:
        return render(request,'login.html')
    # except:
    #     return render(request,'404.html')
