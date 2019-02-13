from django.http import QueryDict
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from application.src.managers import *


@method_decorator(csrf_exempt, name='dispatch')
class CheckpointController(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()
        self.checkpoint_manager = CheckpointManager()

    def get(self, request, **kwargs):
        """
        Get checkpoint('s) by user
        /api/checkpoint/<str:token>/ - return all checkpoints
        /api/checkpoint/<str:token>/<str:checkpoint>/ - return specific checkpoint
        """
        user = None
        checkpoint_name = None
        result = None
        error = None

        try:
            if 'token' in kwargs:
                user = self.user_manager.get_user_by_token(kwargs['token'])

            if 'checkpoint' in kwargs:
                checkpoint_name = kwargs['checkpoint']

            if isinstance(user, User):
                if checkpoint_name is None:
                    result = self.checkpoint_manager.get_checkpoints(user)
                else:
                    checkpoint = self.checkpoint_manager.get_checkpoint_by_name(kwargs['checkpoint'], user)
                    result = self.checkpoint_manager.serialize(checkpoint)
        except Exception as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    def post(self, request, **kwargs):
        """
        Create checkpoint
        /api/checkpoint/<str:token>/<str:checkpoint>/ - create checkpoint
        """
        user = None
        checkpoint_name = None
        result = None
        error = None

        try:
            if 'token' in kwargs:
                user = self.user_manager.get_user_by_token(kwargs['token'])

            if 'checkpoint' in kwargs:
                checkpoint_name = kwargs['checkpoint']

            if isinstance(user, User) and checkpoint_name is not None:
                checkpoint = self.checkpoint_manager.create_checkpoint(checkpoint_name, user)
                result = self.checkpoint_manager.serialize(checkpoint)
            else:
                error = 'Wrong params'
        except Exception as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    # TODO: получение чекпойнта с сервера по названию
    # TODO: добавить в модель server_name для синхронизации
    def put(self, request, **kwargs):
        pass

    def patch(self, request, **kwargs):
        """
        Update checkpoint name
        /api/checkpoint/<str:token>/<str:checkpoint>/ - update checkpoint name, parameter should be in body
        /api/checkpoint/<str:token>/<str:checkpoint>/[0-1] - activate or deactivate checkpoint
        """
        user = None
        checkpoint = None
        checkpoint_name = None
        patch = QueryDict(request.body)
        result = None
        error = None

        try:
            if 'token' in kwargs:
                user = self.user_manager.get_user_by_token(kwargs['token'])

            if 'checkpoint' in kwargs:
                checkpoint = self.checkpoint_manager.get_checkpoint_by_name(kwargs['checkpoint'], user)

            if 'name' in patch:
                checkpoint_name = patch['name']

            if 'active' in kwargs:
                if kwargs['active'] == 0:
                    result = self.checkpoint_manager.deactivate(checkpoint)
                elif kwargs['active'] == 1:
                    result = self.checkpoint_manager.activate(checkpoint)

            elif isinstance(user, User) and checkpoint_name is not None:
                checkpoint = self.checkpoint_manager.update_checkpoint(checkpoint, checkpoint_name)
                result = self.checkpoint_manager.serialize(checkpoint)
        except Exception as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    # TODO спорный вопрос надо ли синхронизировать удаление
    # + того что синхронизация не нужна то что пользователь в любой момент сможет восстановить номера
    # + синхронизации только в том что не придётся удалять номера на сервере, но т.к. сервер ничего не распознаёт
    # то можно реализовать на сервере статус Используется/Не используется
    def delete(self, request, **kwargs):
        """
        Delete checkpoint
        /api/checkpoint/<str:token>/<str:checkpoint>/ - delete checkpoint
        :param request:
        :return:
        """
        user = None
        checkpoint = None
        result = None
        error = None

        try:
            if 'token' in kwargs and kwargs['token'] and kwargs['token'] != '':
                user = self.user_manager.get_user_by_token(kwargs['token'])

            if 'checkpoint' in kwargs:
                checkpoint = self.checkpoint_manager.get_checkpoint_by_name(kwargs['checkpoint'], user)

            result = self.checkpoint_manager.delete_checkpoint(checkpoint)

        except Exception as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})


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
        self.checkpoint_manager = CheckpointManager()

    def get(self, request, **kwargs):
        """
        Get user by token or request
        """
        user = None
        if 'token' not in kwargs and request.user is not None and request.user.is_active:
            user = self.user_manager.get_user_from_request(request)
        if 'token' in kwargs and kwargs['token'] and kwargs['token'] != '':
            user = self.user_manager.get_user_by_token(kwargs['token'])

        return JsonResponse({'result': self.user_manager.serialize(user)})

    def post(self, request):
        """
        Authorize user by username and password
        """
        username = None
        password = None
        user = None

        if 'username' in request.POST:
            username = request.POST.get('username')
        if 'username' in request.POST:
            password = request.POST.get('password')

        if username is not None and password is not None:
            self.user_manager.get_user_by_username_and_password(
                username=username,
                password=password
            )
            user = self.user_manager.generate_user_token()

        return JsonResponse({'result': self.user_manager.serialize(user)})

    # TODO: Получение пользователя с сервера
    def put(self, request):
        # When we get user from server we should update his token
        # to make sure person who already logged in is the same user
        # user.update_token()
        return JsonResponse({})

    # TODO: Обновление пароля
    def patch(self, request):
        return JsonResponse({})

    # TODO: Удаление пользователя по его токену
    def delete(self, request):
        return JsonResponse({})
