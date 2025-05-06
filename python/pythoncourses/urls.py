from django.urls import path

from .views import index, course, theme, task, editor

urlpatterns = [
    path('', index, name='index'),  # Главная страница
    path('editor/', editor, name='editor'),  # Редактор
    path('task/', task),  # Задание
    path('<slug:course>/', course, name='course'),  # Курс
    path('<slug:course>/<slug:theme>/', theme, name='theme'),  # Тема

]
