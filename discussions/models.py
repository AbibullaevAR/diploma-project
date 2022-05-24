from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Discussions(models.Model):

    created_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=250,
        null=False
    )

    is_general_discussions = models.BooleanField(default=False)

    create_date = models.DateField(auto_now_add=True)

    change_date = models.DateTimeField(auto_now=True)


class Message(models.Model):

    created_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    discussion = models.ForeignKey(
        Discussions,
        on_delete=models.CASCADE
    )

    body = models.TextField()

    create_date = models.DateTimeField(auto_now_add=True)

    change_date = models.DateTimeField(auto_now=True)
