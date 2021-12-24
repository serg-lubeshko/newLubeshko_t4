from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    class StatusPerson(models.TextChoices):
        Pr = 'p', 'Professor'
        St = 's', 'Student'

    status = models.CharField(max_length=2,
                              verbose_name='Статус юзера',
                              choices=StatusPerson.choices,
                              default=StatusPerson.Pr)

    def __str__(self):
        return self.username


class Course(models.Model):
    """ Модель курсов """

    name = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание', blank=True)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Последние изменения')
    author = models.ForeignKey(MyUser, related_name='author_user', verbose_name='автор курса', on_delete=models.CASCADE)
    student = models.ManyToManyField(MyUser, related_name='student', verbose_name='студент курса',
                                     through='StudCour', )
    teacher = models.ManyToManyField(MyUser, related_name='teacher', verbose_name='соавтор курса',
                                     through='TeachCour', )

    def __str__(self):
        return f"{self.name}|{self.author}"


class StudCour(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course}|{self.student}"


class TeachCour(models.Model):
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tea')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cou')

    def __str__(self):
        return f"{self.course}|{self.teacher}"


class Lecture(models.Model):
    """ Модель курсов """

    title = models.CharField(max_length=255, verbose_name='Название лекции')
    file_present = models.FileField(upload_to='files/%Y/%m/%d/', blank=True, verbose_name="Презентация")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    professor = models.ForeignKey(MyUser, related_name='professor', verbose_name='Автор лекции',
                                  on_delete=models.CASCADE)

    course = models.ForeignKey(Course, related_name='lectures', verbose_name='Курс', on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.title} - автор {self.professor}"


class Homework(models.Model):
    """ Модель курсов """

    homework_task = models.TextField(verbose_name='Домашняя работа')
    title = models.CharField(verbose_name='Название домашней работы', max_length=155)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    professor = models.ForeignKey(MyUser, related_name='professor_lec', verbose_name='Автор лекции',
                                  on_delete=models.CASCADE)

    lecture_for_homework = models.ForeignKey(Lecture, related_name='lecture_for_homework', verbose_name='Лекция',
                                             on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.title} - автор {self.professor}"


class Solution(models.Model):
    """ Модель решения задачи"""

    solution_task = models.URLField(verbose_name='Решение')
    user_solution = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_solution',
                                      verbose_name='Студент')
    homework_solution = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='homework_solution',
                                          verbose_name='Домашняя работа')
    # mark = models.SmallIntegerField(verbose_name='Оценка', blank=True, null=True)
    task_solved = models.BooleanField(verbose_name='Задача решена?')

    def __str__(self):
        return f'{self.solution_task} - {self.homework_solution}'


class Mark(models.Model):
    mark = models.SmallIntegerField(verbose_name='Оценка')
    solution = models.OneToOneField(Solution, verbose_name='Решение', related_name='mark_solution', blank=True,
                                    null=True,
                                    on_delete=models.CASCADE)
    user_mark = models.ForeignKey(MyUser, related_name='user_mark', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mark} | {self.solution}'


class MessageTeacher(models.Model):
    text = models.TextField(blank=False, null=True, verbose_name='Текстовое сообщение')
    # user_message = models.ForeignKey(MyUser, verbose_name='Сообщение написал', on_delete=models.CASCADE)
    mark_message = models.ForeignKey(Mark, verbose_name='Оценка_ID', on_delete=models.CASCADE,
                                     related_name='mark_message')

    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'Сообщение текстовое № {self.id}'
