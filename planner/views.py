from django.shortcuts import render, redirect
from .models import Company, Project, Sprint, Case, User_Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def projects(request):
    """
    Returns a list of projects to the front end and renders the page
    with the role and projects as a parameter for the page
    """
    user = User_Profile.objects.get(user_id=request.user)
    print(user.role)
    projects = Project.objects.filter(
        company=User_Profile.objects.get(user_id=request.user).company_id)
    context = {
        'role': user.role,
        'projects': {}
    }
    for project in projects:
        context['projects'][project.name] = Sprint.objects.filter(
            project=project)
    return render(request, 'planner/projects.html', context)


@login_required
def new_project(request):
    """
    Creates a new project in the database and reloads the page
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        user = User.objects.get(username=request.user)
        user_profile = User_Profile.objects.get(user_id=user)
        if not user_profile.company_id:
            print('test')
            return redirect('create-company')
        company = Company.objects.get(owner=user)
        Project.objects.create(name=name, company=company)
        user_profile.role = User_Profile.Role.ADMIN
        user_profile.save()
    return redirect('projects')


@login_required
def sprints(request, project):
    """
    Returns a list of sprints to the front end and renders the page
    with the user role and sprints as a parameter for the page
    """
    user = User_Profile.objects.get(user_id=request.user)
    project = Project.objects.get(
        name=project)
    sprints = Sprint.objects.filter(project=project)
    context = {
        'role': user.role,
        'sprints': {}
    }
    for sprint in sprints:
        try:
            context['sprints'][sprint.name] = Case.objects.filter(
                sprint=sprint
            )
            print(context['sprints'][sprint.name])
        except Case.DoesNotExist:
            context['sprints'][sprint.name] = 'No Cases Found'
    return render(request, 'planner/sprints.html', context)


@login_required
def new_sprint(request, project):
    """
    Creates a new sprint in the database and reloads the page
    with the project name as a parameter
    """
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


@login_required
def cases(request, sprint):
    user = User_Profile.objects.get(user_id=request.user)
    current_sprint = Sprint.objects.get(name=sprint)
    cases = Case.objects.filter(sprint=current_sprint)
    context = {
        'role': user.role,
        'cases': cases
    }
    return render(request, 'planner/cases.html', context)


@login_required
def new_case(request, sprint):
    if request.method == 'POST':
        Case.objects.create(
            category=request.POST.get('category'),
            title=request.POST.get('title'),
            status=request.POST.get('status'),
            due_date=request.POST.get('date-due'),
            task_size=request.POST.get('size'),
            sprint=Sprint.objects.get(name=sprint)
        )
    return redirect('cases', sprint)


@login_required
def edit_case(request, sprint, case):
    print(request.method)
    if request.method == 'POST':
        found_case = Case.objects.get(case_id=case)
        found_case.title = request.POST.get('title')
        found_case.category = request.POST.get('category')
        found_case.status = request.POST.get('status')
        found_case.due_date = request.POST.get('date-due')
        found_case.task_size = request.POST.get('size')
        found_case.save()
    return redirect('cases', sprint)


@login_required
def delete_case(request, sprint, case):
    print(request.method)
    if request.method == 'POST':
        Case.objects.filter(case_id=case).delete()
    return redirect('cases', sprint)


@login_required
def create_profile(request):
    return render(request, 'planner/create_profile.html')


@login_required
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


@login_required
def create_company(request):
    return render(request, 'planner/create_company.html')


@login_required
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
