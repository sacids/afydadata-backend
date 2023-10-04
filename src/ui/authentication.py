import logging
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import LoginForm, ChangePasswordForm
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
        logging.info("Check if user already logged in")
        if request.user.is_authenticated:
            return redirect(self.success_url)
        else:    
            form = LoginForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            logging.info("Authenticate user")
            # authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                remember_me = request.POST.get("remember_me")
                if remember_me is True:
                    ONE_MONTH = 30 * 24 * 60 * 60
                    expiry = getattr(
                        settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                    request.session.set_expiry(expiry)

                # redirect
                return redirect(self.success_url)
            else:
                logging.info("Failed to login => wrong credentials")
                messages.error(request, 'Wrong credentials, try again!')
       # render view
        return render(request, self.template_name, {'form': form})


class LogoutView(generic.View):
    """Logout from the platform"""
    def get(self, request):
        logout(request)
        messages.error(request, 'Log out successfully')
        logging.info("User logout")
        # redirect
        return redirect('login')