from django.contrib import admin
from .models import aboutUs, team

# Register your models here.
class aboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'locations')
    search_fields = ('title', 'locations')
    contents = ('content',)
    
    
class teamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')
    bios = ('bio',)


admin.site.register(aboutUs, aboutUsAdmin)
admin.site.register(team, teamAdmin)