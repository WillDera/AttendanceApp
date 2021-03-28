from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:welcome_teacher')
        else:
            return redirect('students:welcome_students')
    return render(request, 'classroom/home.html')
