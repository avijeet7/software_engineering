from django.shortcuts import render, redirect
from student.models import StudentCourses, Student
from course.models import Catalog, Prerequisites
from authentication.models import UserType
from registrar.models import Constraints
from django.contrib import messages
from history.models import StudentCourseHistory

import ast
#constarints = {'min-credits':12,'max-credits':30,'max-enroll-inst':3,'max-enroll-reg':10}

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
        d.append(Prerequisites.objects.filter(cid=item.courseid.id).values_list('prereq', flat=True))
        d1.append(d)
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    for item in codelist:
        codelistid.append(int(item[1]))
    courses = Catalog.objects.exclude(id__in = codelistid).values_list('id','code','name','instructor','credits','coursetag')
    coursedata = []
    for i, elem in enumerate(courses):
        coursedata.append([elem, Prerequisites.objects.filter(cid=elem[0]).values_list('prereq', flat=True)])
    min_credits = Constraints.objects.get().min_credits
    if (total_credits_registered<min_credits):
        messages.add_message(request,messages.INFO,"Minimum number of credits needed are "+str(min_credits),extra_tags='viewerror')

    return render(request, 'StudentView.html', {'user': request.user.first_name, 'data': d1, 'courses':coursedata, 'mode': request.session['mode'], 'nbar': 'home'})

def delete(request):
    credits_to_delete = 0
    success = 0
    total_credits_registered = 0
    enroll_limit_status_reg = ""
    enroll_limit_status_inst = ""
    max_enroll_inst = 0
    min_credits = Constraints.objects.get().min_credits

    rcodelist = request.POST.getlist('code')
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')
    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=item[1]).credits

    for i in rcodelist:
        credits_to_delete = credits_to_delete + Catalog.objects.get(code=i).credits

    if ((total_credits_registered-credits_to_delete)>=min_credits):
        for item in rcodelist:
            id1 = Catalog.objects.get(code=item).id
            max_enroll_inst = Catalog.objects.get(id=id1).max_enroll_limit

            number_of_course_reg = StudentCourses.objects.filter(courseid_id=id1).count()
            myobj = StudentCourses.objects.filter(UserId=request.user.id,courseid_id=id1).values_list('UserId','courseid','enroll_limit_status_inst','enroll_limit_status_reg')
            
            if str(myobj[0][2]) == "C":
                #code for confirming next student from waitlist
                print "before modifying" , myobj
                if (number_of_course_reg > max_enroll_inst): 
                    list_of_waiting_students = StudentCourses.objects.filter(courseid_id=id1,enroll_limit_status_inst="W")[:1].get()
                    list_of_waiting_students.enroll_limit_status_inst = "C"
                    print "new" , list_of_waiting_students
                    list_of_waiting_students.save()
                
            obj = StudentCourses.objects.get(courseid=id1, UserId=request.user.id)
            obj.delete()
            success = 1
    
    if success :
        successmsg = "Courses deleted successfully"
        messages.add_message(request,messages.INFO,successmsg,extra_tags='deletesuccess')
    else:
        errormsg = "Minimum number of credits needed are " + str(min_credits)
        messages.add_message(request,messages.INFO,errormsg,extra_tags='deleteerror')

    return redirect('/student/')

def add(request):

    rcodelist = request.POST.getlist('code')

    """Check Prerequisites are met or not"""
    stu_courses = StudentCourseHistory.objects.filter(user=request.user.id).values_list('course', flat=True)
    for item in rcodelist:
        course_prereq = Prerequisites.objects.filter(cid=item).values_list('prereq', flat=True)
        print course_prereq , " :: " , stu_courses
        c = 0
        for i in course_prereq:
            if i in stu_courses:
                c += 1
        if c == len(course_prereq):
            """Prerequisites satisfied, add the course"""
            add_the_course(request, [item])
        else:
            """Course not added"""
            errormsg = "Course prerequisites not satisfied"
            messages.add_message(request,messages.INFO,errormsg,extra_tags='adderror')

    return redirect('/student/')

def add_the_course(request, code):
    credits_to_add = 0
    total_credits_registered = 0
    success = 0
    enroll_limit_status_reg = ""
    enroll_limit_status_inst = ""
    max_enroll_reg = 0 
    max_enroll_inst = 0

    rcodelist = code
    codelist = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId', 'courseid')

    for item in codelist:
        total_credits_registered = total_credits_registered + Catalog.objects.get(id=int(item[1])).credits
    for i in rcodelist:
        credits_to_add = credits_to_add + Catalog.objects.get(id=int(i)).credits
    
    max_credits = Constraints.objects.get().max_credits
    if ((total_credits_registered+credits_to_add)<=max_credits):
        for item in rcodelist:
            id1 = Catalog.objects.get(id=int(item)).id
            max_enroll_inst = Catalog.objects.get(id=int(item)).max_enroll_limit
            max_enroll_reg = Constraints.objects.get().max_enroll_limit_reg

            number_of_course_reg = StudentCourses.objects.filter(courseid_id=id1).count()
            z = StudentCourses.objects.filter(UserId=request.user.id).values_list('UserId','courseid','enroll_limit_status_inst','enroll_limit_status_reg')

            if number_of_course_reg >= max_enroll_reg:
                enroll_limit_status_reg = "NA"
            else:  
                enroll_limit_status_reg = "A"

            if number_of_course_reg >= max_enroll_inst:
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
        errormsg = "Maximum number of credits can be added are " + str(max_credits)
        messages.add_message(request,messages.INFO,errormsg,extra_tags='adderror')

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

def edit_profile(request):
    if request.method == 'POST':
        uid = request.user.id
        rn = request.POST['rn']
        dept = request.POST['dept']

        try:
            sd_new = Student(rollno=rn, department=dept, UserId_id=uid)
            sd_old = Student.objects.filter(UserId=uid)
            sd_old.delete()
            sd_new.save()
            msg = "Details successfully added!"
            messages.add_message(request,messages.INFO,msg,extra_tags='adderror')
        except:
            errormsg = "Error while adding details"
            messages.add_message(request,messages.ERROR,errormsg,extra_tags='adderror')

    sd = Student.objects.filter(UserId=request.user.id).values_list('rollno', 'department')
    return render(request, 'profile.html', {'uid': request.user.id, 'rn': sd[0][0], 'nm': request.user.first_name, 'dept': sd[0][1]})