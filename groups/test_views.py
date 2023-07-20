from django.test import TestCase
from django.test import TestCase, Client
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from blog.models import Group, UserGroup, Post, User
from django.urls import reverse_lazy, reverse


class SetUpClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.group1 = Group.objects.create(
            group_name="Test Group 1",
            description="Test Description 1",
            is_approved=True,
            creator=self.user,
        )
        self.group2 = Group.objects.create(
            group_name="Test Group 2",
            description="Test Description 2",
            is_approved=False,
            creator=self.user,
        )

        self.client.login(username="testuser", password="12345")


class GroupsViewTests(SetUpClass):
    def setUp(self):
        super().setUp()
        self.view_groups_url = reverse("groups")
        self.add_group_url = reverse("addGroup")
        self.view_group_url = reverse("viewGroup", kwargs={"pk": self.group1.pk})
        self.enter_group_url = reverse("enterGroup", kwargs={"pk": self.group1.pk})
        self.edit_group_url = reverse("editGroup", kwargs={"pk": self.group1.pk})
        self.delete_group_url = reverse("deleteGroup", kwargs={"pk": self.group1.pk})

    def test_view_groups_successfully(self):
        response = self.client.get(self.view_groups_url)

        self.assertTemplateUsed(response, "Groups/groups.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)
        self.assertQuerysetEqual(
            response.context["groups"],
            [f"<Group: {self.group1.group_name}>"],
            ordered=False,
        )

    def test_successfully_create_group(self):
        initial_group_count = Group.objects.count()

        response = self.client.post(
            self.add_group_url,
            {
                "group_name": "Test Group",
                "description": "Test Description",
                "featuredImage": "placeholder",
            },
        )

        self.assertEqual(Group.objects.count(), initial_group_count + 1)
        new_group = Group.objects.last()
        self.assertEqual(new_group.group_name, "Test Group")
        self.assertEqual(new_group.description, "Test Description")
        self.assertEqual(str(new_group.featuredImage), "placeholder")
        self.assertFalse(new_group.is_approved)
        self.assertEqual(new_group.creator, self.user)

    def test_view_group_successfully(self):
        response = self.client.get(self.view_group_url)

        self.assertTemplateUsed(response, "Groups/groupIndex.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["group_member"].count(),
            UserGroup.objects.filter(group_id=self.group1, user_id=self.user).count(),
        )
        self.assertEqual(
            response.context["group_user"].count(),
            UserGroup.objects.filter(group_id=self.group1, user_id=self.user).count(),
        )
        self.assertEqual(
            list(response.context["group_user"]),
            list(UserGroup.objects.filter(group_id=self.group1, user_id=self.user)),
        )

    def test_join_group_successfully(self):
        self.client.get(self.enter_group_url)

        self.assertTrue(
            UserGroup.objects.filter(user_id=self.user, group_id=self.group1).exists()
        )

    def test_leave_group_successfully(self):
        UserGroup.objects.create(user_id=self.user, group_id=self.group1)
        self.client.get(self.enter_group_url)

        self.assertFalse(
            UserGroup.objects.filter(user_id=self.user, group_id=self.group1).exists()
        )

    def test_successfully_update_group(self):
        response = self.client.post(
            self.edit_group_url,
            {
                "group_name": "Updated Test Group Name",
                "description": "Updated Test Description",
                "featuredImage": "placeholder",
            },
        )

        self.group1.refresh_from_db()
        self.assertEqual(self.group1.group_name, "Updated Test Group Name")
        self.assertEqual(self.group1.description, "Updated Test Description")
        self.assertEqual(str(self.group1.featuredImage), "placeholder")

    def test_successfully_delete_group(self):
        self.client.login(username="testuser", password="12345")
        initial_group_count = Group.objects.count()
        response = self.client.post(self.delete_group_url)

        self.assertEqual(Group.objects.count(), initial_group_count - 1)
        self.assertRaises(Group.DoesNotExist, Group.objects.get, pk=self.group1.pk)
