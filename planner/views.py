from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Company, Project, Sprint, Case, UserProfile


@login_required
def projects(request):
    """
    Returns a list of projects to the front end and renders the page
    with the role and projects as a parameter for the page
    """

    if not UserProfile.objects.filter(user_id=request.user):
        return redirect('create-profile')

    user = UserProfile.objects.get(user_id=request.user)
    existing_projects = Project.objects.filter(
        company=UserProfile.objects.get(user_id=request.user).company_id)
    context = {
        'role': user.role,
        'projects': {}
    }
    for project in existing_projects:
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
        user_profile = UserProfile.objects.get(user_id=user)
        if not user_profile.company_id:
            return redirect('create-company')
        company = Company.objects.get(owner=user)
        Project.objects.create(name=name, company=company)
        user_profile.role = UserProfile.Role.ADMIN
        user_profile.save()
    return redirect('projects')


@login_required
def edit_project(request, project):
    """
    Edits a project in the database and reloads the page
    """
    user_profile = UserProfile.objects.get(user_id=request.user)
    if user_profile.role == UserProfile.Role.ADMIN:
        if request.method == 'POST':
            name = request.POST.get('name')
            Project.objects.filter(name=project).update(name=name)

            return redirect('projects')


@login_required
def delete_project(request, project):
    """
    Deletes a project in the database and reloads the page
    """
    user_profile = UserProfile.objects.get(user_id=request.user)
    if user_profile.role == UserProfile.Role.ADMIN:
        if request.method == 'POST':
            if Project.objects.filter(name=project):
                Project.objects.get(name=project).delete()

        return redirect('projects')


@login_required
def sprints(request, project):
    """
    Returns a list of sprints to the front end and renders the page
    with the user role and sprints as a parameter for the page
    """
    user = UserProfile.objects.get(user_id=request.user)
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
                company=UserProfile.objects.get(
                    user_id=request.user
                ).company_id,
                name=project
            )
        )
    return redirect('sprints', project)


@login_required
def delete_sprint(request, sprint, project):
    """
    Deletes a sprint in the database and reloads the page
    """
    user_profile = UserProfile.objects.get(user_id=request.user)
    if user_profile.role == UserProfile.Role.ADMIN:
        if request.method == 'POST':
            if Sprint.objects.filter(name=sprint):
                Sprint.objects.get(name=sprint).delete()

        return redirect('sprints', project)


@login_required
def cases(request, sprint):
    user = UserProfile.objects.get(user_id=request.user)
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
        if not UserProfile.objects.filter(id=user.id):
            role = UserProfile.Role.CLIENT

            if request.user.is_superuser:
                role = UserProfile.Role.ADMIN
            elif request.user.is_staff:
                role = UserProfile.Role.DEVELOPER

            UserProfile.objects.create(first_name=first_name,
                                       last_name=last_name,
                                       role=role,
                                       user_id=user)

            return redirect('projects')

    return render(request, 'planner/create_profile.html')


@login_required
def create_company(request):
    if request.user.is_superuser:
        return render(request, 'planner/create_company.html')
    else:
        return redirect('projects')


@login_required
def new_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user_id=user)
        Company.objects.create(name=name, owner=user)
        user_profile.company_id = Company.objects.get(name=name)
        user_profile.save()
        return redirect('projects')
