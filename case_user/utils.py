from .exceptions import NotLoggedInException, UnAuthorized
from django.http import request, JsonResponse
from .models import User, Client, UserType


def check_logged_in(request: request.HttpRequest):
    if not request.user.is_authenticated:
        raise NotLoggedInException("user not loggedin")


def check_internal(request: request.HttpRequest):
    if not request.user.is_authenticated and request.user.client.name != 'admin':
        raise UnAuthorized("user unauthorized")


def check_admin(request: request.HttpRequest):
    check_logged_in(request)
    user: User = request.user
    client: Client = user.client
    # TODO using hardcoded
    if UserType(user.user_type) != UserType.ADMIN_USER or client.name != 'admin':
        raise UnAuthorized("unauthentecated request")


def bad_response(msg: str):
    return JsonResponse({"message": msg}, status=400)


def permission_dec(allowed_permissions=[UserType.CLIENT_USER], exclude=[]):
    def wrapper(func):
        def act(request, *args, **kwargs):
            if len(exclude) != 0 and request.user.user_type in exclude:
                return JsonResponse({"message": "unauthorized"}, status=401)
            if len(allowed_permissions) != 0 and request.user.user_type in allowed_permissions:
                return func(request, *args, **kwargs)
            return JsonResponse({"message": "unauthorized"}, status=401)
        return act
    return wrapper
