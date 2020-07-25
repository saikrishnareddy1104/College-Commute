from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import offerride
from django.db.models import Q
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.core.mail import send_mail
import datetime
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import re
# Create your views here.
def register(request):
    if request.method == 'POST':
        
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
     
        if password1==password2:
            if User.objects.filter(username=username).exists():
               messages.info(request,'MECID Already Registered')
               return redirect('register')
            elif User.objects.filter(email=email).exists():
              messages.info(request,'Email Already Registered')
              return redirect('register')
            else:  
               user=User.objects.create_user(username=username,password=password1,email=email,first_name=firstname,last_name=lastname)
               user.is_active = False
               user.save()
               
          
               current_site = get_current_site(request)
               mail_subject = 'Activate your meccommute account.'
               message = render_to_string('acc_active_email.html', {
                 'user': user,
                 'domain':current_site.domain,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),
               })
               to_email = user.email
               email = EmailMessage(
                        mail_subject, message, to=[to_email]
                )
               email.send()
               return HttpResponse('Please confirm your email address to complete the registration')


        else:
            messages.info(request,'Password not Matching')
            return redirect('register')
        return redirect('login')     
    else:
        
     return render(request, 'registerbootstrap.html')   

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request)  
        # return redirect('home')
        return redirect('login')
        
    else:
        return HttpResponse('Activation link is invalid!')
        
def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
          auth.login(request,user)
          return redirect('/')
        
        else:
          messages.info(request,'Invalid credentials')
          return redirect('login')  
    else:
      return render(request,'loginbootstrap.html')   

def logout(request):
  auth.logout(request)
  return redirect('/')      


def offride(request):
  if request.method == 'POST':
      i=offerride()
      i.datetime=request.POST['datetime']
      i.userid=request.user
      i.startingpoint=request.POST['startingpoint']
      i.destination=request.POST['destination']
      i.vacancy=request.POST['vacancy']
      i.phonenumb=request.POST['phonenumber']
      datetime_obj = datetime.datetime.strptime(i.datetime,'%Y-%m-%dT%H:%M')
      if datetime_obj >= datetime.datetime.now():
         i.save()
         return redirect('yourrides')  
      else:
          messages.info(request,'please enter correct date and time')
          return redirect('offride')
  else:  
    return render(request,'offerridebootstrap.html')   
    
    
def lookride(request):
    now=datetime.datetime.now()
    ride = offerride.objects.filter(datetime__gte=now).exclude(userid=request.user).exclude(Q(vacancy=0),~Q(passenger1=request.user),~Q(passenger2=request.user),~Q(passenger3=request.user),~Q(passenger4=request.user),~Q(passenger5=request.user),~Q(passenger6=request.user)).order_by('datetime')
    return render(request,"lookride.html",{'ride':ride})

def yourrides(request):
    now=datetime.datetime.now()
    ride = offerride.objects.filter(datetime__gte=now).filter(userid=request.user).order_by('datetime')
    return render(request,"yourrides.html",{'ride':ride})

def deleteyourride(request,id):
  ride=offerride.objects.get(id=id) 
  if ride.passenger1 == None and ride.passenger2 == None and ride.passenger3 == None and ride.passenger4 == None and ride.passenger5 == None and ride.passenger6 == None:
    ride.delete()
    return redirect('yourrides')
  else:  
    rider_list=[ride.passenger1,ride.passenger2,ride.passenger3,ride.passenger4,ride.passenger5,ride.passenger6]  
    for i in rider_list:
        if i is not None:   
            passeng=User.objects.get(username=i)  
            current_site = get_current_site(request)
            mail_subject = 'Ride Deleted'
            message = render_to_string('notify.html', {
                'user':passeng,
                'domain': current_site.domain,
               })
            to_email = [passeng.email]
            email = EmailMessage(
            mail_subject, message, to=[to_email]
            )
            email.send()
        else:
           pass
    ride.delete()    
    return redirect('yourrides')

def join(request,id):
    
    a=offerride.objects.get(id=id)
    if a.passenger1 == None:
       a.passenger1=request.user.username
    elif a.passenger2 == None:
       a.passenger2=request.user.username
    elif a.passenger3 == None:
       a.passenger3=request.user.username
    elif a.passenger4 == None:
       a.passenger4=request.user.username 
    elif a.passenger5 == None:
       a.passenger5=request.user.username    
    elif a.passenger6 == None:
       a.passenger6=request.user.username
    else:
        return HttpResponse("sorry something was wrong....please go back and refresh the page!!!")
    count=a.vacancy
    count=count-1
    a.vacancy=count

    a.save()
    
    return redirect('lookride')

def cancel(request,id):
    a=offerride.objects.get(id=id)
    count=a.vacancy
    count=count+1
    a.vacancy=count
    if a.passenger1==request.user.username:
        a.passenger1=None
    elif a.passenger2==request.user.username:
        a.passenger2=None
    elif a.passenger3==request.user.username:
        a.passenger3=None
    elif a.passenger4==request.user.username:
        a.passenger4=None
    elif a.passenger5==request.user.username:
        a.passenger5=None
    elif a.passenger6==request.user.username:
        a.passenger6=None
    a.save()
    
    return redirect('lookride')


def userprofile(request,username):
    user=User.objects.filter(username=username)
    return render(request,"userprofile.html",{'user':user})
