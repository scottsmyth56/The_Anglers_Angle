from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, User, Like, Comment, Competition, CompetitionUser
from django.shortcuts import get_object_or_404


class SetUpClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")


class ViewCompetitionsTest(SetUpClass):
    def setUp(self):
        super().setUp()
        self.competition = Competition.objects.create(
            title="Test Competition",
            location="Test Location",
            description="Test Description",
            category="Test Category",
            date="2023-07-20 00:00:00",
            creator=self.user,
        )
        self.view_competition_detail_url = reverse(
            "viewCompetitionDetailed", kwargs={"pk": self.competition.pk}
        )
        self.edit_competition_url = reverse(
            "editCompetition", kwargs={"pk": self.competition.pk}
        )
        self.delete_competition_url = reverse(
            "deleteCompetition", kwargs={"pk": self.competition.pk}
        )

        self.enter_competition_url = reverse(
            "enterCompetition", kwargs={"pk": self.competition.pk}
        )
        self.delete_competition_url = reverse(
            "deleteCompetition", kwargs={"pk": self.competition.pk}
        )
        self.view_competitions_url = reverse("competitions")
        self.add_competition_url = reverse("addCompetition")

    def test_view_competitions_successfully(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.view_competitions_url)
        self.assertTemplateUsed(response, "Competitions/competitions.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(list(response.context["competitions"]), [self.competition])

    def test_successfully_create_competition(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            self.add_competition_url,
            {
                "title": "Test Title",
                "location": "Test Location",
                "description": "Test Description",
                "category": "Test Category",
                "date": "2023-07-23 13:00:00",
                "featuredImage": "placeholder",
            },
        )

        self.assertEqual(Competition.objects.count(), 2)
        self.assertEqual(Competition.objects.last().title, "Test Title")

    def test_view_competition_detail_successfully(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.view_competition_detail_url)
        self.assertTemplateUsed(response, "Competitions/competition_detail.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["competition_user"].count(), 0)
        self.assertEqual(response.context["registered_users"].count(), 0)

    def test_successfully_edit_competition(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            self.edit_competition_url,
            {
                "title": "Updated Test Title",
                "location": "Updated Test Location",
                "description": "Updated Test Description",
                "category": "Updated Test Category",
                "date": "2023-07-23 13:00:00",
                "featuredImage": "placeholder",
            },
        )

        self.competition.refresh_from_db()
        self.assertEqual(self.competition.title, "Updated Test Title")
        self.assertEqual(self.competition.location, "Updated Test Location")
        self.assertEqual(self.competition.description, "Updated Test Description")
        self.assertEqual(self.competition.category, "Updated Test Category")

    def test_successfully_delete_competition(self):
        self.client.login(username="testuser", password="12345")
        initial_competition_count = Competition.objects.count()
        response = self.client.post(self.delete_competition_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Competition.objects.count(), initial_competition_count - 1)
        with self.assertRaises(Competition.DoesNotExist):
            Competition.objects.get(pk=self.competition.pk)

    def test_successfully_enter_competition(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.enter_competition_url)

        competition_user_exists = CompetitionUser.objects.filter(
            user_id=self.user, competition_id=self.competition
        ).exists()

        self.assertTrue(competition_user_exists)

    def test_successfully_leave_competition(self):
        CompetitionUser.objects.create(
            user_id=self.user, competition_id=self.competition
        )

        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.enter_competition_url)

        competition_user_exists = CompetitionUser.objects.filter(
            user_id=self.user, competition_id=self.competition
        ).exists()

        self.assertFalse(competition_user_exists)
