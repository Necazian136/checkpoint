from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from application.models import *


class KitLicensePlateManager:
    def __init__(self):
        self.kit = None

    def get_kits(self, user: User):
        kit_list = []
        for kit in user.kits:
            kit_list.append(self.serialize(kit))
        return kit_list

    def get_kit_by_name(self, name, user: User):
        """
        :param name:
        :param user:
        :except Exception
        :return:
        """
        try:
            return Kit.objects.get(name=name, user=user)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('Kit does not exists')

    def set_kit(self, kit: Kit):
        """
        Set kit
        :param Kit kit:
        :return:
        """
        self.kit = kit

    def serialize(self, kit: Kit):
        """
        Return dict from object
        :param kit:Kit
        :return:dict|None
        """
        if isinstance(kit, Kit):
            return {
                'name': kit.name,
                'user': kit.user.username,
                'active': kit.is_active,
                'sync_counter': kit.sync_counter,
            }
        return

    def create_kit(self, name, user: User):
        """
        :param name:
        :param user:
        :except Exception
        :return Kit:
        """
        kit = Kit(name=name, user=user)
        if self.__kit_is_unique(kit, user):
            kit.save()
            return kit
        raise ObjectDoesNotExist('Kit with this name already exists')

    def __kit_is_unique(self, kit: Kit, user: User):
        if len(Kit.objects.filter(name=kit.name, user=user)) == 0:
            return True
        return False

    def update_kit(self, name, kit: Kit, user: User):
        """
        Update name of kit
        :param user:
        :param name:
        :param Kit kit:
        :return KitLicensePlate|None:
        """
        kit.name = name
        if self.__kit_is_unique(kit, user):
            kit.save()
            return kit
        raise ObjectDoesNotExist('Kit with this name already exists')

    def activate(self, kit: Kit):
        kit.is_active = True
        kit.save()
        return True

    def deactivate(self, kit):
        kit.is_active = False
        kit.save()
        return True

    def get_active_kits(self):
        return Kit.objects.filter(active=True)

    def delete_kit(self, kit: Kit):
        """
        Delete kit from user
        :param kit:
        :return bool:
        """
        kit.delete()
        return True


class PlateManager:
    def __init__(self):
        self.plate = None
        self.error = None

    def get_plates(self, kit: Kit):
        kit_list = []
        for plate in kit.plates:
            kit_list.append(self.serialize(plate))
        return kit_list

    def get_plate_by_name(self, name, kit: Kit):
        try:
            return Plate.objects.get(name=name, kit=kit)
        except ObjectDoesNotExist:
            raise Exception('Plate does not exists')

    def create_plate(self, name, kit: Kit):
        plate = Plate(name=name, kit=kit)
        if self.__plate_is_unique(plate, kit):
            plate.save()
            return plate
        raise Exception('Plate already exists')

    def update_plate(self, name, plate: Plate, kit: Kit):
        plate.name = name
        if self.__plate_is_unique(plate, kit):
            plate.save()
            return plate
        raise Exception('Plate with this name already exists')

    def delete_plate(self, plate: Plate):
        plate.delete()
        return True

    def __plate_is_unique(self, plate: Plate, kit: Kit):
        if len(Plate.objects.filter(name=plate.name, kit=kit)) == 0:
            return True
        return False

    def serialize(self, plate: Plate = None):
        """
        Return dict from object
        :param plate:Plate
        :return:dict|None
        """
        if plate is None:
            plate = self.plate
        if isinstance(plate, Plate):
            return {
                'name': plate.name,
                'kit': plate.kit.name,
            }
        return


class UserManager:

    def __init__(self):
        self.user = None

    def serialize(self, user: User = None):
        """
        Return dict from object
        :param User user:
        :return dict|None:
        """
        if user is None:
            user = self.user

        if isinstance(user, User):
            return {
                'username': user.username,
                'sync_counter': user.sync_counter,
            }
        return

    def set_user(self, user: User):
        """
        Set user
        :param User user:
        :return:
        """
        self.user = user

    def get_user_from_request(self, request):
        """
        Getting user from request
        :param request:
        :return User|None:
        """
        self.user = request.user
        return self.user

    def get_user_by_username_and_password(self, username: str, password: str):
        """
        Get user by his username and password
        :param str username:
        :param str password:
        :return User|None:
        """
        try:
            user = authenticate(
                username=username,
                password=password
            )
            return user
        except ObjectDoesNotExist:
            return
