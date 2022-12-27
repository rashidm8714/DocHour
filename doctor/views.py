from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctor.models import Doctor, Schedule, Specialization, Message
from client.models import Client
from datetime import date as dt, datetime
from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
# Create your views here.
def welcome(request):
    return render(request,'doctor/welcome.html', context={})

def login_doc(request):
    return render(request,'doctor/doc-login.html', context={})

def signup_doc(request):
    spec = Specialization.objects.all()
    return render(request,'doctor/doc-signup.html', context={'spec':spec})

def doc_home(request):
    doc = Doctor.objects.get(user=request.user)
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    return render(request,'doctor/doc-home.html', context={'doc':doc, 'dates':dates, 'today':today})

def doc_home_chat(request, client):
    doc = Doctor.objects.get(user=request.user)
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    client = Client.objects.get(id=client)
    msgs_send = Message.objects.filter(sender=request.user.id, reciever=client.user.id)
    msgs_recieved = Message.objects.filter(reciever=request.user.id, sender=client.user.id)
    msgs = sorted(chain(msgs_send, msgs_recieved), key=attrgetter('datetime'))
    return render(request,'doctor/msgbox.html', context={'doc':doc, 'dates':dates, 'today':today, 'client' :client, 'msgs':msgs})
    
def doc_home_send(request):
    if request.method == 'POST':
        client = request.POST.get('client')
        client = Client.objects.get(id=client)
        message = request.POST.get('message')
        msg = Message(sender = request.user, reciever= client.user, message=message)
        msg.save()
        print(msg)
        return HttpResponseRedirect(reverse('doctor:doc_home_chat', args=(client.id,)))

def delete_msg(request):
    if request.method == 'POST':
        client = request.POST.get('client')
        msg = request.POST.get('msg')
        msg = Message(id=msg)
        msg.delete()
        return HttpResponseRedirect(reverse('doctor:doc_home_chat', args=(client,)))



def doc_home_slot(request, date):
    doc = Doctor.objects.get(user=request.user)
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    slot = Schedule.objects.filter(doc=doc, date=date)
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    return render(request,'doctor/doc-home.html', context={'doc':doc, 'dates':dates, 'slots':slot, 'date':date, 'today':today})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        place = request.POST.get('place')
        hospital = request.POST.get('hospital')
        specialization = request.POST.get('specialization')
        specialization = Specialization.objects.get(id=specialization)
        if not User.objects.filter(username=username).exists():
            user = User(username=username, first_name=firstname, last_name=lastname, is_staff=1)
            user.set_password(password)
            user.save()

            doc = Doctor(user=user, location=place, hospital=hospital, specialization=specialization)
            doc.save()
            messages.success(request, "Regitration Success!")
            return HttpResponseRedirect(reverse('doctor:login_doc'))
        else:
            messages.warning(request, "Username already exist!")
            return HttpResponseRedirect(reverse('doctor:login_doc'))

        

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and user.is_staff:
                login(request,user)
                print('working')
                return HttpResponseRedirect(reverse('doctor:doc_home'))
            else:
                messages.warning(request, "You are not a doctor")
                return HttpResponseRedirect(reverse('doctor:login_doc'))
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.warning(request, "Invalid login details given")
            return HttpResponseRedirect(reverse('doctor:login_doc'))
    else:
        return HttpResponseRedirect(reverse('doctor:login_doc'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))


def add_slot(request):
    if request.method == 'POST':
        doc = Doctor.objects.get(user=request.user)
        date = request.POST.get('date')
        start = request.POST.get('start')
        no_hours = int(request.POST.get('no_hours'))

        for _ in range(no_hours):
            start =  str(datetime.strptime(str(int(start[:2])+1) +":"+ start[3:],"%H:%M"))[11:16]
            sc = Schedule(doc=doc, date=date, start_time=start, taken=None)
            sc.save()
    return HttpResponseRedirect(reverse('doctor:doc_home_slot', args=(date,)))

def confirm_booking(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.confirmed = True
    slot.save()
    return HttpResponseRedirect(reverse('doctor:doc_home_slot', args=(slot.date,)))

def cancel_booking(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.confirmed=False
    slot.cancelled = slot.taken
    slot.taken=None
    slot.save()
    return HttpResponseRedirect(reverse('doctor:doc_home_slot', args=(slot.date,)))

def delete_slot(request, slot):
    slot = Schedule.objects.get(id=slot)
    date = slot.date
    slot.delete()
    return HttpResponseRedirect(reverse('doctor:doc_home_slot', args=(date,)))

