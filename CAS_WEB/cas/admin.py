from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Project, Control, User

# @admin.register(Project, Control)
# class SuperAdmin(admin.ModelAdmin):
#     pass

class MyAdminSite(AdminSite):
	site_header = "CAS Administration"
	login_template = "login.html"

admin_site = MyAdminSite(name='myadmin')

class ProjectAdmin(admin.ModelAdmin):    
    list_display = ('name', 'description', 'created_time', 'updated_time')
    list_filter = ('created_time', )
    search_fields = ('name', )
    
class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_filter = ('id', )
    search_fields = ('title', 'id')

class UserAdmin(admin.ModelAdmin):
	pass
    
admin_site.register(Project, ProjectAdmin)
admin_site.register(Control, ControlAdmin)
admin_site.register(User, UserAdmin)
