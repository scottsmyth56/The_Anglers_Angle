from django.contrib import admin
from .models import User, Post, Comment, Competition, Group, Like
from .models import Competition, CompetitionUser, UserGroup
from django_summernote.admin import SummernoteModelAdmin


@admin.register(User)
class UserAdmin(SummernoteModelAdmin):
    list_display = ('first_name', 'last_name', 'username')
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'content', 'category', 'group', 'author')
    search_fields = ('title', 'category', 'content')
    list_filter = ('timestamp',)

    def author(self, obj):
        return obj.user_id.username

    author.short_description = "Author"


# @admin.register(Comment)
# class CommentAdmin(SummernoteModelAdmin):
#     list_display = ('')

admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Like)
admin.site.register(Competition)
admin.site.register(UserGroup)
admin.site.register(CompetitionUser)
