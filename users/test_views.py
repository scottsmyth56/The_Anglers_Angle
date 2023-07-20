from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import User
from .forms import RegistrationForm, LoginForm, EditUserForm, ResetPasswordForm


class SetUpClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345",
            "password2": "12345",
        }

        self.client.login(username="testuser", password="12345")
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.edit_profile_url = reverse("editProfile")
        self.view_profile_url = reverse(
            "profile", kwargs={"username": self.user.username}
        )
        self.change_password_url = reverse("change_password")


class RegistrationViewTest(SetUpClass):
    def setUp(self):
        super().setUp()

    def test_register_new_user_successfully(self):
        response = self.client.post(
            self.register_url, self.user_data, format="text/html"
        )
        user = User.objects.filter(username=self.user_data["username"])
        if not user.exists():
            form = RegistrationForm(self.user_data)
            print(form.errors)
        self.assertTrue(user.exists())

    def test_user_can_log_in_with_correct_credentials(self):
        response = self.client.post(self.login_url, self.user_data, follow=True)
        user = get_user_model().objects.get(username=self.user_data["username"])

        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_successfully_view_profile(self):
        response = self.client.get(self.view_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Auth/profile.html")

    def test_successfully_change_password(self):
        response = self.client.post(
            self.change_password_url,
            {
                "current_password": "12345",
                "new_password": "newpassword123",
                "confirm_new_password": "newpassword123",
            },
        )

        self.user.refresh_from_db()
        self.client.login(username="testuser", password="newpassword123")
        self.assertTrue(self.user.check_password("newpassword123"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("profile", kwargs={"username": self.user.username})
        )

    def test_change_password_non_matching_new_passwords(self):
        response = self.client.post(
            self.change_password_url,
            {
                "old_password": "12345",
                "new_password1": "newpassword123",
                "new_password2": "newpassword321",
            },
        )
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("newpassword123"))
        self.assertTrue(self.user.check_password("12345"))
        self.assertEqual(response.status_code, 200)

    def test_change_password_incorrect_current_password(self):
        response = self.client.post(
            self.change_password_url,
            {
                "old_password": "wrongpassword",
                "new_password1": "newpassword123",
                "new_password2": "newpassword123",
            },
        )
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("newpassword123"))
        self.assertTrue(self.user.check_password("12345"))
        self.assertEqual(response.status_code, 200)
