from django.shortcuts import render

from history.models import StudentHistory, StudentCourses


def view(request):

    students = StudentHistory.objects.all().values_list('roll_no', 'id')
    students_courses = []
    for item in students:
        students_courses[i].append(StudentCourses.objects.filter(user_id=item[1]).values_list('course'))
        print StudentCourses.objects.filter(user_id=item[1]).values_list('course')

    return render(request, 'student_view.html', {'data': students_courses})