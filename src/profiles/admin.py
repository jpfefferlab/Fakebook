from django.contrib import admin
from .models import Profile, Relationship
from fakebook.downloads import get_csv

# Register your models here.


#admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'user', 'first_name', 'last_name', 'bio', 'email', 'country', 'created']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'profiles.csv')
        return response

    download_csv.short_description = "Download CSV file"
    
#admin.site.register(Relationship)
@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'status', 'updated', 'created', 'receiver_id', 'sender_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'relationships.csv')
        return response

    download_csv.short_description = "Download CSV file"
