from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages

from .models import *

# Create your views here.
def index(request):
    messages.info(request,'I assigned default values to the fields, feel free to change the value to validate.')
    return render(request,'user/index.html')

def register(request):
    messages.info(request,'I assigned default values to the fields, feel free to change the value to validate')
    return render(request,'user/regit.html')

def loginP(request):
    if request.method == 'POST':
        errors=User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            request.session['user_id']=User.objects.get(email_address=request.POST['mail'].lower()).id
            return redirect('/trip')
       
    
    else:
        return redirect('/')

def regiP(request):
    if request.method == 'POST':
        errors=User.objects.register_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                print tag
                messages.error(request, error, extra_tags=tag)
                if tag=='warning':
                    return redirect('/')
            return redirect('/register')
        else:
            User.objects.create(first_name=request.POST['fName'],
                                last_name=request.POST['lName'],
                                password=bcrypt.hashpw(request.POST['psd1'].encode(), bcrypt.gensalt()),
                                email_address=request.POST['mail'].lower(),
                                phone=request.POST['pnum'],
                                DOB=request.POST['dob'])           
            request.session['user_id']=User.objects.last().id
            return redirect('/trip')
    else:
        return redirect('/register')

def show(request):
    user=User.objects.get(id=request.session['user_id'])
    print user.first_name
    return render(request,'user/user_info.html',{'user':user})

def logout(request):
    request.session.clear()
    return redirect('/')