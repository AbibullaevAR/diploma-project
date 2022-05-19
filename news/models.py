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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.title


class TagUserChoice(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    choice = models.BooleanField(blank=False)
