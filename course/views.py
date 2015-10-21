from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from course.models import Catalog
from authentication.models import UserType
from forms import courseform

def list(request):
    data = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'list.html', {'data': data})

def registrar(request):
    username = request.user
    if request.method == 'POST':
        form = courseform(request.POST)
        form.save()

    pending_user=[]
    pending_req = UserType.objects.filter(Type="P").values_list('UserId')
    pending_req_id = [int(i[0]) for i in pending_req]
    for i in pending_req_id:
        p_user = User.objects.filter(id = i).values_list('id','username','first_name','email')
        pending_user.append(p_user)
    #print pending_user
    
    form = courseform()
    d = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'course.html', {'form': form, 'data': d, 'username': username,'pending_user':pending_user})

def student(request):
    return redirect('/student/view/')

def instructor(request):
    data = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'list.html', {'data': data})

def add_inst(request):
    #userdetails = UserType.objects.get(UserId=request.user.id)
    usertoapprove = request.POST.getlist('inst_req')
    for i in usertoapprove:
        userdetails = UserType.objects.get(UserId=i)
        userdetails.Type = "I"
        userdetails.save()
    return redirect('/course/registrar/')

