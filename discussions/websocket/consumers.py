import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User


from discussions.models import Discussions, Message


class ChatConsumer(WebsocketConsumer):
    """
    Consumer for chat logic.
    """

    def connect(self):

        discussion_id = self.scope['url_route']['kwargs']['discussion_id']

        if Discussions.objects.filter(pk=discussion_id).first():
            self.group_name = discussion_id

            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()

    def disconnect(self, code):

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """
        Handler when user send message in chat.

        :param text_data: include message body and sending user information
        :type text_data: Union[str, bytes]
        :param bytes_data:
        :return: None
        """
        text_data_json = json.loads(text_data)
        text_message = text_data_json['text_message']

        discussion_id = self.scope['url_route']['kwargs']['discussion_id']
        Message(discussion_id=discussion_id, body=text_message, created_user=self.scope['user']).save()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': text_message,
                'sending_user': text_data_json['sending_user']
            }
        )

    def chat_message(self, event):
        """
        Need for send message in all user in chat.

        :param event:
        :return: None
        """
        message = event['message']
        sending_username = event['sending_user']
        user_id = User.objects.filter(username=sending_username).first().pk

        self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'user': sending_username,
                    'user_id': user_id,
                    'date_time': datetime.now().strftime('%m.%d.%Y')
                }
            )
        )


