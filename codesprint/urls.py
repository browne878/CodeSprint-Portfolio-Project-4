from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from planner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='projects'), name='projects'),
    path('projects', views.projects, name='projects'),
    path('projects/edit/', views.edit_project, name='edit-project'),
    path('projects/delete/<str:project>', views.delete_project, name='delete-project'),
    path('sprints/<str:project>', views.sprints, name='sprints'),
    path('sprints/delete/<str:sprint>/<str:project>', views.delete_sprint, name='delete-sprint'),
    path('sprints/edit/<str:project>', views.edit_sprint, name='edit-sprint'),
    path('cases/<str:sprint>', views.cases, name='cases'),
    path('accounts/', include('allauth.urls')),
    path('new-profile', views.new_profile, name='profile'),
    path('create-profile', views.create_profile, name='create-profile'),
    path('new-company', views.new_company, name='company'),
    path('create-company', views.create_company, name='create-company'),
    path('new-project', views.new_project, name='new-project'),
    path('new-sprint/<str:project>', views.new_sprint, name='new-sprint'),
    path('new-case/<str:sprint>', views.new_case, name='new-case'),
    path('edit-case/<str:sprint>/<case>', views.edit_case, name='edit-case'),
    path(
        'delete-case/<str:sprint>/<case>',
        views.delete_case,
        name='delete-case'
    )
]
