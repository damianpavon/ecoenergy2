from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, Organization

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Org", email="test@org.com")
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.profile = UserProfile.objects.create(user=self.user, organization=self.organization)

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.organization.name, "Test Org")

    def test_edit_profile_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/edit_profile.html')

    def test_change_password_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/change_password.html')
