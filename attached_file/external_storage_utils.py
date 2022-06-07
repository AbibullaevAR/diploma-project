from django.conf import settings
import requests


def get_upload_link(file_id):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'OAuth {settings.EXTERNAL_STORAGE_TOKEN}'
    }
    request_json = requests.get(
        url=f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={file_id}',
        headers=headers
    ).json()
    return request_json['href']
