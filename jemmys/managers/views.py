from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from .forms import LoginForm

# Create your views here.

class Login(LoginView):
    template_name = "managers/login.html"
    authentication_form = LoginForm

    def get(self, *args, **kwargs):
        # Redirect if user is already logged in.
        if self.request.user.is_authenticated:
            return redirect('managers:dashboard')
        else:
            return super().get(self.request, args, kwargs)


class Logout(LogoutView):
    template_name = "managers/logout.html"

@login_required()
def dash(request):
    return render(request, "managers/dashboard.html", context={})
