from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

from cas.forms import *
from cas.models import *

import datetime

# Create your views here.
def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'cas/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'cas/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('projects'))




def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'cas/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        print("Errors:"+form.non_field_errors())
        return render(request, 'cas/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    return redirect(reverse('projects'))

@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def get_project_list_action(request):
    content = {}
    content['user'] = request.user

    project_list = Project.objects.filter(user=request.user)
    paginator = Paginator(project_list, 2)
    page = request.GET.get('page')
    if not page:
        page = 1
    projects = paginator.get_page(page)
    # print(project_list)
    content['projects'] = projects
    return render(request, 'cas/projects.html', content)

@login_required
def create_project_action(request):
    content = {}
    if request.method == 'GET':
        content['user'] = request.user
        content['form'] = ProjectForm()
        return render(request, 'cas/new_project.html', content)


    #### Example: create new project ####
    project = Project(name=request.POST['name'], description=request.POST['description'], user=request.user,
                       created_time=datetime.datetime.now(), updated_time=datetime.datetime.now())
    project.save()
    #### ####

    #### Example: configure control of project ####
    # control1 = Control.objects.get(cid='ac-1')
    # control2 = Control.objects.get(cid='ac-2')
    # project=Project.objects.get(name='project1')
    # ## add item into manyToMany field
    # project.control.add(control1)
    # project.control.add(control2)
    # project.save()
    #### ####

    return render(request, 'cas/new_project.html', content)


# @login_required
def get_control_list_action(request):
    # content = {}
    # content['user'] = request.user

    control_list = Control.objects.all()
    paginator = Paginator(control_list, 2)
    page = request.GET.get('page')
    if not page:
        page = 1
    controls = paginator.get_page(page)
    print(control_list)
    print(type(controls))
    # content['controls'] = controls
    # return render(request, 'cas/projects.html', content)
    return JsonResponse(controls)
