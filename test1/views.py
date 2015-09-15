from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from authentication.models import UserType

def index(request):

    try:
        user = request.user
        request.session['mode'] = UserType.objects.get(UserId_id=user.id).Type
        if request.session['mode'] == 'R':
            return redirect('/instructor/')
        if request.session['mode'] == 'S':
            return redirect('/course/student/')
        if request.session['mode'] == 'I':
            return redirect('/instructor/')
    except:
        print "No login"
    
    return render(request, 'welcome.html')

def dummy(request):
    return 0