from django.shortcuts import render
from course.models import Catalog


def list(request):
    data = Catalog.objects.all().values_list('code', 'name', 'credits')
    return render(request, 'list.html', {'data': data, 'nbar': 'courselist'})