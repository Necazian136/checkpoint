from django.db import models
from django.contrib.auth.models import AbstractUser


class Checkpoint(models.Model):
    name = models.CharField(max_length=63, null=False, default='Unnamed')
    sync_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(AbstractUser):
    admin = models.BooleanField(default=False)
    checkpoint = models.OneToOneField(Checkpoint, on_delete=models.CASCADE, null=True)

    @property
    def is_admin(self):
        return self.admin


class Plate(models.Model):
    number = models.CharField(max_length=15, null=False)
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.number

