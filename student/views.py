from django.shortcuts import render, redirect
from student.models import StudentCourses
from student.models import Catalog
from authentication.models import UserType

from django.contrib import messages

import ast
constarints = {'min-credits':12,'max-credits':30,'max-enroll-inst':3,'max-enroll-reg':10}

def view(request):
    
    total_credits_registered = 0
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
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

    return render(request, 'StudentView.html', {'user': request.user.first_name, 'data': d1, 'courses':courses, 'mode': request.session['mode']})

def delete(request):
    credits_to_delete = 0
    success = 0
    total_credits_registered = 0
    enroll_limit_status_reg = ""
    enroll_limit_status_inst = ""

    rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=item[1]).credits

    for i in rcodelist:
        credits_to_delete = credits_to_delete + Catalog.objects.get(code=i).credits

    if ((total_credits_registered-credits_to_delete)>=constarints["min-credits"]):
        for item in rcodelist:
            id1 = Catalog.objects.get(code=item).id


            number_of_course_reg = StudentCourses.objects.filter(courseid_id=id1).count()
            myobj = StudentCourses.objects.filter(UserId=request.user.id,courseid_id=id1).values_list('UserId','courseid','enroll_limit_status_inst','enroll_limit_status_reg')
            if str(myobj[0][2]) == "C":
                #code for confirming next student from waitlist
                print "before modifying" , myobj
                list_of_waiting_students = StudentCourses.objects.filter(courseid_id=id1,enroll_limit_status_inst="W")[:1].get()
                list_of_waiting_students.enroll_limit_status_inst = "C"
                list_of_waiting_students.save()
                
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
    enroll_limit_status_reg = ""
    enroll_limit_status_inst = ""
            
    rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')

    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=int(item[1])).credits
    for i in rcodelist:
        credits_to_add = credits_to_add + Catalog.objects.get(id=int(i)).credits
    
    if ((total_credits_registered+credits_to_add)<=constarints["max-credits"]):
        for item in rcodelist:
            id1 = Catalog.objects.get(id=int(item)).id
            
            number_of_course_reg = StudentCourses.objects.filter(courseid_id=id1).count()
            z = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId','courseid','enroll_limit_status_inst','enroll_limit_status_reg')

            if number_of_course_reg >= constarints["max-enroll-reg"]:
                enroll_limit_status_reg = "NA"
            else:  
                enroll_limit_status_reg = "A"

            if number_of_course_reg >= constarints["max-enroll-inst"]:
                enroll_limit_status_inst = "W"
            else:
                enroll_limit_status_inst = "C"
            
            obj = StudentCourses(UserId_id=int(request.user.id),courseid_id=int(id1),enroll_limit_status_inst=enroll_limit_status_inst,enroll_limit_status_reg=enroll_limit_status_reg)
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
    request.session['mode'] = 'P'
    return redirect('/student/')

def can_req_prev(request):
    userdetails = UserType.objects.get(UserId=request.user.id)
    userdetails.Type = "S"
    userdetails.save()
    request.session['mode'] = 'S'
    return redirect('/student/')