from django.shortcuts import render
from .models import Course, Theme, Lesson, Task, Test
from django.http import JsonResponse


# Главная страница
def index(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'index.html', context)


# Курс
def course(request, course):
    course = Course.objects.get(slug=course)
    themes = course.theme_set.all()
    context = {'course': course, 'themes': themes}
    return render(request, 'themesofcourse.html', context)


# Тема
def theme(request, course, theme):
    course = Course.objects.get(slug=course)
    theme = Theme.objects.get(slug=theme)
    lessons = theme.lesson_set.all()

    lns_tks = []
    for l in lessons:
        tasks = l.task_set.all()
        lns_tks.append({'lesson': l, 'tasks': tasks})
    context = {'course': course, 'theme': theme, 'lessons': lns_tks}
    return render(request, 'lessonsoftheme.html', context)


# Получение тестов
def task(request):
    if request.is_ajax():
        tsk = Task.objects.get(pk=request.POST['id'])
        tests = {'tests': [{'in': test.in_put, 'out': test.out_put} for test in tsk.test_set.all()]}
        return JsonResponse(tests)


# Редактор
def editor(request):
    return render(request, 'editor.html')
