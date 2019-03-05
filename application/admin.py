# TODO: удалить когда сервер будет готов

from django.contrib import admin
from application.models import User, Kit, Plate


admin.site.register(User)
admin.site.register(Kit)
admin.site.register(Plate)
