from django.urls import path
from .views import AudioFileView

urlpatterns = [
    path("<str:audio_type>/", AudioFileView.as_view(), name='get-post-audio'),
    path("<str:audio_type>/<int:audio_id>/", AudioFileView.as_view(), name='retrive-delete-update-audio'),
]
