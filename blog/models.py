from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model representing a registered user.
    """
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    profile_picture = CloudinaryField("image", default="placeholder")
    email = models.EmailField(max_length=254, unique=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]


class Group(models.Model):
    """
    Group model representing a user group.
    """
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    description = models.TextField()
    featuredImage = CloudinaryField(
        "image", default="placeholder", null=True, blank=True
    )
    is_approved = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name


class Post(models.Model):
    """
    Post model representing a user post.
    """
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image1 = CloudinaryField("image", default="placeholder")
    image2 = CloudinaryField("image", default="placeholder")
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comment model representing a user comment on a post.
    """
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class Like(models.Model):
    """
    Like model representing a user's like of a post.
    """
    like_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE)


class UserGroup(models.Model):
    """
    UserGroup model representing the relationship between users and groups.
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)


class Competition(models.Model):
    """
    Competition model representing a user competition.
    """
    competition_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=150)
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    featuredImage = CloudinaryField(
        "image", default="placeholder", null=True, blank=True
    )

    def __str__(self):
        return self.title


class CompetitionUser(models.Model):
    """
    CompetitionUser model representing 
    the relationship between users and competitions.
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE)
