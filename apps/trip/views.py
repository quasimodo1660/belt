from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages

from .models import *
from ..user.models import *

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        content={'user':User.objects.get(id=request.session['user_id']),
                 'all_trips': Trip.objects.all().order_by("-updated_at"),
                 }
        return render(request,'trip/process.html',content)

def add(request):
    return render(request,'trip/regit.html',{'user':User.objects.get(id=request.session['user_id'])})

def add_process(request):
    if request.method == 'POST':
        errors=Trip.objects.add_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/trip/add')
        else:
           Trip.objects.create(place=request.POST['des'],
                               content=request.POST['content'],
                               date_to=request.POST['dTo'],
                               date_from=request.POST['dFrom'],
                               user=User.objects.get(id=request.session['user_id']))
           return redirect('/trip')
       
    
    else:
        return redirect('/')



def show(request,id):
    user=User.objects.get(id=request.session['user_id'])
    trip=Trip.objects.get(id=id)
    return render(request,'trip/info.html',{'trip':trip,'user':user})

def join(request):
    Trip.objects.get(id=request.POST['trip_id']).join_user.add(User.objects.get(id=request.session['user_id']))
    return redirect('/trip')


def logout(request):
    request.session.clear()
    return redirect('/')