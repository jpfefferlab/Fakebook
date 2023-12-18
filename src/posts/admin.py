from django.contrib import admin
from .models import Post, Comment, Like, Dislike, Report, PlannedReaction
from fakebook.downloads import get_csv

# Register your models here.

#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'content', 'image', 'updated', 'created', 'author_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'posts.csv')
        return response

    download_csv.short_description = "Download CSV file"

# admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'body', 'updated', 'created', 'post_id', 'user_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'comments.csv')
        return response

    download_csv.short_description = "Download CSV file"

# admin.site.register(Like)
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'value', 'updated', 'created', 'post_id', 'user_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'likes.csv')
        return response

    download_csv.short_description = "Download CSV file"

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'value', 'updated', 'created', 'post_id', 'user_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'dislikes.csv')
        return response

    download_csv.short_description = "Download CSV file"

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'value', 'updated', 'created', 'post_id', 'user_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'reports.csv')
        return response

    download_csv.short_description = "Download CSV file"


@admin.register(PlannedReaction)
class PlannedReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'time_delta', 'reaction_type', 'post', 'target_profile', 'post_offset']

