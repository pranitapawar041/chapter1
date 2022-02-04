import json
import logging
from typing import Any

from django.http import HttpResponse, JsonResponse, request
from django.views import View

from .exceptions import (BadRequest, CaseUserException, NotLoggedInException,
                         UnAuthorized)
from .utils import check_logged_in

logger = logging.getLogger(__name__)


class BaseView(View):
    def dispatch(self, request: request.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except NotLoggedInException:
            return JsonResponse({
                "success": False,
                "message": "please login"
            }, status=401)
        except UnAuthorized:
            return JsonResponse({
                "success": False,
                "message": "unauthorized"
            }, status=403)
        except BadRequest as e:
            return JsonResponse({
                "success": False,
                "message": str(e)}, status=400)
        except CaseUserException as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)


class OnlyLoggedIn(BaseView):

    def dispatch(self, request, *args, **kwargs):
        try:
            check_logged_in(request)
            self.user = request.user
            return super().dispatch(request, *args, **kwargs)
        except NotLoggedInException:
            return JsonResponse({
                "success": False,
                "message": "please login"
            }, status=401)
        except UnAuthorized:
            return JsonResponse({
                "success": False,
                "message": "unauthorized"
            }, status=403)
        except BadRequest as e:
            return JsonResponse({
                "success": False,
                "message": str(e)}, status=400)
        except CaseUserException as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)


class JsonView(BaseView):
    def json(self, request: request.HttpRequest):
        if request.headers.get(
                'content-type', "").startswith("application/json"):
            try:
                return json.loads(request.body)
            except:
                logger.warn('content-type is json but responded with nonjson')
        raise CaseUserException("non json request")
