from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from application.src.managers import *


@method_decorator(csrf_exempt, name='dispatch')
class CheckpointController(View):
    def get(self, request):
        """
        Get checkpoint by user
        """
        return JsonResponse({})

    def post(self, request):
        return JsonResponse({})

    def put(self, request):
        return JsonResponse({})

    def delete(self, request):
        return JsonResponse({})


@method_decorator(csrf_exempt, name='dispatch')
class PlateController(View):
    def get(self, request):
        return JsonResponse({})

    def post(self, request):
        return JsonResponse({})

    def put(self, request):
        return JsonResponse({})

    def delete(self, request):
        return JsonResponse({})


@method_decorator(csrf_exempt, name='dispatch')
class UserController(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()

    def get(self, request, **kwargs):
        """
        Get user by token or request
        """
        user = None
        if 'token' not in kwargs and request.user is not None and request.user.is_active:
            user = request.user

        if 'token' in kwargs and kwargs['token'] and kwargs['token'] != '':
            user = self.user_manager.get_user_by_token(kwargs['token'])
        if isinstance(user, User):
            return JsonResponse({'result': {
                'username': user.username,
                'is_admin': user.is_admin,
                'token': user.token,
            }})
        return JsonResponse({'result': None})

    def post(self, request):
        """
        Authorize user by username and password
        """
        username = None
        password = None
        user = None
        if 'username' in request.POST:
            username = request.POST['username']
        if 'username' in request.POST:
            password = request.POST['password']

        if username is not None and password is not None:
            self.user_manager.get_user_by_username_and_password(
                username=username,
                password=password
            )
            user = self.user_manager.generate_user_token()
        if isinstance(user, User):
            return JsonResponse({'result': {
                'username': user.username,
                'is_admin': user.is_admin,
                'token': user.token,
            }})
        return JsonResponse({'result': None})

    # TODO: Получение пользователя с сервера
    def put(self, request):
        return JsonResponse({})

    # TODO: Обновление пароля
    def patch(self, request):
        return JsonResponse({})

    # TODO: Удаление пользователя по его токену
    def delete(self, request):
        return JsonResponse({})
