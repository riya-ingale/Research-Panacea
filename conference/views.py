from multiprocessing import context
from time import strftime
from django.shortcuts import render
from django.http import HttpResponse
import json
from users.models import Conference
from datetime import datetime

# Create your views here.
def upcoming_conf(request):
    try:
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
            conf_names = []
            for conf in filt:
                conf_names.append(conf.name)
            context = {
                'allconf':filt
            }    
            # print(conf_names)
            return render(request,'upcomingconf.html',context)
        else:
            return render(request,'404.html')
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
        print(conf_id)
        conf = Conference.objects.filter(id = conf_id)
        context = {
            'conf_details':conf
        }
        print(conf)
        return render(request,'conferencedetails.html',context)
    except :
        return render(request,'404.html')

def upcoming_event(request):
    
    return render(request,'404.html')

def registeration(request) :

    return render(request,'404.html')
