from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from authentication.models import UserType


def index(request):
    username = request.user

    pending_user=[]
    pending_req = UserType.objects.filter(Type="P").values_list('UserId')
    pending_req_id = [int(i[0]) for i in pending_req]
    for i in pending_req_id:
        p_user = User.objects.filter(id = i).values_list('id','username','first_name','email')
        pending_user.append(p_user)

    return render(request, 'RegistrarView.html', {'username': username,'pending_user':pending_user})

def add_inst(request):
    #userdetails = UserType.objects.get(UserId=request.user.id)
    usertoapprove = request.POST.getlist('inst_req')
    for i in usertoapprove:
        userdetails = UserType.objects.get(UserId=i)
        userdetails.Type = "I"
        userdetails.save()
    return redirect('/registrar/')