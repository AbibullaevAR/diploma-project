from django.db import models
from django.contrib.auth import get_user_model

from discussions.models import Discussions


# Create your models here.
class UserFiles(models.Model):

    discussion = models.ForeignKey(
        Discussions,
        on_delete=models.CASCADE
    )
    created_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    file_name = models.CharField(max_length=250, null=False)

    create_date = models.DateField(auto_now_add=True)
