from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .external_storage_utils import ExternalStorageManage
from .models import UserFiles

# Create your views here.


class UserFileDetailView(LoginRequiredMixin, DetailView):
    """
    Return download link for chosen file.
    """
    model = UserFiles

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        ext_manage = ExternalStorageManage()
        redir_link = ext_manage.get_download_link(str(obj.pk)+obj.file_name)
        return redirect(redir_link)
