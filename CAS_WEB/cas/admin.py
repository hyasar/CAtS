from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Project, Control

@admin.register(Project, Control)
class SuperAdmin(admin.ModelAdmin):
    pass

class MyAdminSite(AdminSite):
	site_header = "CAS Administration"
	login_template = "login.html"

admin_site = MyAdminSite(name='myadmin')
# admin_site.register(Project, Control)
