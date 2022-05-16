from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Group(models.Model):

    group_name = models.CharField(
        max_length=250,
        null=False
    )


class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    avatar = models.CharField(
        max_length=250,
        default=''
    )

    class Meta:
        permissions = [('mentor', 'Mentor can control group')]
