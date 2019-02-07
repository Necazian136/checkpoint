from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from application.models import User


class CheckpointManager:
    pass


class PlateManager:
    pass


class UserManager:

    def __init__(self):
        self.user = None

    def set_user(self, user):
        """
        Set user
        :param user:
        :return:
        """
        self.user = user

    def get_user_by_token(self, token):
        """
        Getting user by his token from database
        :param token:
        :return User|None:
        """
        try:
            user = User.objects.get(token=token)
            self.user = user
            return user
        except ObjectDoesNotExist:
            return None

    def get_user_by_username_and_password(self, username, password):
        """
        Get user by his username and password
        :param username:
        :param password:
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
            return None

    def generate_user_token(self, user=None):
        """
        Generate new token for user
        :param User user:
        :return User:
        """
        if user is None:
            user = self.user
        if isinstance(user, User):
            user.update_token()
            self.user = user
            return user
        return None
