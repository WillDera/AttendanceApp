from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('student/', include(([
        path('', students.QuizListView.as_view(), name='class_list'),
        path('level/', students.StudentLevelView.as_view(),
             name='student_level'),
        path('marked/', students.TakenQuizListView.as_view(),
             name='taken_quiz_list'),
        path('class/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('lecturer/', include(([
        path('', teachers.ClassListView.as_view(), name='quiz_change_list'),
        path('class/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('class/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('class/<int:pk>/delete/',
             teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('class/<int:pk>/results/',
             teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('class/<int:pk>/question/add/',
             teachers.question_add, name='question_add'),
        path('class/<int:quiz_pk>/question/<int:question_pk>/',
             teachers.question_change, name='question_change'),
        path('class/<int:quiz_pk>/question/<int:question_pk>/delete/',
             teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
