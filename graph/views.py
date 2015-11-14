from django.shortcuts import render

from course.models import Catalog, Prerequisites

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(http_method_names=['GET'])
def graph_data(request):
    courses = Catalog.objects.all().values_list('id', 'code')
    
    prereq = Prerequisites.objects.all().values_list('cid', 'prereq')

    edges = []

    for item in prereq:
        p = Catalog.objects.get(id=item[0]).code
        edges.append([item[1], p])
    print edges

    return Response([courses, edges])

def graph(request):
    print "ASD"
    data = Catalog.objects.all().values_list('code', flat=True)
    print data
    return render(request, 'graphs.html', {'courses': data})