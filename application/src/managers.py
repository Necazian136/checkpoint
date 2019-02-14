from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from application.models import *


class CheckpointManager:
    def __init__(self):
        self.checkpoint = None

    def get_checkpoints(self, user: User):
        checkpoint_list = []
        for checkpoint in user.checkpoints:
            checkpoint_list.append(self.serialize(checkpoint))
        return checkpoint_list

    def get_checkpoint_by_name(self, name, user: User):
        """
        :param name:
        :param user:
        :except Exception
        :return:
        """
        try:
            return Checkpoint.objects.get(name=name, user=user)
        except ObjectDoesNotExist:
            raise Exception('Checkpoint does not exists')

    def set_checkpoint(self, checkpoint: Checkpoint):
        """
        Set checkpoint
        :param Checkpoint checkpoint:
        :return:
        """
        self.checkpoint = checkpoint

    def serialize(self, checkpoint: Checkpoint):
        """
        Return dict from object
        :param checkpoint:Checkpoint
        :return:dict|None
        """
        if isinstance(checkpoint, Checkpoint):
            return {
                'name': checkpoint.name,
                'user': checkpoint.user.username,
                'active': checkpoint.is_active,
                'sync_counter': checkpoint.sync_counter,
            }
        return

    def create_checkpoint(self, name, user: User):
        """
        :param name:
        :param user:
        :except Exception
        :return Checkpoint:
        """
        checkpoint = Checkpoint(name=name, user=user)
        if self.__checkpoint_is_unique(checkpoint, user):
            checkpoint.save()
            return checkpoint
        raise Exception('Checkpoint with this name already exists')

    @staticmethod
    def __checkpoint_is_unique(checkpoint: Checkpoint, user: User):
        if len(Checkpoint.objects.filter(name=checkpoint.name, user=user)) == 0:
            return True
        return False

    def update_checkpoint(self, name, checkpoint: Checkpoint, user: User):
        """
        Update name of checkpoint
        :param name:
        :param Checkpoint checkpoint:
        :return Checkpoint|None:
        """
        checkpoint.name = name
        if self.__checkpoint_is_unique(checkpoint, user):
            checkpoint.save()
            return checkpoint
        raise Exception('Checkpoint with this name already exists')

    def activate(self, checkpoint: Checkpoint):
        checkpoint.set_active()
        return True

    def deactivate(self, checkpoint):
        checkpoint.is_active = False
        checkpoint.save()
        return True

    def delete_checkpoint(self, checkpoint: Checkpoint):
        """
        Delete checkpoint from user
        :param checkpoint:
        :return bool:
        """
        checkpoint.delete()
        return True


class PlateManager:
    def __init__(self):
        self.plate = None
        self.error = None

    def get_plates(self, checkpoint: Checkpoint):
        checkpoint_list = []
        for plate in checkpoint.plates:
            checkpoint_list.append(self.serialize(plate))
        return checkpoint_list

    def get_plate_by_name(self, name, checkpoint: Checkpoint):
        try:
            return Plate.objects.get(name=name, checkpoint=checkpoint)
        except ObjectDoesNotExist:
            raise Exception('Plate does not exists')

    def create_plate(self, name, checkpoint: Checkpoint):
        plate = Plate(name=name, checkpoint=checkpoint)
        if self.__plate_is_unique(plate, checkpoint):
            plate.save()
            return plate
        raise Exception('Plate already exists')

    def update_plate(self, name, plate: Plate, checkpoint: Checkpoint):
        plate.name = name
        if self.__plate_is_unique(plate, checkpoint):
            plate.save()
            return plate
        raise Exception('Plate with this name already exists')

    def delete_plate(self, plate: Plate):
        plate.delete()
        return True

    @staticmethod
    def __plate_is_unique(plate: Plate, checkpoint: Checkpoint):
        if len(Plate.objects.filter(name=plate.name, checkpoint=checkpoint)) == 0:
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
                'checkpoint': plate.checkpoint.name,
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
                'is_admin': user.is_admin,
                'token': user.token,
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

    def get_user_by_token(self, token: str):
        """
        Getting user by his token from database
        :except Exception
        :param str token:
        :return User|None:
        """
        try:
            self.user = User.objects.get(token=token)
            return self.user
        except ObjectDoesNotExist:
            raise Exception('User does not exists')

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
            self.user = user
            return user
        except ObjectDoesNotExist:
            return

    def generate_user_token(self, user: User = None):
        """
        Generate new token for user
        :param User user:
        :return User|None:
        """
        if user is None:
            user = self.user
        if isinstance(user, User):
            if user.token is None:
                user.update_token()
            self.user = user
            return user
        return
