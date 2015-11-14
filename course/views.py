from django.shortcuts import render
from course.models import Catalog, Prerequisites


def list(request):
    data = Catalog.objects.all().values_list('code', 'name', 'credits', 'id')
    output = []
    for item in data:
        output.append([item, Prerequisites.objects.filter(cid=item[3]).values_list('prereq')])

    try:
        request.session["mode"]
        loggedin = True
    except:
        loggedin = False
    return render(request, 'list.html', {'data': output, 'nbar': 'courselist', 'loggedin': loggedin})