from django.contrib import admin
from .models import Advertisement
from fakebook.downloads import get_csv

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'image', 'text', 'url', 'num_clicked']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'advertisements.csv')
        return response

    download_csv.short_description = "Download CSV file"