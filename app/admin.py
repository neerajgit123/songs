from django.contrib import admin
from .models import Audio

# Register your models here.
class DeleteRequestMixin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(is_soft_deleted=False)
        return queryset


@admin.register(Audio)
class AudioAdmin(DeleteRequestMixin):
    list_display = ["name", "audio_file_type", "duration"]
    exclude = ["is_soft_deleted"]
