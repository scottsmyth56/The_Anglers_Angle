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
    list_display = ('title', 'content', 'category', 'group', 'get_author')
    search_fields = ('title', 'category', 'content')
    list_filter = ('timestamp',)

    def get_author(self, obj):
        return obj.user_id.username

    get_author.short_description = "Author"


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('comment', 'get_commenter', 'get_post_title')
    search_fields = ('get_commenter', 'get_post_title', 'comment')
    list_filter = ('timestamp',)

    def get_commenter(self, obj):
        return obj.user_id.username

    def get_post_title(self, obj):
        return obj.post_id.title

    get_commenter.short_description = "Commenter"
    get_post_title.short_description = "Post Title"


@admin.register(Group)
class GroupAdmin(SummernoteModelAdmin):
    list_display = ('group_name', 'description')
    search_fields = ('group_name',)


@admin.register(Competition)
class CompetitionAdmin(SummernoteModelAdmin):
    list_display = ('title', 'description', 'location', 'date')
    search_fields = ('title', 'location', 'date', 'description')
    list_filter = ('date', 'location',)


@admin.register(UserGroup)
class UserGroupAdmin(SummernoteModelAdmin):
    list_display = ('get_group_member', 'get_group_name')
    search_fields = ('get_group_name',)

    def get_group_member(self, obj):
        return obj.user_id.username

    def get_group_name(self, obj):
        return obj.group_id.group_name

    get_group_member.short_description = 'Member'
    get_group_name.short_description = 'Group'


@admin.register(CompetitionUser)
class CompetitionUserAdmin(SummernoteModelAdmin):
    list_display = ('get_competition_member', 'get_competition_name')
    search_fields = ('get_competition_member', 'get_competition_name')

    def get_competition_member(self, obj):
        return obj.user_id.username

    def get_competition_name(self, obj):
        return obj.competition_id.title

    get_competition_member.short_description = "Participant"
    get_competition_name.short_description = "Competition"


admin.site.register(Like)
