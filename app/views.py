import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)
from .models import Audio
from .serializers import AudioSerializer


class AudioFileNotFoundException(NotFound):
    default_detail = "Audio file not found or alreday deleted!"


class AudioFileView(generics.GenericAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def get(self, request, audio_type, audio_id=None):

        if audio_type and not audio_id:
            audio_files = self.filter_queryset(
                self.get_queryset().filter(audio_file_type=audio_type.lower())
            )
            if audio_files:
                serializer = self.get_serializer(audio_files, many=True)
                return Response({"data": serializer.data}, status=HTTP_200_OK)
            return Response(
                {"detail": "Audio file not found or records not available!."},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            audio_file = self.get_object()
            if audio_file.audio_file_type == audio_type.lower():
                serializer = self.get_serializer(audio_file)
                return Response({"data": serializer.data}, status=HTTP_200_OK)
            return Response(
                {"detail": "Audio file not found or records not available!."},
                status=HTTP_400_BAD_REQUEST,
            )

    def post(self, request, audio_type):
        request_data = json.loads(request.data.get("audioFileMetadata"))
        request_data["audio_file_type"] = audio_type.lower()

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(
            {"errors": serializer.errors}, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

    def put(self, request, audio_type, audio_id):
        request_data = json.loads(request.data.get("audioFileMetadata"))
        audio_file = self.get_object()
        if audio_file.audio_file_type != audio_type.lower():
            return Response(
                {"detail": "Audio file not found."}, status=HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(audio_file, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "detail": "Audio updated successfully!"},
                status=HTTP_200_OK,
            )
        return Response(
            {"errors": serializer.errors}, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

    def delete(self, request, audio_type, audio_id):
        audio_file = self.get_object()
        if audio_file.audio_file_type != audio_type.lower():
            return Response(
                {"detail": "Audio file not found."}, status=HTTP_400_BAD_REQUEST
            )
        audio_file.is_soft_deleted = True
        audio_file.save()
        return Response({"detail": "Audio deleted successfully!"}, status=HTTP_200_OK)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            return queryset.get(id=self.kwargs["audio_id"], is_soft_deleted=False)
        except Audio.DoesNotExist:
            raise AudioFileNotFoundException()