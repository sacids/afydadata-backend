from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse,  HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User, Group
from accounts.models import *
from accounts.forms import UserForm, UserUpdateForm, UserProfileForm

# from .forms import UserForm, UserUpdateForm, UserProfileForm


class UserListView(generic.ListView):
    #permission_required = 'auth.view_user' 
    template_name = "pages/users/lists.html"
    model = User

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch( *args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        context['title'] = "Manage Users"
        context['breadcrumb'] = {'Manage Users': 0,}
        context['datatable_list']   = "userList"
        
        context['links']    = {
            'Dashboard':    reverse('dashboard'),
            'Projects':     reverse('list_projects'),
        }
        
        context['pg_actions']   = {
            'New User': reverse('create_user'),
        }

        return context


class UserCreateView(generic.CreateView):
    template_name   = 'pages/users/create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch( *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """roles"""
        roles = Group.objects.all().order_by("name")

        """forms"""
        user_form = UserForm()
        profile_form = UserProfileForm()

        context = {"roles": roles, 'user_form': user_form, 'profile_form': profile_form, 'btn_create': "Register"}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            profile = profile_form.save(commit=False)
            profile.save()

            """insert roles"""
            role_ids = request.POST.getlist('role_ids')

            for role_id in role_ids:
                role = Group.objects.get(pk=role_id)
                user.groups.add(role)

            # return response
            return HttpResponse('<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">User registered</div>')
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form, 'btn_create': "Register"}) 


class UserUpdateView(generic.UpdateView):
    """Update user"""
    # permission_required = 'auth.change_user' 
    model = User
    context_object_name = 'user'
    template_name = 'pages/users/edit.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch( *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk']) 

        #forms
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)

        # user roles
        user_roles = []
        for val in user.groups.all():
            user_roles.append(val.id)

        # roles
        roles = Group.objects.all().order_by("name")

        """context"""
        context = {"user": user, "roles": roles, 'user_roles': user_roles, 'user_form': user_form, 'profile_form': profile_form, 'btn_create': "Update"}
        return render(request, 'users/edit.html', context)
    
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])

        # forms
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()

            profile = profile_form.save(commit=False)
            profile.save()   

            """delete"""
            user.groups.clear()

            """insert/update roles"""
            role_ids = request.POST.getlist('role_ids')

            for role_id in role_ids:
                role = Group.objects.get(pk=role_id)
                user.groups.add(role)

            # return response
            return HttpResponse('<div class="bg-green-200 p-3 text-sm text-gray-600 rounded-sm">User updated</div>')
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form, 'btn_create': "Update"})         
            

class UserDeleteView(generic.View):
    """Delete Project"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDeleteView, self).dispatch( *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs['pk']

        try:
            user = User.objects.get(pk=user_id)
            user.delete()

            """response"""
            return JsonResponse({"error": False, "success_msg": "User deleted"}, safe=False)
        except:
            """response"""
            return JsonResponse({"error": True, "error_msg": "Failed to delete user"}, safe=False)