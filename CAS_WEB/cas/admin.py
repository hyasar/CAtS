from django.contrib import admin


from .models import Project, Control

@admin.register(Project, Control)
class SuperAdmin(admin.ModelAdmin):
    pass