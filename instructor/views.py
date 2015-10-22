from django.shortcuts import render
from student.models import StudentCourses
from course.models import Catalog
from django.contrib.auth.models import User

def index(request):

    if request.method == 'POST':
        code = request.POST['code']
        name = request.POST['name']
        instructor = request.user.first_name
        credits = request.POST['credits']
        coursetag = request.POST['type']

        course = Catalog(code=code, name=name, instructor=instructor, credits=credits, coursetag=coursetag)
        course.save()

    courses = Catalog.objects.filter(instructor = request.user.first_name).values_list('id','code','name','instructor','credits','coursetag','prereq')
    coursesoffered = []
    for n, course in enumerate(courses):
        if not course[6]:
            z = tuple("None" if x == '' else x for x in course)
            coursesoffered.append(z)
        else:
            z = tuple(x for x in course)
            coursesoffered.append(z)
    studentlist = []
    for course in coursesoffered:
        waiting_students = StudentCourses.objects.filter(courseid = course[0],enroll_limit_status_inst="W").values_list('UserId')
        waiting_students = [ int(x[0]) for x in waiting_students ]
        confirmed_students = StudentCourses.objects.filter(courseid = course[0],enroll_limit_status_inst="C").values_list('UserId')
        confirmed_students = [ int(x[0]) for x in confirmed_students ]
        
        code = Catalog.objects.filter(id = course[0]).values_list('code')

        waiting_studentinfo = []
        for studentid in waiting_students:
            waiting_studentinfo.append(User.objects.filter(id = studentid).values_list('id','username','first_name','email')[0])

        confirmed_studentinfo = []
        for studentid in confirmed_students:
            confirmed_studentinfo.append(User.objects.filter(id = studentid).values_list('id','username','first_name','email')[0])
        
        studentlist.append([str(code[0][0]),confirmed_studentinfo,waiting_studentinfo])
        print studentlist
    return render(request, 'InstructorView.html', {'user': request.user.first_name, 'courses':coursesoffered,'studentlist':studentlist})