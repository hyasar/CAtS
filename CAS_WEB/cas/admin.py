from django.contrib import admin
from .models import Project, Control

class ProjectAdmin(admin.ModelAdmin):    
    list_display = ('name', 'description', 'created_time', 'updated_time')
    list_filter = ('created_time', )
    search_fields = ('name', )
    change_form_template = "change_form.html"
    
class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_filter = ('id', )
    search_fields = ('title', 'id')
    
admin.site.login_template = "login.html"
admin.site.site_header = "CAS Administration"
admin.site.register(Project, ProjectAdmin)
admin.site.register(Control, ControlAdmin)
