from django.contrib import admin
from .models import Company, UserProfile, Project, Sprint, Case

admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Case)
