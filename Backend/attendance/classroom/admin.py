from django.contrib import admin
from .models import Subject, User, Quiz, Department, Student

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Department)
