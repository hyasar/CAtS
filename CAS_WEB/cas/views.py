from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from cas.utils.xml_parser import *
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
        print("Errors:" + form.non_field_errors())
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
def get_profile_action(request):
    content = dict()
    content['user'] = request.user

    # Can get user info (profile) from user object directly
    return render(request, 'cas/profile.html', content)


@login_required
def get_setting_action(request):
    content = dict()
    content['user'] = request.user

    user = User.objects.get(username=request.user.username)

    # return user password (encrypted)
    content['password'] = user.password
    return render(request, 'cas/setting.html', content)
 

@login_required
def change_password_action(request, id):
    if request.method == 'GET':
        content = dict()
        content['user'] = request.user
        
        # return with a html of a input form
        return render(request, 'cas/change_password.html', content)

    # set new password
    request.user.set_password(request.POST['password'])
    request.user.save()
    
    content = dict()
    content['user'] = request.user
    user = User.objects.get(username=request.user.username)

    # authentcate again
    updated_user = authenticate(username=user.get_username(),
                            password=request.POST['password'])

    # login again
    login(request, updated_user)
    return redirect(reverse('projects'))

 
@login_required
def update_profile_action(request):
    if request.method == 'GET':
        content = dict()
        content['user'] = request.user

        # return with a html of a input form
        return render(request, 'cas/update_profile.html', content)

    # get user input from the request form
    user = request.user
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']

    # set and save changes
    user.first_name = firstName
    user.last_name = lastName
    user.email = email
    user.save()

    content = dict()
    content['user'] = user

    return redirect(reverse('get_profile'))


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
    content['qname'] = ""
    return render(request, 'cas/projects.html', content)


# give accessibility to another user
@login_required
def share_project_action(request, id):
    if request.method == 'GET':
        content = dict()
        content['user'] = request.user
        try:
            project = Project.objects.filter(id=id).first()
            owner = project.user
        except:
            raise Http404("Project not found")

        # get all users that have accessibility to this project
        shared_user_ids = project.shared
        shared_users = []
        if shared_user_ids is not None:
            for uid in shared_user_ids:
                u = User.objects.get(id=uid)
                if u is not None:
                    shared_users.append(u)

        content['sharedUsers'] = shared_users
        content['project'] = project
        content['owner'] = owner
        return render(request, 'cas/share.html', content)

    # get the username from the request form
    project = get_object_or_404(Project, pk=id)
    name = request.POST['newSharedUser']

    try:
        user = User.objects.get(username=name)
    except:
        raise Http404("User does not exist")

    # get project shared list
    if project.shared is None:
        project.shared = []

    # add a new accessible user 
    if user.id not in project.shared:
        project.shared.append(user.id)
        project.save()

    # get all users that have accessibility to this project
    shared_users = []
    if project.shared is not None:
        for uid in project.shared:
            u = User.objects.get(id=uid)
            if u is not None:
                shared_users.append(u)

    content = dict()
    content['sharedUsers'] = shared_users
    content['project'] = project
    content['owner'] = request.user
    content['user'] = request.user

    return render(request, 'cas/share.html', content)


# remove a user from the project accessible list
@login_required
def stop_share_project_action(request, id):
    if request.method == 'GET':
        content = dict()
        content['user'] = request.user
        try:
            project = Project.objects.filter(id=id).first()
            owner = project.user
        except:
            raise Http404("Project not found")

        # get all users that have accessibility to this project
        shared_user_ids = project.shared
        shared_users = []
        if shared_user_ids is not None:
            for uid in shared_user_ids:
                u = User.objects.get(id=uid)
                if u is not None:
                    shared_users.append(u)

        content['sharedUsers'] = shared_users
        content['project'] = project
        content['owner'] = owner
        return render(request, 'cas/share.html', content)

    # get username from request form
    project = get_object_or_404(Project, pk=id)
    name = request.POST['stopSharedUser']
    
    try:
        user = User.objects.get(username=name)
    except:
        raise Http404("User does not exist")
    
    # remove the user from this project's accessible list
    if project.shared is not None:
        for uid in project.shared:
            if uid == user.id: 
                project.shared.remove(uid)
                project.save()
                
    # get all users that have accessibility to this project
    shared_users = []
    if project.shared is not None:
        for uid in project.shared:
            u = User.objects.get(id=uid)
            if u is not None:
                shared_users.append(u)

    content = dict()
    content['sharedUsers'] = shared_users
    content['project'] = project
    content['owner'] = request.user
    content['user'] = request.user

    return render(request, 'cas/share.html', content)
    

@login_required
def get_shared_project_list_action(request):
    content = dict()
    content['user'] = request.user

    # find all projects that are shared to this user
    project_list = Project.objects.filter(shared__contains=[request.user.id]).order_by('-updated_time')
    paginator = Paginator(project_list, 5)
    page = request.GET.get('page')
    if not page:
        page = 1
    projects = paginator.get_page(page)
    content['projects'] = projects
    content['qname'] = ""
    return render(request, 'cas/shared_projects.html', content)


@login_required
def get_project_configuration(request):
    content = dict()
    project = Project.objects.get(user=request.user, id=request.GET.get('id'))
    content['user'] = request.user
    content['project'] = project
    return render(request, 'cas/config_project.html', content)


@login_required
def get_project_controlls(request):
    content = dict()
    project = Project.objects.get(id=request.GET.get('id'))
    controls = list(
        Control.objects.filter(controlconfigure__in=ControlConfigure.objects.filter(project=project)).values("cid",
                                                                                                             "id",
                                                                                                             "title"))
    content['controls'] = []
    for control in controls:
        control_obj = get_object_or_404(Control, id=control['id'])
        keywords = list(ControlConfigure.objects.filter(project=project, control=control_obj).first().keywords)
        keywords.sort()
        keywords = ','.join(keywords)
        control['keywords'] = keywords
        content['controls'].append(control)

    return JsonResponse(content)


@login_required
def create_project_action(request):
    content = dict()
    if request.method == 'GET':
        content['user'] = request.user
        content['form'] = ProjectForm()
        return render(request, 'cas/new_project.html', content)

    project = Project(name=request.POST['name'], description=request.POST['description'], user=request.user,
                      created_time=datetime.datetime.now(), updated_time=datetime.datetime.now())
    project.save()

    return redirect('/config_project?id=' + str(project.id))


@login_required
def configure_control_action(request):
    # json
    data = json.loads(request.body.decode("utf-8"))

    project_id = data.get("id", 0)
    controlconfigs = data.get("controlconfigs", [])

    project = get_object_or_404(Project, pk=project_id)
    ControlConfigure.objects.filter(project=project).delete()

    content = dict()
    content['id'] = project_id
    content['controls'] = []
    ids = []

    for config in controlconfigs:
        id = config['id']
        ids.append(id)
        keywords = config['keywords']
        control = get_object_or_404(Control, id=id)
        ControlConfigure.objects.create(project=project, control=control, keywords=keywords)

    content['controls'] = list(Control.objects.filter(id__in=ids).values())
    return JsonResponse(content)


@login_required
def get_control_by_id_action(request):
    content = dict()

    control = Control.objects.filter(id=request.GET.get('id')). \
        order_by('id').values('cid', 'title', 'id', 'gid', 'parameters', 'properties', 'classinfo', 'parts')
    content['control'] = list(control)
    return JsonResponse(content)


@login_required
def get_control_list_action(request):
    content = dict()
    control_list = Control.objects.order_by('id').values('cid', 'title', 'id', 'gid', 'parameters', 'properties',
                                                         'classinfo', 'parts')
    paginator = Paginator(control_list, 10)
    page = request.GET.get('page')
    if not page:
        page = 1
    controls = paginator.page(page)
    content['controls'] = list(controls)
    return JsonResponse(content)


@login_required
def search_control_list_action(request):
    content = dict()
    keyword = request.GET.get('key')

    control_list = Control.objects.filter(Q(title__icontains=keyword) | Q(cid__icontains=keyword)). \
        order_by('id').values('cid', 'title', 'id', 'gid', 'parameters', 'properties', 'classinfo', 'parts')
    paginator = Paginator(control_list, 10)
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
    project_list = Project.objects.filter(user=request.user).filter(name__icontains=query_name).order_by('-updated_time')
    paginator = Paginator(project_list, 5)
    page = request.GET.get('page')
    if not page:
        page = 1
    projects = paginator.get_page(page)
    content['projects'] = projects
    content['qname'] = query_name
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
    project_id = request.POST['project_id']

    project = get_object_or_404(Project, pk=project_id, user=request.user)

    if project:
        project.delete()
        message = "Successfully deleted."
    else:
        message = "This project doesn't exist or belong to you."
    return HttpResponse(message)


@login_required
def project_dashboard(request):
    project_id = request.GET.get('id')
    project = get_object_or_404(Project, pk=project_id) #, user=request.user)
    content = dict()
    content['project'] = project

    return render(request, 'cas/project_dashboard.html', content)


@csrf_exempt
def parse_testing_report(request):
    if request.method == 'POST':
        # Authentication
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if not user:
            message = "Invalid username/password"
            return HttpResponse(message)

        # Validate project authorization
        project_id = request.POST['projectId']
        project = get_object_or_404(Project, pk=project_id)
        user = User.objects.get(username=username)
        if user != project.user:
            print(user)
            print(project.user)
            message = "This user doesn't own this project"
            return HttpResponse(message)

        # Parse report
        build_number = request.POST['buildNumber']
        testing_report = request.FILES['testingReport']
        if not testing_report:
            message = "No report sent"
            return HttpResponse(message)

        parse_report_xml(testing_report, project, build_number)
        message = "Report parsed successfully"
        return HttpResponse(message)


@login_required
def get_controlconfig_by_id(request):
    content = dict()
    project_id = request.GET.get('project_id')
    control_id = request.GET.get('control_id')
    project_obj = get_object_or_404(Project, id=project_id)
    control_obj = get_object_or_404(Control, id=control_id)
    try:
        controlconfig_obj = ControlConfigure.objects.get(project=project_obj, control=control_obj)
        keywords = ','.join(controlconfig_obj.keywords)
        content['control'] = {'id': control_id, 'title': control_obj.title, 'cid': control_obj.cid,
                              'keywords': keywords}
    except ControlConfigure.DoesNotExist:
        content['control'] = {'id': control_id, 'title': control_obj.title, 'cid': control_obj.cid,
                              'keywords': ''}
    return JsonResponse(content)


@login_required
def get_reports(request):
    content = dict()
    project_id = request.GET.get('id')
    project_obj = get_object_or_404(Project, id=project_id)
    reports = list(Report.objects.filter(project=project_obj).order_by('version').values())
    content['reports'] = reports
    return JsonResponse(content)


@login_required
def get_issues(request):
    report_id = request.GET.get('report_id')
    project_id = request.GET.get('project_id')
    if report_id == -1:
        issues = {}
        return issues

    report_obj = get_object_or_404(Report, id=report_id)
    project_obj = get_object_or_404(Project, id=project_id)

    try:
        controlconfigs = ControlConfigure.objects.filter(project=project_obj)
        issues = {}
        for controlconfig in controlconfigs:
            issues_tmp = search_issue_xml(controlconfig, report_obj)
            issues[controlconfig.control.cid] = issues_tmp
    except ControlConfigure.DoesNotExist:
        issues = {}
    content = dict()
    content['issues'] = issues
    return JsonResponse(content)


@login_required
def get_id_from_name(request):
    content = dict()
    name = request.GET.get('name')
    if (name == ''):
        content['name'] = name
        content['id'] = -1
        return JsonResponse(content)

    user = User.objects.get(username=name)
    
    content['name'] = name
    content['id'] = user.id
    return JsonResponse(content)


@login_required
def get_name_from_id(request):
    content = dict()
    uid = request.GET.get('id')
    print(type(uid), uid)
    if (uid == "-1"):
        content['name'] = ""
        content['id'] = uid
        return JsonResponse(content)

    user = User.objects.get(id=uid)
    
    content['name'] = user.username
    content['id'] = uid
    return JsonResponse(content)





