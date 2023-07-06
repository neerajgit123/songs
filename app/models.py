from django.db import models

# Create your models here.
class Audio(models.Model):
    AUDIO_TYPE = (
        ('mp3', 'MP3'),
        ('wav', 'WAV'),
        ('amr', 'AMR'),
        ('wma', 'WMA'),  
    )
    name = models.CharField(max_length=100)
    audio_file_type = models.CharField(max_length=100, choices=AUDIO_TYPE)
    duration = models.PositiveIntegerField()
    is_soft_deleted = models.BooleanField(default=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_upload_time = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.audio_file_type}'    
