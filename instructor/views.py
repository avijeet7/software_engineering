from django.shortcuts import render

from course.models import Catalog

def index(request):

    if request.method == 'POST':
        code = request.POST['code']
        name = request.POST['name']
        instructor = request.user.first_name
        credits = request.POST['credits']
        coursetag = request.POST['type']

        course = Catalog(code=code, name=name, instructor=instructor, credits=credits, coursetag=coursetag)
        course.save()

    courses = Catalog.objects.all().values_list('id','code','name','instructor','credits','coursetag')

    return render(request, 'InstructorView.html', {'user': request.user, 'courses':courses})