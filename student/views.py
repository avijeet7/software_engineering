from django.shortcuts import render, redirect

from student.models import StudentCourses
from student.models import Catalog

import ast

def homepage(request):
    print request.user.id

    d = StudentCourses.objects.filter(rollno=request.user.id).values_list('rollno', 'courseid')
    print d
    c = Catalog.objects.all().values_list('id','coursecode','coursename','instructor','coursecredits','coursetag')
    

    rollnoid=1 #give rollno here
    z=[]

    for item in d:
        if item[0]==rollnoid:
            z.append(item[1])
    
    w=[]
    for id1 in z:
        for item1 in c:
            if (item1[0]==id1):
                w.append(item1[1:])

    '''if request.method == 'POST':
        form = studentform(request.POST)
        form.save()'''

    return render(request, 'homepage.html', {'data': w})

def view(request):
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
    rcodelist = request.POST.getlist('code')
    for item in rcodelist:
        id1 = Catalog.objects.get(code=item).id
        obj = StudentCourses.objects.get(courseid=id1, UserId=request.user.id)
        obj.delete()
    return redirect('/student/view/')

def add(request):
    rcodelist = request.POST.getlist('code')
    for item in rcodelist:
        id1 = Catalog.objects.get(id=int(item)).id
        obj = StudentCourses(courseid_id=int(id1), UserId_id=int(request.user.id))
        obj.save()
    return redirect('/student/view/')