from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from authentication.models import UserType

def index(request):

    try:
        user = request.user
        request.session['mode'] = UserType.objects.get(UserId_id=user.id).Type
        if request.session['mode'] == 'R':
            loggedin = True
            return redirect('/instructor/')
        if request.session['mode'] == 'S':
            loggedin = True
            return redirect('/course/student/')
        if request.session['mode'] == 'I':
            loggedin = True
            return redirect('/instructor/')
    except:
        loggedin = False

    return render(request, 'welcome.html', {'nbar': 'home', 'loggedin': loggedin})