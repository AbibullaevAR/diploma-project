from django.urls.base import reverse
from rest_framework import generics
from rest_framework import permissions

from .serializers import CreateUserFileSerializer
from attached_file.external_storage_utils import ExternalStorageManage


class CreateUserFileView(generics.CreateAPIView):
    """
    API View for create new file.

    :ivar created_instance: UserFile instance created after save serializer.
    :type created_instance: model UserFile
    """

    serializer_class = CreateUserFileSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    created_instance = None

    def perform_create(self, serializer):
        self.created_instance = serializer.save(created_user=self.request.user)

    def get_success_headers(self, data):
        """
        Overwrite super class method. Add in success headers:
        `Upload_URL` link for upload created file.
        `download_link` link for download created file

        :param data:
        :return: headers
        """
        headers = super().get_success_headers(data)
        file_name = str(self.created_instance.pk) + self.created_instance.file_name
        ext_manage = ExternalStorageManage()
        headers['Upload_URL'] = ext_manage.get_upload_link(
            file_name
        )
        headers['download_link'] = reverse('attached_file:download_file', kwargs={'pk': self.created_instance.pk})
        return headers

