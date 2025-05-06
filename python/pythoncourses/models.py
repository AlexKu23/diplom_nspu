from django.db import models
from pytils.translit import slugify


class Course(models.Model):
    """Модель курса"""
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание')
    slug = models.SlugField('Нормальный url', editable=False)
    order = models.IntegerField('Порядок вывода')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['order']


class Theme(models.Model):
    """Модель темы"""
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='Курс')
    slug = models.SlugField('Нормальный url', editable=False)
    order = models.IntegerField('Порядок вывода')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['order']


class Lesson(models.Model):
    """Модель урока"""
    name = models.CharField('Название', max_length=100)
    content = models.TextField('Содержание')
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT, verbose_name='Тема')
    slug = models.SlugField('Нормальный url', editable=False)
    order = models.IntegerField('Порядок вывода')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']


class Task(models.Model):
    """Модель задания"""
    name = models.CharField('Название', max_length=100)
    formulation = models.TextField('Формулировка')
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='Урок')
    order = models.IntegerField('Порядок вывода')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['order']


class Test(models.Model):
    """Модель теста"""
    in_put = models.TextField('Входные данные')
    out_put = models.TextField('Выходные данные')
    task = models.ForeignKey(Task, on_delete=models.PROTECT, verbose_name='Задача')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
