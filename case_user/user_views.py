import json
import logging

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import request
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views import View

from .base_view import JsonView, OnlyLoggedIn
from .exceptions import BadRequest
from .models import Client, User, UserType
from .utils import bad_response, check_admin, permission_dec

logger = logging.getLogger(__name__)


# Create your views here.

# USERNAME_VALIDATOR = validators.RegexValidator(
#     regex=r"^[a-z0-9_-]+$",
#     message="Username can only contain lowercase letters, numbers, "
#             "underscores and hyphens."
# )
# PASSWORD_VALIDATOR = validators.RegexValidator(
#     regex=r"^.*(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!$#*&]).*$",
#     message="Password needs to contain at least (a) One lower case letter (b) "
#             "One Upper case letter and (c) One number (d) One of the following"
#             " special characters - !@#$&*"
# )


# decorator could be better option


class WhoAmI(OnlyLoggedIn):
    def get(self, request: request.HttpRequest):
        return JsonResponse(
            self.user.get_dict(), status=200)


class Logout(View):

    def get(self, request: request.HttpRequest):
        logout(request)
        return HttpResponseRedirect("/")


class LoginView(View):

    def post(self, request: request.HttpRequest):
        try:
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user = User.objects.get(
                    username=username)
                if check_password(password, user.password) and user.is_active and user.client.is_active:
                    login(request, user)
                    return JsonResponse(
                        {"success": True, }, status=200)
            return JsonResponse({"success": False, "message": "usernaame and password not matching "}, status=401)
        except KeyError:
            return JsonResponse(
                {"success": False, "message": "both username and password are required for this request"}, status=401)
        except Exception as e:
            logger.warn(f"ran into exception {e}")
            return JsonResponse(
                {"success": False, "message": "Unknown error"}, status=401)


# self
class ChangePassword(OnlyLoggedIn, JsonView):

    # creates new user
    # according to params
    def post(self, request: request.HttpRequest):
        user: User = request.user
        json_data = self.json(request)
        current_password = json_data.get('current_password', None)
        password = json_data.get('password', None)
        confirm_password = json_data.get('confirm_password', None)
        try:
            if (password and
                    confirm_password == password and
                    check_password(current_password, user.password) and
                    # validate_password(password) # TODO need to validate password comes with current terms
                    True
                    ):
                user.password = make_password(password)
                # TODO
                # after saving password, its logging out current user
                # need to check that
                user.save(update_fields=['password'])
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": True}, status=400)
        except:
            pass
        raise BadRequest("user doesnt exist")


# self
class NotifyEmails(OnlyLoggedIn, JsonView):

    # creates new user
    # according to params
    def post(self, request: request.HttpRequest):
        user: User = request.user
        notify = self.json(request).get('notify')
        if notify is not None and notify != user.notify:
            user.notify = notify
            user.save(update_fields=['notify'])
            return JsonResponse({"success": True})
        raise BadRequest(
            "notify param is required (or) user notify settings is already applied")


class SettingOtherUserNotifyEmail(OnlyLoggedIn, JsonView):

    # creates new user
    # according to params
    @permission_dec([UserType.ADMIN_USER])
    def post(self, request: request.HttpRequest, user_id: int):
        notify = self.json(request).get('notify', None)
        try:
            user = User.objects.get(uesr_id=user_id)
            if notify is not None and notify != user.notify:
                user.notify = notify
                user.save(update_fields=['notify'])
                return JsonResponse({"success": True})
            return bad_response("bad params")
        except:
            return bad_response("user doesn't exist")


# other
class ActivateUser(OnlyLoggedIn, JsonView):

    # creates new user
    # according to params
    @permission_dec([UserType.ADMIN_USER])
    def post(self, request: request.HttpRequest, user_id: int):
        try:
            user: User = User.objects.get(user_id=user_id)
            activate = self.json(request).get('activate')
            if activate is not None and activate != user.is_active:
                user.is_active = activate
                user.save(update_fields=['is_active'])
                return JsonResponse({"success": True})
            return bad_response("activate param is required (or) user activate settings is already applied")
        except:
            return JsonResponse({}, status=500)


class MakeAdmin(OnlyLoggedIn, JsonView):

    # creates new user
    # according to params
    @permission_dec([UserType.ADMIN_USER])
    def post(self, request: request.HttpRequest, user_id: int):
        try:
            make_admin = self.json(request).get('make_admin', True)
            user = User.objects.get(user_id=user_id)
            if user.client.name == 'admin':
                user.user_type = UserType.ADMIN_USER if make_admin else UserType.INTERNAL_USER
                user.save()
                return JsonResponse({"success": True})
            else:
                raise BadRequest("user from non admin client")
        except:
            raise BadRequest("user doesnt exist")


def update_user(json_data, user):
    if 'name' in json_data:
        # TODO check name
        user.name = json_data.get('name')
    if 'email' in json_data:
        # TODO send email verify email
        user.email = json_data.get('email')
    if 'phone_number' in json_data:
        # TODO check phone number
        user.phone_number = json_data.get('phone_number')
    if 'address' in json_data:
        user.address = json_data.get('address')
    user.save()


class UpdateUserAdmin(OnlyLoggedIn, JsonView):
    @permission_dec([UserType.ADMIN_USER])
    def patch(self, request):
        json_data = self.json(request)
        try:
            user = User.objects.get(user_id=json_data.get('user_id'))
            update_user(json_data, user)
            return JsonResponse(user.get_dict())
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")
        except Exception as e:
            # TODO could not be e
            return bad_response(f"client does not exist {e}")


class UserApis(OnlyLoggedIn, JsonView):

    def patch(self, request: request.HttpRequest):
        json_data = self.json(request)
        try:
            user = request.user
            update_user(json_data, user)
            return JsonResponse(user.get_dict())
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")
        except Exception as e:
            # TODO could not be e
            return bad_response(f"client does not exist {e}")

    # creates new user
    # according to params

    @permission_dec([UserType.ADMIN_USER])
    def post(self, request: request.HttpRequest):
        json_data = self.json(request)
        try:
            client_id = json_data.get('client_id', 1)
            if client_id == 1:
                user_type = UserType.ADMIN_USER if json_data.get(
                    'is_admin', False) else UserType.INTERNAL_USER
            else:
                user_type = UserType.CLIENT_USER
            user = User(
                # TODO check username with only allowed only chars
                username=json_data.get('username'),
                # TODO check username with only allowed only chars
                name=json_data.get('name'),
                email=json_data.get('email'),
                # TODO check phone number
                phone_number=json_data.get('phone_number'),
                # TODO check or remove speical chars
                address=json_data.get('address'),
                user_type=user_type,
                # client = Client.objects.get(client_id=json_data.get('client_id'))
                # if client_id is not availabile
                # then its internal user
                client_id=client_id,
            )
            user.save()
            return JsonResponse(user.get_dict())
            # TODO send email to set password link
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")
        except Exception as e:
            # TODO could not be e
            return bad_response(f"client does not exist {e}")

    # list users
    @permission_dec([UserType.ADMIN_USER])
    def get(self, request: request.HttpRequest):
        list_users = []
        for user in User.objects.filter(client_id=request.GET.get('client_id', 1)).order_by("-updated_date"):
            list_users.append(user.get_dict())
        return JsonResponse(list_users, safe=False)
