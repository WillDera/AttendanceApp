from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.StudentWelcomeView.as_view(), name='welcome_students'),

    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.TeacherWelcomeView.as_view(), name='welcome_teacher'),
    ], 'classroom'), namespace='teachers')),
]
