from django.contrib import admin
from .models import Project, Control

# @admin.register(Project, Control)
# class SuperAdmin(admin.ModelAdmin):
#     pass

class ProjectAdmin(admin.ModelAdmin):    
    list_display = ('name', 'description', 'created_time', 'updated_time')
    list_filter = ('created_time', )
    search_fields = ('name', )
    
class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_filter = ('id', )
    search_fields = ('title', 'id')
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(Control, ControlAdmin)
