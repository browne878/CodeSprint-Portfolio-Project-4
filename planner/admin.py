from django.contrib import admin
from .models import Company, Employee, Project, Sprint, Case

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Case)
