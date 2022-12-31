from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.
class HomepageTests(SimpleTestCase):
    def test_url_template_contains(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertContains(response, 'Witaj')
        self.assertNotContains(response, 'Żegnaj')


    def test_homepage_url_name(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)





