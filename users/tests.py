from django.test import TestCase
from django.urls import reverse, resolve
import pytest
from django.contrib.auth import get_user_model

from users.forms import CustomUserCreationForm
from .views import RegistrationUserView


@pytest.mark.django_db
class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='Test123', email='test@test.pl', password="testpass123")
        self.assertEqual(user.username, 'Test123')
        self.assertEqual(user.email, 'test@test.pl')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='superuser', email='supertest@test.pl',
                                                   password="testpass123")
        self.assertEqual(admin_user.username, 'superuser')
        self.assertEqual(admin_user.email, 'supertest@test.pl')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class RegistrationTests(TestCase):
    def setUp(self):
        url = reverse('users:registration')
        self.response = self.client.get(url)

    def test_registration_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "registration/registration.html")
        self.assertContains(self.response, "Rejestracja")
        self.assertNotContains(self.response, "Coś czego tu nie ma")

    def test_registration_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_registration_view(self):  # new
        view = resolve("/users/registration/")
        self.assertEqual(view.func.__name__, RegistrationUserView.as_view().__name__)

