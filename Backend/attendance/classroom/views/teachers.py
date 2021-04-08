from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required
from ..forms import TeacherSignUpForm
from ..models import User, Level, Class, Attendance

# QUIZ = CLASS, ANSWER = ATTENDANCE


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:welcome_teacher')


class TeacherWelcomeView(ListView):
    template_name = 'classroom/teachers/welcome_teacher.html'

    def get_queryset(self):
        """Return Schools """
        return self.request.user.username


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassListView(ListView):
    model = Class
    ordering = ('name', )
    context_object_name = 'classes'
    template_name = 'classroom/teachers/class_list.html'

    def get_queryset(self):
        queryset = self.request.user.classes \
            .selected_related('level') \
            .annotate(attendee_count=Count('classes', distinct=True)) \
            .annotate(attendee_count=Count('attended_class', distinct=True))

        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassCreateView(CreateView):
    model = Class
    fields = ('name', 'subject', )
    template_name = 'classroom/teachers/class_add_form.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.owner = self.request.user
        course.save()
        messages.success(self.request, 'The class was created successfully!')
        return redirect('teachers:class_change_list')


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassUpdateView(UpdateView):
    model = Class
    fields = ('name', 'subject', )
    context_object_name = 'class'
    template_name = 'classroom/teachers/class_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(
            answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.classes.all()

    def get_success_url(self):
        return reverse('teachers:class_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassDeleteView(DeleteView):
    model = Class
    context_object_name = 'class'
    template_name = 'classroom/teachers/class_delete_confirm.html'
    success_url = reverse_lazy('teachers:class_change_list')

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(
            request, 'The class %s was deleted with success!' % course.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.classes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class ClassResultView(DetailView):
    model = Class
    context_object_name = 'class'
    template_name = 'classroom/teachers/class_results.html'

    def get_context_data(self, **kwargs):
        course = self.get_object()
        attended = course.attended_class.select_related(
            'student__user').order_by('-date')
        total_attendance = attended.count()
        attendance_score = course.attended.aggregate(
            average_score=Avg('score'))
        extra_context = {
            'attended_class': attended,
            'total_attendance': total_attendance,
            'attendance_score': attendance_score
        }

        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.classes.all()
