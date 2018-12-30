from django.db import models


class User(models.Model):
    login = models.CharField(max_length=63)
    password = models.CharField(max_length=63)
    token = models.CharField(max_length=63, default=None, null=True)


class Checkpoint(models.Model):
    name = models.CharField(max_length=63, null=True)
    ip = models.CharField(max_length=21, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Plate(models.Model):
    number = models.CharField(max_length=15, null=False)
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, null=False)


class Synchronization(models.Model):
    counter = models.IntegerField()
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, null=False)
