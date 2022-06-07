from django.conf import settings
import requests


class ExternalStorageManage:
    headers = {
        'Accept': 'application/json',
        'Authorization': f'OAuth {settings.EXTERNAL_STORAGE_TOKEN}'
    }

    action = {
        'upload_file': 'https://cloud-api.yandex.net/v1/disk/resources/upload?path=',
        'download_file': 'https://cloud-api.yandex.net/v1/disk/resources/download?path='
    }

    def get_upload_link(self, file_name: str):

        request_json = requests.get(
            url=self.action['upload_file'] + file_name,
            headers=self.headers
        ).json()
        return request_json['href']

    def get_download_link(self, file_name):

        request_json = requests.get(
            url=self.action['download_file'] + file_name,
            headers=self.headers
        ).json()
        return request_json['href']
