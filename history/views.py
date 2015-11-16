from django.shortcuts import render

from history.models import StudentCourseHistory
from django.contrib.auth.models import User


def view(request):

    if (request.session['mode'] != 'R'):
        return render(request, 'error.html', {'message': 'You do not have permission'})

    students = User.objects.all().values_list('first_name', 'id')
    students_courses = []
    for i, item in enumerate(students):
        students_courses.append([item[0], StudentCourseHistory.objects.filter(user_id=item[1]).values_list('course', flat=True)])
        #print StudentCourseHistory.objects.filter(user_id=item[1]).values_list('course')

    return render(request, 'student_view.html', {'data': students_courses})