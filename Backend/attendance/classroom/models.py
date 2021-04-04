from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Level(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#016b2f')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-success" style="background-color: %s">%s</span>' % (
            color, name)
        return mark_safe(html)


class Class(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=255)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.name


class Attendance(models.Model):
    course = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='classes')
    text = models.CharField('Class Code', max_length=20)

    def __str__(self):
        return self.text


class ClassCode(models.Model):
    attendance = models.ForeignKey(
        Attendance, on_delete=models.CASCADE, related_name='class_code')
    text = models.CharField('Class code', max_length=20)
    is_correct = models.BooleanField('Correct code', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    classes = models.ManyToManyField(Class, through='AttendedClass')
    interests = models.ManyToManyField(Level, related_name='student_level')

    def get_unattended_classes(self, course):
        attended_classes = self.attended_classes \
            .filter(classcode__attendance__class=course) \
            .values_list('classcode__attendance__pk', flat=True)
        classes = course.classes.exclude(
            pk__in=attended_classes).order_by('text')
        return classes

    def __str__(self):
        return self.user.username


class AttendedClass(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='attended_class')
    course = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='attended_class')
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='attended_classes')
    answer = models.ForeignKey(
        ClassCode, on_delete=models.CASCADE, related_name='+')
