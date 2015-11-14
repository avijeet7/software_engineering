from django.shortcuts import render

from history.models import StudentHistory, StudentCourses


def view(request):

    if (request.session['mode'] != 'R'):
        return render(request, 'error.html', {'message': 'You do not have permission'})

    students = StudentHistory.objects.all().values_list('roll_no', 'id')
    students_courses = []
    for i, item in enumerate(students):
        students_courses.append([item[0], StudentCourses.objects.filter(user_id=item[1]).values_list('course', flat=True)])
        #print StudentCourses.objects.filter(user_id=item[1]).values_list('course')

    return render(request, 'student_view.html', {'data': students_courses})