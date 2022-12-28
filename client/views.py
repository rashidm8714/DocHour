from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from client.models import Client, Uploads
from doctor.models import Schedule, Specialization, Doctor, Message
from datetime import date as dt, datetime, timedelta
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from django.core.files.storage import FileSystemStorage
import time
import mimetypes
import os
# Create your views here.

def login_client(request):
    return render(request,'client/client-login.html', context={})

def signup_client(request):
    return render(request,'client/client-signup.html', context={})

def client_home(request):
    client = Client.objects.get(user=request.user)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    booked = Schedule.objects.filter(taken=client)
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    uploads = Uploads.objects.filter(client=client)
    return render(request,'client/client-home.html', context={'uploads':uploads, 'client': client, 'booked':booked,'cancelled':cancelled, 'spec':spec, 'today': today})

def client_home_chat(request, slot):
    doctor = 0
    slot = Schedule.objects.get(id=slot)
    msgs = ['wait until your scheduled time to start chat']
    client = Client.objects.get(user=request.user)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    booked = Schedule.objects.filter(taken=client)

    start = datetime.strptime(str(slot.date)+" "+str(int(str(slot.start_time)[:2])) +":"+ str(slot.start_time)[3:5],"%Y-%m-%d %H:%M")
    if int(str(slot.start_time)[:2])!=23:
        end = datetime.strptime(str(slot.date)+" "+str(int(str(slot.start_time)[:2])+1) +":"+ str(slot.start_time)[3:5],"%Y-%m-%d %H:%M")
    else:
        end = datetime.strptime(str(slot.date + timedelta(days=1))+" 00:"+ str(slot.start_time)[3:5],"%Y-%m-%d %H:%M")
    now = datetime.strptime(str(datetime.now())[0:16], "%Y-%m-%d %H:%M")
    if slot.date == dt.today() and now >= start and now <= end:
        doctor = Doctor.objects.get(id=slot.doc.id)
        msgs_recieved = Message.objects.filter(sender=request.user.id, reciever=doctor.user.id)
        msgs_send = Message.objects.filter(reciever=request.user.id, sender=doctor.user.id)
        msgs = sorted(chain(msgs_send, msgs_recieved), key=attrgetter('datetime'))
    elif slot.date == dt.today() and now > end:
        msgs =["Schedule ended at " + str(end)[11:16]]
    elif slot.date == dt.today() and now < start:
        msgs =["Schedule is from " + str(start)[11:16] + " to " + str(end)[11:16] ]
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    uploads = Uploads.objects.filter(client=client)
    
    return render(request,'client/client-home.html', context={'uploads':uploads, 'slot':slot, 'client': client, 'booked':booked,'cancelled':cancelled, 'spec':spec, 'today': today, 'doctor':doctor, 'msgs': msgs})


def client_home_spec(request):
    specs=""
    if request.method == 'POST':
        specs = request.POST.get('spec')
    client = Client.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    spec_sel = Specialization.objects.get(id=specs)
    doc = Doctor.objects.filter(specialization=spec_sel)
    uploads = Uploads.objects.filter(client=client)
    return render(request,'client/client-home.html', context={'uploads':uploads, 'client': client, 'booked':booked, 'cancelled':cancelled, 'spec_sel':spec_sel,'spec':spec, 'doctors':doc,  'today': today})

def client_home_doc(request):
    specs=""
    docs=""
    if request.method == 'POST':
        specs = request.POST.get('spec_sel')
        docs = request.POST.get('doc')
    client = Client.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    spec_sel = Specialization.objects.get(spec=specs)
    doc = Doctor.objects.filter(specialization=spec_sel)
    doctor = Doctor.objects.get(id=docs)
    doc_schedule = Schedule.objects.filter(doc=doctor)
    for sc in doc_schedule:
        if sc.date < dt.today() :
            sc.delete()
    doc_schedule = Schedule.objects.filter(doc=doctor)
    uploads = Uploads.objects.filter(client=client)
    return render(request,'client/client-home.html', context={'uploads':uploads, 'client': client, 'booked':booked, 'cancelled':cancelled, 'spec_sel':spec_sel,'spec':spec, 'doctors':doc, 'doc_schedule':doc_schedule, 'doctor':doctor,  'today': today})

def client_home_send(request):
    if request.method == 'POST':
        doc = request.POST.get('doctor')
        doc = Doctor.objects.get(id=doc)
        slot = request.POST.get('slot')
        slot = Schedule.objects.get(id=slot)
        message = request.POST.get('message')
        msg = Message(sender = request.user, reciever= doc.user, message=message)
        msg.save()
        return HttpResponseRedirect(reverse('client:client_home_chat', args=(slot.id,)))

def delete_msg(request):
    if request.method == 'POST':
        slot = request.POST.get('slot')
        msg = request.POST.get('msg')
        msg = Message(id=msg)
        msg.delete()
        return HttpResponseRedirect(reverse('client:client_home_chat', args=(slot,)))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        place = request.POST.get('place')
        age = request.POST.get('age')
        health_history = request.POST.get('health-history')
        if not User.objects.filter(username=username).exists():
            user = User(username=username, first_name=firstname, last_name=lastname)
            user.set_password(password)
            user.save()
            
            client = Client(user=user, place=place, age=age, health_history=health_history)
            client.save()
            messages.success(request, "Regitration Success!")
            return HttpResponseRedirect(reverse('client:login_client'))
        else:
            messages.warning(request, "Username already exist!")
            return HttpResponseRedirect(reverse('client:login_client'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and not user.is_staff:
                login(request,user)
                return HttpResponseRedirect(reverse('client:client_home'))
            else:
                messages.warning(request, "You are not a client")
                return HttpResponseRedirect(reverse('client:login_client'))
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.warning(request, "Invalid login details given")
            return HttpResponseRedirect(reverse('client:login_client'))
    else:
        return HttpResponseRedirect(reverse('client:login_client'))

def book_slot(request, slot):
    user= User.objects.get(id = request.user.id)
    slot= Schedule.objects.get(id = slot)
    client = Client.objects.get(user=user)
    slot.taken = client
    slot.confirmed = False
    slot.save()
    return HttpResponseRedirect(reverse('client:client_home'))

def delete_slot(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.delete()
    return HttpResponseRedirect(reverse('client:client_home'))

def delete_file(request, upload):
    upload = Uploads.objects.get(id=upload)
    upload.delete()
    return HttpResponseRedirect(reverse('client:client_home'))


def upload_file(request):
    if request.method == 'POST' and request.FILES['link']:
        filen = request.POST.get("filename")
        link = request.FILES['link']
        link.name = ''.join([c if c!=' ' else '-' for c in link.name])
        fs = FileSystemStorage()
        filename = fs.save(link.name, link)
        uploaded_file_url = fs.url(filename)
        date_of_issue = request.POST.get('date_of_issue')
        client = Client.objects.get(user=request.user)
        upload = Uploads(filename=link.name, caption=filen, link=uploaded_file_url, date_of_issue=date_of_issue, client=client)
        upload.save()
        return HttpResponseRedirect(reverse('client:client_home'))

def download_file(request, id):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload= Uploads.objects.get(id=id)
    paths = upload.link.url
    filepath = BASE_DIR + "".join([c if c != '/' else '\\' for c in paths[6:]])
    with open(filepath, 'rb') as f:
        path = f.read()
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % upload.filename
    # Return the response value
    return response

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))