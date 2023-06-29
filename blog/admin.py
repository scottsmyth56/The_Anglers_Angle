from django.contrib import admin
from .models import User
from .models import Post
from .models import Comment
from .models import Group
from .models import Like
from .models import Competition
from .models import CompetitionUser
from .models import UserGroup


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Like)
admin.site.register(Competition)
admin.site.register(UserGroup)
admin.site.register(CompetitionUser)
