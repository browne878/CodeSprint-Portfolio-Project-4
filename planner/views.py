from django.shortcuts import render
from .models import Company, Project, Sprint, Case


# Pages
def login(request):
    return render(request, "planner/login.html")


def register(request):
    return render(request, "planner/register.html")


def projects(request):
    return render(request, 'planner/projects.html')


def sprints(request):
    return render(request, 'planner/sprints.html')


def cases(request):
    return render(request, 'planner/cases.html')


# RENDER MODELS
def get_company(request):
    return request


def get_employee(request):
    return request


def get_project(request):
    return request


def get_sprint(request):
    return request


def get_case(request):
    return request


# EDIT MODELS
def edit_company(request):
    return request


def edit_employee(request):
    return request


def edit_project(request):
    return request


def edit_sprint(request):
    return request


def edit_case(request):
    return request


# CREATE MODELS
def add_company(request):
    return request


def add_employee(request):
    return request


def add_project(request):
    return request


def add_sprint(request):
    return request


def add_case(request):
    return request
