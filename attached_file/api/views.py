from rest_framework import generics
from rest_framework import permissions

from .serializers import CreateUserFileSerializer
from attached_file.external_storage_utils import ExternalStorageManage


class CreateUserFileView(generics.CreateAPIView):
    serializer_class = CreateUserFileSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    created_instance = None

    def perform_create(self, serializer):
        self.created_instance = serializer.save(created_user=self.request.user)

    def get_success_headers(self, data):
        headers = super().get_success_headers(data)
        ext_manage = ExternalStorageManage()
        headers['Upload_URL'] = ext_manage.get_upload_link(
            str(self.created_instance.pk) + self.created_instance.file_name
        )
        return headers

