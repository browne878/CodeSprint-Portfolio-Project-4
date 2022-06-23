from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Company, Project, Sprint, Case, User_Profile
from django.contrib.auth.models import User


# Pages
def projects(request):
    projects = Project.objects.filter(
        company=User_Profile.objects.get(user_id=request.user).company_id)
    context = {
        'projects': {}
    }
    for project in projects:
        try:
            context['projects'][project.name] = Sprint.objects.filter(
                project=project)
        except Sprint.DoesNotExist:
            context['projects'][project.name] = 'No Sprints Found'
    return render(request, 'planner/projects.html', context)


def new_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = User.objects.get(username=request.user)
        company = Company.objects.get(owner=user)
        Project.objects.create(name=name, company=company)
        user_profile = User_Profile.objects.get(user_id=user)
        user_profile.role = User_Profile.Role.ADMIN
        user_profile.save()
    return redirect('projects')


def sprints(request, project):
    company = User_Profile.objects.get(user_id=request.user).company_id
    project = Project.objects.get(
        company=company)
    sprints = Sprint.objects.filter(project=project)
    context = {
        'sprints': {}
    }
    for sprint in sprints:
        try:
            context.sprints[sprint.name] = Case.objects.get(sprint=sprint)
        except Case.DoesNotExist:
            context['sprints'][sprint.name] = 'No Cases Found'
    return render(request, 'planner/sprints.html', context)


def new_sprint(request, project):
    if request.method == 'POST':
        Sprint.objects.create(
            name=request.POST.get('name'),
            starts_at=request.POST.get('date-starts'),
            ends_at=request.POST.get('date-ends'),
            project=Project.objects.get(
                company=User_Profile.objects.get(
                    user_id=request.user
                    ).company_id,
                name=project
            )
        )
    return redirect('sprints', project)


def cases(request, sprint):
    return render(request, 'planner/cases.html')


def create_profile(request):
    return render(request, 'planner/create_profile.html')


def new_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('user')
        user = User.objects.get(username=username)
        try:
            User_Profile.objects.get(user_id=user)
        except User_Profile.DoesNotExist:
            User_Profile.objects.create(first_name=first_name,
                                        last_name=last_name,
                                        role=User_Profile.Role.CLIENT,
                                        user_id=user)
            return redirect('create-company')

    return render(request, 'planner/create_profile.html')


def create_company(request):
    return render(request, 'planner/create_company.html')


def new_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('user')
        user = User.objects.get(username=username)
        user_profile = User_Profile.objects.get(user_id=user)
        Company.objects.create(name=name, owner=user)
        user_profile.company_id = Company.objects.get(name=name)
        user_profile.save()
        return redirect('projects')
