from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    admin = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.admin


class Checkpoint(models.Model):
    name = models.CharField(max_length=63, null=True)
    ip = models.CharField(max_length=21, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    sync_counter = models.IntegerField(default=0)


class Plate(models.Model):
    number = models.CharField(max_length=15, null=False)
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, null=False)

