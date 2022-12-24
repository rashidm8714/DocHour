from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from client.models import Client
from doctor.models import Schedule, Specialization, Doctor
from datetime import date as dt, datetime, timedelta
from django.contrib.auth.models import User
# Create your views here.

def login_client(request):
    return render(request,'client/client-login.html', context={})

def signup_client(request):
    return render(request,'client/client-signup.html', context={})

def client_home(request):
    client = Client.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client)
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    return render(request,'client/client-home.html', context={'client': client, 'booked':booked,'cancelled':cancelled, 'spec':spec})

def client_home_spec(request):
    specs=""
    if request.method == 'POST':
        specs = request.POST.get('spec')
    client = Client.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client)
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    spec_sel = Specialization.objects.get(id=specs)
    doc = Doctor.objects.filter(specialization=spec_sel)
    return render(request,'client/client-home.html', context={'client': client, 'booked':booked, 'cancelled':cancelled, 'spec_sel':spec_sel,'spec':spec, 'doc':doc})

def client_home_doc(request):
    specs=""
    docs=""
    if request.method == 'POST':
        specs = request.POST.get('spec_sel')
        docs = request.POST.get('doc')
    client = Client.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client)
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    spec_sel = Specialization.objects.get(spec=specs)
    doc = Doctor.objects.filter(specialization=spec_sel)
    doctor = Doctor.objects.get(id=docs)
    doc_schedule = Schedule.objects.filter(doc=doctor)
    return render(request,'client/client-home.html', context={'client': client, 'booked':booked, 'cancelled':cancelled, 'spec_sel':spec_sel,'spec':spec, 'doc':doc, 'doc_schedule':doc_schedule, 'doctor':doctor})


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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))