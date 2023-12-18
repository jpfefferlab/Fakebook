from django.contrib import admin

from analytics.models import TrackedSession, TrackedPostView
from fakebook.downloads import get_csv


@admin.register(TrackedSession)
class TrackedSessionAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['username', 'duration', 'first_seen', 'last_seen']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'sessions.csv')
        return response

    def username(self, session):
        return session.profile.user.username

    def duration(self, session):
        return session.last_seen - session.first_seen

    download_csv.short_description = "Download CSV file"

@admin.register(TrackedPostView)
class TrackedPostViewAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['username', 'total_time_seconds', 'post_id', 'post_content']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'sessions.csv')
        return response

    def username(self, post_view):
        return post_view.profile.user.username

    def total_time_seconds(self, post_view):
        return round(post_view.total_time_ms / 1000)

    def post_content(self, post_view):
        return post_view.post.content

    download_csv.short_description = "Download CSV file"