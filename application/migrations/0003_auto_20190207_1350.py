# Generated by Django 2.1.5 on 2019-02-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]