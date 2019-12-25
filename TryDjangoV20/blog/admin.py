from django.contrib import admin
from .models import UserBlog


# Register your models here.
# @admin.register(UserBlog)

class UserBlogModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "title", "timestamp", "updated"]
    list_display_links = ["__str__"]
    list_filter = ["user", "updated"]
    search_fields = ["title", "content"]
    list_editable = ["title"]

    class Meta:
        model = UserBlog

admin.site.register(UserBlog, UserBlogModelAdmin)
