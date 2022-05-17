from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Group
# Create your models here.


class Tag(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=250)


class NewsModel(models.Model):

    created_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    tags = models.ManyToManyField(Tag)

    title = models.CharField(
        max_length=250,
        null=False
    )

    body = models.TextField()

    create_date = models.DateField(auto_now_add=True)

    change_date = models.DateTimeField(auto_now=True)
