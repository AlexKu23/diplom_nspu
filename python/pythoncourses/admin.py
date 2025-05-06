from django.contrib import admin

from .models import *


admin.site.site_header = 'Управление сайтом'
admin.site.index_title = 'Модели'
admin.site.site_title = 'Обучение программированию на Python'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order', 'slug')
    list_display_links = None
    readonly_fields = ('slug',)
    list_editable = ('name', 'description', 'order')
    fields = ('name', 'description', 'order')
    search_fields = ('name', 'description')

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'course', 'order', 'slug')
    list_display_links = None
    readonly_fields = ('slug',)
    list_editable = ('name', 'description', 'course', 'order')
    fields = ('name', 'description', 'course','order')
    search_fields = ('name', 'description')
    list_filter = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'content', 'order', 'slug')
    readonly_fields = ('slug',)
    list_editable = ('theme', 'order')
    fields = ('name', 'content', 'theme', 'order')
    search_fields = ('name', 'content')
    list_filter = ('theme',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'formulation', 'lesson', 'order')
    list_editable = ('name', 'formulation', 'lesson', 'order')
    list_display_links = None
    fields = ('name', 'formulation', 'lesson', 'order')
    search_fields = ('name', 'formulation')
    list_filter = ('lesson',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('in_put', 'out_put', 'task')
    list_editable = ('in_put', 'out_put', 'task')
    list_display_links = None
    fields = ('in_put', 'out_put', 'task')
    list_filter = ('task',)