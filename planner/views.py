from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Company, Project, Sprint, Case, User_Profile
from django.contrib.auth.models import User


# Pages
def projects(request):
    return render(request, 'planner/projects.html')


def sprints(request):
    return render(request, 'planner/sprints.html')


def cases(request):
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
        Company.objects.create(name=name)
        user_profile.company_id = Company.objects.get(name=name)
        user_profile.save()
        return redirect('projects')
