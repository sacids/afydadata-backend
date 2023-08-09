from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.utils.encoding import force_str

from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

# Create your views here.

class LoginView(generic.View):
    """Login to the platform"""
    template_name = 'authentication/login.html'
    success_url = '/ui/dashboard'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        else:    
            return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):  
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)

        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #remember me
            remember_me = request.POST.get("remember_me")

            if remember_me is True:
                ONE_MONTH = 30 * 24 * 60 * 60
                expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                request.session.set_expiry(expiry)

            # redirect
            return redirect(self.success_url)
        else:
            messages.error(request, 'Wrong credentials, try again!')
            # render view
            return render(request, self.template_name, {})


class LogoutView(generic.View):
    """Logout from the platform"""
    def get(self, request):
        logout(request)
        messages.error(request, 'Log out successfully')
        return redirect('login')