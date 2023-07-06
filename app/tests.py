from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Audio

class AudioAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_audio(self):
        return Audio.objects.create(audio_file_type='mp3', name='name', duration=120)

    def test_create_audio(self):
        import pdb;pdb.set_trace()
        url = reverse('mp3/')
        data = {
            'name': 'Test Song',
            'duration': 180,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Audio.objects.count(), 1)
        self.assertEqual(Audio.objects.get().name, 'Test Song')

   