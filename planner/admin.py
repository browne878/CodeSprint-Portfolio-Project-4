from django.contrib import admin
from .models import Company, User, Project, Sprint, Case

admin.site.register(Company)
# admin.site.register(User)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Case)
