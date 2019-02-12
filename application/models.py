from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib


class User(AbstractUser):
    admin = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True, default=None)

    @property
    def is_admin(self):
        return self.admin

    @property
    def checkpoints(self):
        checkpoints = Checkpoint.objects.filter(user=self)
        return checkpoints

    def update_token(self):
        h = hashlib.new('ripemd160')
        if self.token is None:
            h.update(self.username.encode('utf-8'))
            self.token = h.hexdigest()
        else:
            h.update(self.token.encode('utf-8'))
            self.token = h.hexdigest()
        self.save()
        return self.token

    def __str__(self):
        return self.username


class Checkpoint(models.Model):
    name = models.CharField(max_length=63, null=False, default='Unnamed')
    sync_counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=False)

    @property
    def plates(self):
        return Plate.objects.filter(checkpoint=self)

    def set_active(self):
        self.objects.all().update(is_active=False)
        self.is_active = True
        self.save()

    def __str__(self):
        return self.name


class Plate(models.Model):
    number = models.CharField(max_length=15, null=False)
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.number
