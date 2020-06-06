from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Project, Control, User

# @admin_site.register(Project, Control)
# class SuperAdmin(admin.ModelAdmin):
#     pass

# class MyAdminSite(AdminSite):
# 	site_header = "CAS Administration"
# 	login_template = "login.html"

# admin_site = MyAdminSite(name='myadmin')

class ProjectAdmin(admin.ModelAdmin):    
    list_display = ('name', 'description', 'created_time', 'updated_time')
    list_filter = ('created_time', )
    search_fields = ('name', )
    change_form_template = "change_form.html"
    
class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_filter = ('id', )
    search_fields = ('title', 'id')

# class UserAdmin(admin.ModelAdmin):
	# pass
    
admin.site.login_template = "login.html"
admin.site.site_header = "CAS Administration"
admin.site.register(Project, ProjectAdmin)
admin.site.register(Control, ControlAdmin)
# admin_site.register(User, UserAdmin)
