from rest_framework import generics
from rest_framework import permissions

from .serializers import CreateUserFileSerializer
from attached_file.external_storage_utils import get_upload_link


class CreateUserFileView(generics.CreateAPIView):
    serializer_class = CreateUserFileSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    created_instance = None

    def perform_create(self, serializer):
        self.created_instance = serializer.save(created_user=self.request.user)

    def get_success_headers(self, data):
        headers = super().get_success_headers(data)
        headers['Upload_URL'] = get_upload_link(self.created_instance.pk)
        return headers

