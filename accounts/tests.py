from django.test import TestCase, Client
from django.urls import reverse
from .models import MyUser

class LoginRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_student = MyUser.objects.create_user(
            email='student@example.com',
            username = 'stuuser',
            reg_no='1234',
            password='password',
            role='Student'
        )
        self.user_chair = MyUser.objects.create_user(
            email='chair@example.com',
            username = 'chairuser',
            password='password',
            role='Chair'
        )

    def test_login_student(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': 'student@example.com',
            'reg_no': '1234',
            'password': 'password',
            'students': 'students'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/home/student/'))
        self.assertEqual(response.wsgi_request.user.email, 'student@example.com')

    def test_login_chair(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': 'chair@example.com',
            'password': 'password',
            'chair': 'chair'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/home/chair/'))
        self.assertEqual(response.wsgi_request.user.email, 'chair@example.com')

    def test_invalid_login(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': 'invalid@example.com',
            'password': 'password',
            'students': 'students'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:login'))

    def test_registration(self):
        response = self.client.post(reverse('accounts:sign-up'), {
            'email': 'newuser@example.com',
            'reg_no': '5678',
            'username': 'Joseph',
            'password1': 'password',
            'password2': 'password',
            'role': 'Student'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MyUser.objects.filter(email='newuser@example.com').exists())

        # Additional tests for chair registration can be added similarly

    def test_invalid_registration(self):
        response = self.client.post(reverse('accounts:sign-up'), {
            'email': 'invalidemail.com',
            'reg_no': '5678',
            'password1': 'password',
            'password2': 'password',
            'role': 'Student'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFalse(MyUser.objects.filter(email='invalidemail.com').exists())

        # Additional tests for other invalid cases can be added


# Create your tests here.
