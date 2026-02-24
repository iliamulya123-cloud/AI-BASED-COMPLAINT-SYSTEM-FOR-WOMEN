from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Complaint


class ComplaintFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='StrongPass123!', email='u@test.com')

    def test_submit_complaint(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.post(reverse('submit_complaint'), {
            'incident_type': Complaint.IncidentType.HARASSMENT,
            'location': 'Central Park',
            'incident_time': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'description': 'Detailed incident report',
            'evidence_notes': 'Photo evidence available',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Complaint.objects.count(), 1)
