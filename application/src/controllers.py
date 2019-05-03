from json import JSONDecodeError

from django.contrib.auth import login
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
import json

from application.src.managers import *


@method_decorator(csrf_exempt, name='dispatch')
class PlateController(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()
        self.kit_manager = KitLicensePlateManager()
        self.plate_manager = PlateManager()

    def get(self, request, **kwargs):
        """
        Get plate('s) by user and kit
        /api/plate/<str:kit>/ - return all plates of kit
        /api/plate/<str:kit>/<str:plate>/ - return specific plate
        """
        result = None
        error = None

        try:
            user = None
            kit = None
            plate_name = None
            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)

            if 'plate' in kwargs:
                plate_name = kwargs['plate'].replace(' ', '').upper()

            if isinstance(user, User) and isinstance(kit, Kit):
                if plate_name is None:
                    result = self.plate_manager.get_plates(kit)
                else:
                    plate = self.plate_manager.get_plate_by_name(plate_name, kit)
                    result = self.plate_manager.serialize(plate)

            if result is None:
                error = 'request is not valid'
        except Exception or ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    def post(self, request, **kwargs):
        """
        Create plate
        /api/plate/<str:kit>/<str:plate>/ - create plate
        """
        result = None
        error = None

        try:
            plate_name = None
            user = None
            kit = None
            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)

            if 'plate' in kwargs:
                plate_name = kwargs['plate'].replace(' ', '').upper()

            if isinstance(user, User) and isinstance(kit, Kit) and plate_name is not None:
                plate = self.plate_manager.create_plate(plate_name, kit)
                result = self.plate_manager.serialize(plate)

            if result is None:
                error = 'request is not valid'
        except Exception or ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    # TODO: получение номерного знака с сервера
    def put(self, request):
        return JsonResponse({})

    def patch(self, request, **kwargs):
        """
        Update plate name
        /api/kit/<str:kit>/<str:plate>/ - parameter should be in request
        """
        result = None
        error = None

        try:
            user = None
            kit = None
            plate = None
            plate_name = None
            try:
                patch = json.loads(request.body.decode('utf-8'))
            except JSONDecodeError:
                patch = None

            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)

            if 'plate' in kwargs:
                plate = self.plate_manager.get_plate_by_name(kwargs['plate'], kit)

            if 'plate_name' in patch:
                plate_name = patch['plate_name'].replace(' ', '').upper()

            if isinstance(user, User) and isinstance(kit, Kit):
                plate = self.plate_manager.update_plate(plate_name, plate, kit)
                result = self.plate_manager.serialize(plate)

            if result is None:
                error = 'request is not valid'
        except Exception or ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    def delete(self, request, **kwargs):
        """
        Delete plate
        /api/kit/<str:kit>/<str:plate>/ - delete plate
        :param request:
        :return:
        """
        result = None
        error = None

        try:
            user = None
            kit = None
            plate = None

            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)

            if 'plate' in kwargs:
                plate = self.plate_manager.get_plate_by_name(kwargs['plate'], kit)

            result = self.plate_manager.delete_plate(plate)

            if result is None:
                error = 'request is not valid'
        except Exception or ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})


@method_decorator(csrf_exempt, name='dispatch')
class KitController(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()
        self.kit_manager = KitLicensePlateManager()

    def get(self, request, **kwargs):
        """
        Get kit('s) by user
        /api/kit/ - return all kits
        /api/kit/<str:kit>/ - return specific kit
        """
        result = None
        error = None

        try:
            user = None
            kits_name = None

            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kits_name = kwargs['kit']

            if isinstance(user, User):
                if kits_name is None:
                    result = self.kit_manager.get_kits(user)
                else:
                    kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)
                    result = self.kit_manager.serialize(kit)

            if result is None:
                error = 'request is not valid'
        except ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    def post(self, request, **kwargs):
        """
        Create kit
        /api/kit/<str:kit>/<int:active>/ - create kit
        """
        result = None
        error = None

        try:
            user = None
            kit_name = None
            kit = None

            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit_name = kwargs['kit']

            if isinstance(user, User) and kit_name is not None:
                kit = self.kit_manager.create_kit(kit_name, user)
                result = self.kit_manager.serialize(kit)

            if 'active' in kwargs and isinstance(kit, Kit):
                if kwargs['active'] == 0:
                    result = self.kit_manager.deactivate(kit)
                elif kwargs['active'] == 1:
                    result = self.kit_manager.activate(kit)

            if result is None:
                error = 'request is not valid'
        except ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    # TODO: получение чекпойнта с сервера по названию
    # TODO: добавить в модель server_name для синхронизации
    def put(self, request, **kwargs):
        pass

    def patch(self, request, **kwargs):
        """
        Update kit name
        /api/kit/<str:kit>/ - update kit name, parameter should be in body
        /api/kit/<str:kit>/[0-1] - activate or deactivate kit
        """
        result = None
        error = None

        try:
            user = None
            kit = None
            kit_name = None
            try:
                patch = json.loads(request.body.decode('utf-8'))
            except JSONDecodeError:
                patch = None

            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)

            if patch is not None and 'kit_name' in patch:
                kit_name = patch['kit_name']

            if 'active' in kwargs:
                if kwargs['active'] == 0:
                    result = self.kit_manager.deactivate(kit)
                elif kwargs['active'] == 1:
                    result = self.kit_manager.activate(kit)

            if isinstance(user, User) and kit_name is not None and kit_name != kit.name:
                kit = self.kit_manager.update_kit(kit_name, kit, user)
                result = self.kit_manager.serialize(kit)

            if result is None:
                error = 'request is not valid'
        except ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    def delete(self, request, **kwargs):
        """
        Delete kit
        /api/kit/<str:kit>/ - delete kit
        :param request:
        :return:
        """
        result = None
        error = None

        try:
            user = None
            kit = None

            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            if 'kit' in kwargs:
                kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)

            result = self.kit_manager.delete_kit(kit)

            if result is None:
                error = 'request is not valid'
        except ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})


@method_decorator(csrf_exempt, name='dispatch')
class UserController(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()
        self.kit_manager = KitLicensePlateManager()

    def get(self, request):
        """
        Get user from request
        """
        result = None
        error = None

        try:
            user = None
            if request.user is not None and request.user.is_active:
                user = self.user_manager.get_user_from_request(request)

            result = self.user_manager.serialize(user)

        except ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    def post(self, request):
        """
        Authorize user by username and password
        """
        result = None
        error = None

        try:
            try:
                post = json.loads(request.body.decode('utf-8'))
            except JSONDecodeError:
                post = None
            username = None
            password = None
            user = None

            if 'username' in post:
                username = post['username']
            if 'password' in post:
                password = post['password']

            if username is not None and password is not None:
                user = self.user_manager.get_user_by_username_and_password(
                    username=username,
                    password=password
                )
                if user is None:
                    raise ObjectDoesNotExist('User does not exists')
                login(request, user)
            result = self.user_manager.serialize(user)
            if result is None:
                error = 'Request is not valid'
        except ObjectDoesNotExist as e:
            error = e.args[0]

        return JsonResponse({'result': result, 'error': error})

    # TODO: Получение пользователя с сервера
    def put(self, request):
        # When we get user from server we should update his token
        # to make sure person who already logged in is the same user
        # user.update_token()
        return JsonResponse({})

    # TODO: Обновление пароля
    def patch(self, request):
        return JsonResponse({})
