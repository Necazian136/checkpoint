from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    admin = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.admin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.username


class Checkpoint(models.Model):
    name = models.CharField(max_length=63, null=False, default='Unnamed')
    sync_counter = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Plate(models.Model):
    number = models.CharField(max_length=15, null=False)
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.number
