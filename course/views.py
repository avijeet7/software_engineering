from django.shortcuts import render, redirect

from course.models import Catalog

from forms import courseform

def list(request):
    data = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'list.html', {'data': data})

def registrar(request):
    username = request.user
    if request.method == 'POST':
        form = courseform(request.POST)
        form.save()

    form = courseform()
    print form
    d = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'course.html', {'form': form, 'data': d, 'username': username})

def student(request):
    return redirect('/student/view/')

def instructor(request):
    data = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'list.html', {'data': data})
