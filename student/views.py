from django.shortcuts import render, redirect
from student.models import StudentCourses
from student.models import Catalog
from authentication.models import UserType

from django.contrib import messages

import ast
constarints = {'min-credits':12,'max-credits':30}

# def homepage(request):
#     print request.user.id

#     d = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
#     print d
#     c = Catalog.objects.all().values_list('id','code','coursename','instructor','coursecredits','coursetag')
    

#     rollnoid=request.user.id #give rollno here
#     z=[]
#     for item in d:
#         if item[0]==rollnoid:
#             z.append(item[1])
#     w=[]
#     for id1 in z:
#         for item1 in c:
#             if (item1[0]==id1):
#                 w.append(item1[1:])

#     return render(request, 'homepage.html', {'data': w})

def view(request):
    
    #x = Catalog.objects.filter(id__in = [1]).values_list('id','code','name','instructor','credits','coursetag','prereq')
    #print x
    total_credits_registered = 0
    #rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    print codelist
    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=item[1]).credits

    data = StudentCourses.objects.filter(UserId=request.user.id)
    d1 = []    
    codelistid = []
    for item in data:
        d = []
        d.append(item.courseid.code)
        d.append(item.courseid.name)
        d.append(item.courseid.instructor)
        d.append(item.courseid.credits)
        d.append(item.courseid.coursetag)
        d1.append(d)
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    for item in codelist:
        codelistid.append(int(item[1]))
    courses = Catalog.objects.exclude(id__in = codelistid).values_list('id','code','name','instructor','credits','coursetag')
    
    if (total_credits_registered<constarints["min-credits"]):
        messages.add_message(request,messages.INFO,"Minimum number of credits needed are "+str(constarints["min-credits"]),extra_tags='viewerror')
    return render(request, 'StudentView.html', {'user': request.user.first_name, 'data': d1, 'courses':courses})

def delete(request):
    credits_to_delete = 0
    success = 0
    
    total_credits_registered = 0
    rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    print codelist
    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=item[1]).credits

    for i in rcodelist:
        credits_to_delete = credits_to_delete + Catalog.objects.get(code=i).credits

    if ((total_credits_registered-credits_to_delete)>=constarints["min-credits"]):
        for item in rcodelist:
            id1 = Catalog.objects.get(code=item).id
            obj = StudentCourses.objects.get(courseid=id1, UserId=request.user.id)
            obj.delete()
            success = 1
    
    if success :
        successmsg = "Courses deleted successfully"
        messages.add_message(request,messages.INFO,successmsg,extra_tags='deletesuccess')
    else:
        errormsg = "Minimum number of credits needed are " + str(constarints["min-credits"])
        messages.add_message(request,messages.INFO,errormsg,extra_tags='deleteerror')
 
    return redirect('/student/')

def add(request):
    credits_to_add = 0
    total_credits_registered = 0
    success = 0
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
            success = 1
            obj.save()

    if success :
        successmsg = "Courses added successfully"
        messages.add_message(request,messages.INFO,successmsg,extra_tags='addsuccess')
    else:
        errormsg = "Maximum number of credits can be added are " + str(constarints["max-credits"])
        messages.add_message(request,messages.INFO,errormsg,extra_tags='adderror')
 
    return redirect('/student/')

def req_instr_prev(request):
    userdetails = UserType.objects.get(UserId=request.user.id)
    userdetails.Type = "P"
    userdetails.save()
    return redirect('/student/')