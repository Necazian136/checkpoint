from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    sync_counter = models.IntegerField(default=0)

    @property
    def kits(self):
        return Kit.objects.filter(user=self)

    def save(self, *args, **kwargs):
        self.sync_counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Kit(models.Model):
    name = models.CharField(max_length=63, null=False)
    sync_counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=True)

    @property
    def plates(self):
        return Plate.objects.filter(kit=self)

    def save(self, *args, **kwargs):
        self.sync_counter += 1
        if self.name != '':
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Plate(models.Model):
    name = models.CharField(max_length=15, null=False)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, null=False)
    sync_counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.sync_counter += 1
        if self.name != '':
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class History(models.Model):
    plate_name = models.CharField(max_length=15, null=False)
    plate = models.ForeignKey(Plate, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
