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
            checkpoint = Checkpoint.objects.get(name=name, user=user)
            self.checkpoint = checkpoint
            return checkpoint
        except ObjectDoesNotExist:
            raise Exception('Checkpoint does not exists')

    def set_checkpoint(self, checkpoint: Checkpoint):
        """
        Set checkpoint
        :param Checkpoint checkpoint:
        :return:
        """
        self.checkpoint = checkpoint

    def serialize(self, checkpoint: Checkpoint = None):
        """
        Return dict from object
        :param checkpoint:Checkpoint
        :return:dict|None
        """
        if checkpoint is None:
            checkpoint = self.checkpoint
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
        if self._checkpoint_is_unique(checkpoint):
            checkpoint.save()
            self.checkpoint = checkpoint
            return checkpoint
        raise Exception('Checkpoint with this name already exists')

    @staticmethod
    def _checkpoint_is_unique(checkpoint: Checkpoint):
        if len(Checkpoint.objects.filter(name=checkpoint.name)) == 0:
            return True
        return False

    def update_checkpoint(self, checkpoint: Checkpoint, data):
        """
        Update name of checkpoint
        :param data:
        :param Checkpoint checkpoint:
        :return Checkpoint|None:
        """

        if isinstance(checkpoint, Checkpoint):
            if 'name' in data:
                checkpoint.name = data['name']
            if self._checkpoint_is_unique(checkpoint):
                checkpoint.save()
                self.checkpoint = checkpoint
                return checkpoint
            raise Exception('Checkpoint with this name already exists')
        return

    def delete_checkpoint(self, checkpoint: Checkpoint):
        """
        Delete checkpoint from user
        :param checkpoint:
        :return bool:
        """
        checkpoint.delete()
        self.checkpoint = None
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
                'checkpoint': plate.checkpoint.name,
                'number': plate.number
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
                'token': user.token
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
        Getting user by his token from database
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
