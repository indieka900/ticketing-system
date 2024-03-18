from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse 
from services.views import viewComp, viewFeebacks,home
from accounts.models import MyUser
from services.models import Complaint, Feedback, Department

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_chair = MyUser.objects.create_user(email='chair@example.com',username='stude', password='password', role='Chair')
        self.user_student = MyUser.objects.create_user(email='student@example.com',reg_no='1234', username='chairm', password='password', role='Student')
        self.department = Department.objects.create(department_name='Test Department', department_number = 112, chairperson=self.user_chair)
        self.complaint_chair = Complaint.objects.create(sender=self.user_chair, message='Test complaint chair', department=self.department)
        self.complaint_student = Complaint.objects.create(sender=self.user_student, message='Test complaint student', department=self.department)

    def test_home_view_as_chair(self):
        request = self.factory.get(reverse('services:homepage', kwargs={'type': 'chair'}))
        request.user = self.user_chair
        response = home(request, type='chair')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test complaint chair')

    def test_home_view_as_student(self):
        request = self.factory.get(reverse('services:homepage', kwargs={'type': 'student'}))
        request.user = self.user_student
        response = home(request, type='student')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test complaint student')

    def test_home_view_redirect_unauthenticated(self):
        request = self.factory.get(reverse('services:homepage', kwargs={'type': 'chair'}))
        request.user = AnonymousUser()
        response = home(request, type='chair')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)
        
        
class ViewCompViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_chair = MyUser.objects.create_user(email='chair@example.com',username='stude', password='password', role='Chair')
        self.user_student = MyUser.objects.create_user(email='student@example.com',reg_no='1234', username='chairm', password='password', role='Student')
        self.department = Department.objects.create(department_name='Test Department', department_number = 112, chairperson=self.user_chair)
        self.complaint_chair = Complaint.objects.create(sender=self.user_chair, message='Test complaint chair', department=self.department)
        self.complaint_student = Complaint.objects.create(sender=self.user_student, message='Test complaint student', department=self.department)

    def test_view_comp_view_authenticated(self):
        request = self.factory.get(reverse('services:complaint', kwargs={'pk': self.complaint_chair.pk}))
        request.user = self.user_chair
        response = viewComp(request, pk=self.complaint_chair.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test complaint chair')

    def test_view_comp_view_unauthenticated(self):
        request = self.factory.get(reverse('services:complaint', kwargs={'pk': self.complaint_chair.pk}))
        request.user = AnonymousUser()
        response = viewComp(request, pk=self.complaint_chair.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

class ViewFeedbacksViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_chair = MyUser.objects.create_user(email='chair@example.com',username='stude', password='password', role='Chair')
        self.user_student = MyUser.objects.create_user(email='student@example.com',reg_no='1234', username='chairm', password='password', role='Student')
        self.department = Department.objects.create(department_name='Test Department', department_number = 112, chairperson=self.user_chair)
        self.complaint_chair = Complaint.objects.create(sender=self.user_chair, message='Test complaint chair', department=self.department)
        self.complaint_student = Complaint.objects.create(sender=self.user_student, message='Test complaint student', department=self.department)
        self.feedback_chair = Feedback.objects.create(sender=self.user_chair, reciever=self.user_student, complaint=self.complaint_chair, message='Test feedback')
    def test_view_feedbacks_view_authenticated(self):
        request = self.factory.get(reverse('services:feedbacks', kwargs={'pk': self.complaint_chair.pk}))
        request.user = self.user_chair
        response = viewFeebacks(request, pk=self.complaint_chair.pk)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test feedback')

    def test_view_feedbacks_view_unauthenticated(self):
        request = self.factory.get(reverse('services:feedbacks', kwargs={'pk': self.complaint_chair.pk}))
        request.user = AnonymousUser()
        response = viewFeebacks(request, pk=self.complaint_chair.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

# Create your tests here.
