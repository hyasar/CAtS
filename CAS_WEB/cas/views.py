from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from os.path import expanduser, join
from django.core.files.storage import FileSystemStorage


from .forms import *
from .models import *

import datetime
import json


# Create your views here.
def login_action(request):
    context = dict()

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
    context = dict()

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
    content = dict()
    content['user'] = request.user

    project_list = Project.objects.filter(user=request.user).order_by('-updated_time')
    paginator = Paginator(project_list, 5)
    page = request.GET.get('page')
    if not page:
        page = 1
    projects = paginator.get_page(page)
    content['projects'] = projects
    return render(request, 'cas/projects.html', content)


@login_required
def get_project_configuration(request):
    content = dict()
    content['user'] = request.user

    project = Project.objects.get(user=request.user, id=request.GET.get('id'))

    content['project'] = project
    # content['controls'] = get_control_list_action(request)
    # print(content['controls'])
    return render(request, 'cas/config_project.html', content)


@login_required
def get_project_controlls(request):
    content = dict()

    project = Project.objects.get(user=request.user, id=request.GET.get('id'))

    content['controls'] = list(project.control.all().values('id'))
    # print(list(project.control.all().values('id')))

    return JsonResponse(content)

@login_required
def create_project_action(request):
    content = dict()
    if request.method == 'GET':
        content['user'] = request.user
        content['form'] = ProjectForm()
        print(content['form'])
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

    return redirect('/config_project?id='+str(project.id))

    # return render(request, 'cas/new_project.html', content)

# @csrf_exempt
@login_required
def configure_control_action(request):
    # json
    data = json.loads(request.body.decode("utf-8"))
    # else
    # data = request.POST

    project_id = data.get("id", 0)

    project = get_object_or_404(Project, pk=project_id)
    project.control.clear()

    cids = data.get("cids", [])
    for cid in cids:
        control = get_object_or_404(Control, id=cid)
        project.control.add(control)
    project.save()
    content = dict()
    content['id'] = project_id
    content['controls'] = list(project.control.all().values())
    return JsonResponse(content)


@login_required
def get_control_by_id_action(request):
    content = {}

    control = Control.objects.filter(id=request.GET.get('id')).\
        order_by('id').values('cid', 'title', 'id', 'gid', 'parameters', 'properties', 'classinfo', 'parts')
    content['control'] = list(control)
    return JsonResponse(content)

@login_required
def get_control_list_action(request):
    content = {}
    # content['user'] = request.user

    control_list = Control.objects.order_by('id').values('cid', 'title', 'id', 'gid', 'parameters', 'properties', 'classinfo', 'parts')
    paginator = Paginator(control_list, 10)
    page = request.GET.get('page')
    if not page:
        page = 1
    controls = paginator.page(page)
    content['controls'] = list(controls)
    return JsonResponse(content)

@login_required
def search_control_list_action(request):
    content = {}
    # content['user'] = request.user
    keyword = request.GET.get('key')

    control_list = Control.objects.filter(Q(title__icontains=keyword) | Q(cid__icontains=keyword)).\
        order_by('id').values('cid', 'title', 'id', 'gid', 'parameters', 'properties', 'classinfo', 'parts')
    paginator = Paginator(control_list, 5)
    page = request.GET.get('page')
    if not page:
        page = 1
    controls = paginator.page(page)
    content['controls'] = list(controls)
    return JsonResponse(content)

  
@login_required
def search_projects_action(request):
    content = dict()
    content['user'] = request.user

    query_name = request.GET.get('name')
    project_list = Project.objects.filter(user=request.user).filter(name__contains=query_name).order_by('-updated_time')
    paginator = Paginator(project_list, 10)
    page = request.GET.get('page')
    if not page:
        page = 1
    projects = paginator.get_page(page)
    content['projects'] = projects
    return render(request, 'cas/projects.html', content)


@login_required
def search_project_by_id(request, id):
    content = dict()
    content['user'] = request.user
    try:
        project = Project.objects.filter(id=id).first()
    except Exception:
        raise Http404("Project not found")

    content['project'] = project

    return render(request, 'cas/single_project.html', content)


@login_required
def update_project(request, id):
    if request.method == 'GET':
        content = dict()
        content['user'] = request.user
        try:
            project = Project.objects.filter(id=id).first()
        except:
            raise Http404("Project not found")

        content['project'] = project
        return render(request, 'cas/update_project.html', content)

    project = get_object_or_404(Project, pk=id)
    name = request.POST['name']
    description = request.POST['description']

    project.name = name
    project.description = description
    project.save()

    content = dict()
    content['user'] = request.user
    content['project'] = project

    return redirect(reverse('projects'))


@login_required
def delete_project(request):
    # if request.method == 'GET':
    #
    #     content['user'] = request.user
    #     content['project'] = project
    #     return render(request, 'cas/delete_project.html', content)

    project_id = request.POST['project_id']

    project = get_object_or_404(Project, pk=project_id, user = request.user)
    content = dict()

    if project:
        project.delete()
        message = "Successfully deleted."
    else:
        message = "This project doesn't exist or belong to you."
    return HttpResponse(message)


@login_required
def project_dashboard(request):
    project_id = request.GET.get('id')
    project = get_object_or_404(Project, pk=project_id, user = request.user)
    content = dict()
    content['project'] = project

    return render(request, 'cas/project_dashboard.html', content)

@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        save_path = 'Files'

        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=save_path)  # defaults to   MEDIA_ROOT
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)

        message = file_url
    else:
        message = "No file."
    return HttpResponse(message)







