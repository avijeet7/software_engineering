from django.shortcuts import render, redirect

from student.models import StudentCourses
from student.models import Catalog

from authentication.models import UserType

import ast
constarints = {'min-credits':12,'max-credits':30}

def homepage(request):
    print request.user.id

    d = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    print d
    c = Catalog.objects.all().values_list('id','coursecode','coursename','instructor','coursecredits','coursetag')
    

    rollnoid=request.user.id #give rollno here
    z=[]
    for item in d:
        if item[0]==rollnoid:
            z.append(item[1])
    w=[]
    for id1 in z:
        for item1 in c:
            if (item1[0]==id1):
                w.append(item1[1:])

    return render(request, 'homepage.html', {'data': w})

def view(request):
    print request
    data = StudentCourses.objects.filter(UserId=request.user.id)
    d1 = []
    for item in data:
        d = []
        d.append(item.courseid.code)
        d.append(item.courseid.name)
        d.append(item.courseid.instructor)
        d.append(item.courseid.credits)
        d.append(item.courseid.coursetag)
        d1.append(d)

    courses = Catalog.objects.all().values_list('id','code','name','instructor','credits','coursetag')
    return render(request, 'StudentView.html', {'user': request.user.first_name, 'data': d1, 'courses':courses})

def delete(request):
    credits_to_delete = 0
    total_credits_registered = 0
    rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')

    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=item[1]).credits

    for i in rcodelist:
        credits_to_delete = credits_to_delete + Catalog.objects.get(code=i).credits
    
    #print total_credits_registered
    #print credits_to_delete
    

    if ((total_credits_registered-credits_to_delete)>=constarints["min-credits"]):
        for item in rcodelist:
            id1 = Catalog.objects.get(code=item).id
            obj = StudentCourses.objects.get(courseid=id1, UserId=request.user.id)
            obj.delete()
    else:
        print "Minimum number of credits to be registered are ",constarints["min-credits"]


    
    return redirect('/student/view/')

def add(request):
    credits_to_add = 0
    total_credits_registered = 0

    rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')

    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=int(item[1])).credits
    for i in rcodelist:
        credits_to_add = credits_to_add + Catalog.objects.get(id=int(i)).credits
    
    #print total_credits_registered
    #print credits_to_add

    if ((total_credits_registered+credits_to_add)<=constarints["max-credits"]):
        for item in rcodelist:
            id1 = Catalog.objects.get(id=int(item)).id
            obj = StudentCourses(courseid_id=int(id1), UserId_id=int(request.user.id))
            #print obj
            obj.save()
    else:
        print "Maximum number of credits to be added are ",constarints["max-credits"]
    return redirect('/student/view/', {'a': 'ffff'})

def req_instr_prev(request):
    userdetails = UserType.objects.get(UserId=request.user.id)
    userdetails.Type = "P"
    userdetails.save()
    return redirect('/student/view/')