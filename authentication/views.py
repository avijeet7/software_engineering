from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.models import UserType

def auth_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                request.session['mode'] = UserType.objects.get(id=user.id).Type
                if request.session['mode'] == 'R':
                    return redirect('/course/registrar/')
                if request.session['mode'] == 'S':
                    return redirect('/course/student/')
                if request.session['mode'] == 'I':
                    return redirect('/course/instructor/')

            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

    return render(request, 'login.html')

def auth_logout(request):
    logout(request)
    return redirect('/')