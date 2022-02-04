from itertools import count
import os
import pathlib

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.http import request
from django.http.response import FileResponse, JsonResponse
from task_system.settings import STORAGE_DIR

from case_user.base_view import JsonView
from case_user.exceptions import UnAuthorized
from case_user.models import Client, ClientDocument, User, UserType
from case_user.utils import bad_response, check_admin, permission_dec

from .base_view import OnlyLoggedIn


class ClientApis(OnlyLoggedIn, JsonView):

    def get(self, request: request.HttpRequest):
        user: User = request.user
        skip = int(request.GET.get('skip', '0'))
        if user.user_type == UserType.CLIENT_USER:
            return UnAuthorized("only internal users can access client list")
        ret = []
        for client in Client.objects.filter(~Q(client_id=1)).order_by('-updated_date')[skip:skip+20]:
            # TODO add closed cases
            # TODO add total cases
            ret.append(client.get_dict())
        return JsonResponse(ret, safe=False)

    @permission_dec([UserType.ADMIN_USER])
    def patch(self, request: request.HttpRequest):
        json_data = self.json(request)
        try:
            client: Client = Client.objects.get(
                client_id=json_data.get('client_id'))
            if 'name' in json_data:
                # TODO check name
                x = json_data['name'].isalpha()
                if x == True:
                    print("name is valid")
                else:
                    print("name isn't acceptable")
                client.name = json_data.get('name')
            if 'creditor' in json_data:
                # TODO check creditor
                count = 0
                for c in json_data:
                    if c.isalpha():
                        count+=1
                if len(json_data['name'])==count:
                    print('creditor is valid')
                else:
                    print('creditor is valid')
                client.creditor = json_data.get('creditor')
            if 'short_name' in json_data:
                # TODO check short_name
                count = 0
                for c in json_data:
                    if c.isalpha():
                        count+=1
                if len(json_data['short_name'])==count:
                    print('short_name is valid')
                else:
                    print('short_name is not valid')
                client.short_name = json_data.get('short_name')
            if 'description' in json_data:
                # TODO check description
                count = 0
                for c in json_data:
                    if c.isalpha():
                        count+=1
                if len(json_data['description'])== count:
                    print("description is valid")
                else:
                    print('description is not valid')
                client.description = json_data.get('description')
            if 'extra_fields' in json_data:
                count = 0
                for c in json_data:
                    if c.isalpha():
                        count+=1
                if len(json_data['extra_field'])== count:
                    print("extra field is valid")
                else:
                    print('extra field is not valid')
                client.extra_fields = json_data.get('extra_fields')
            if 'is_active' in json_data:
                count = 0
                for c in json_data:
                    if c.isalpha():
                        count+=1
                if len(json_data['is_active'])== count:
                    print(" valid")
                else:
                    print(' not- valid')
                client.is_active = json_data.get('is_active')
            assert client.name != 'admin', "new client name should never be admin"
            client.save()
            return JsonResponse({"success": True, "client_id": client.client_id}, )
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")
        except Exception as e:
            # TODO could not be e
            return bad_response(f"client does not exist {e}")

    @permission_dec([UserType.ADMIN_USER])
    def post(self, request: request.HttpRequest):
        json_data = self.json(request)
        try:
            client = Client(
                name=json_data.get('name'),
                short_name=json_data.get('short_name'),
                description=json_data.get('description'),
                extra_fields=json_data.get('extra_fields'),
                creditor=json_data.get('creditor')
            )
            client.save()
            return JsonResponse({"success": True, "client_id": client.client_id}, )
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")
        except Exception as e:
            # TODO could not be e
            return bad_response(f"client does not exist {e}")


class DownloadDocumentView(OnlyLoggedIn, JsonView):

    @permission_dec([UserType.ADMIN_USER, UserType.CLIENT_USER, UserType.ADMIN_USER])
    def get(self, request: request.HttpRequest, client_id: int, document_id: int):
        try:
            params = {"client_id": client_id}
            if request.user.user_type == UserType.CLIENT_USER and request.user.client.client_id != client_id:
                raise UnAuthorized()
            case_doc = ClientDocument.objects.get(
                document_id=document_id)
            path = f'{STORAGE_DIR}/{case_doc.client.client_id}/docs/{case_doc.document_id}-{case_doc.file_name}'
            if not os.path.exists(path):
                return bad_response("document not availabile")
            else:
                return FileResponse(open(path, 'rb'), as_attachment=True, filename=case_doc.file_name)
        except Exception as e:
            return bad_response("document not found")

    @permission_dec([UserType.ADMIN_USER, UserType.CLIENT_USER])
    def delete(self, request: request.HttpRequest, client_id: int, document_id: int):
        try:
            case_doc: ClientDocument = ClientDocument.objects.get(
                client_id=client_id,
                document_id=document_id)
            case_doc.delete()
            # TODO delete from local store
            return JsonResponse({})
        except:
            return bad_response("document unavailabile")


class ClientDetails (OnlyLoggedIn, JsonView):
    @permission_dec([UserType.ADMIN_USER])
    def get(self, request:  request.HttpRequest, client_id: int):
        try:
            client: Client = Client.objects.get(client_id=client_id)
            return JsonResponse(client.get_dict())
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("case does not exist")
        except:
            return JsonResponse({}, status=500)


class ClientDocumentsView(OnlyLoggedIn, JsonView):
    @permission_dec([UserType.ADMIN_USER])
    def get(self, request:  request.HttpRequest, client_id: int):
        try:
            params = {"client_id": client_id}
            ret = []
            documents = ClientDocument.objects.filter(**params)
            for document in documents:
                ret.append(document.get_dict())
            return JsonResponse(ret, safe=False)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("case does not exist")

    @permission_dec([UserType.ADMIN_USER, UserType.CLIENT_USER])
    def post(self, request: request.HttpRequest, client_id: int):
        try:
            documents = request.FILES.getlist('documents')
            if len(documents) == 0:
                return bad_response("no documents")
            client = Client.objects.get(client_id=client_id)
            for document in documents:
                db_obj = ClientDocument(
                    file_name=document.name, client=client)
                db_obj.save()
                path = f'{STORAGE_DIR}/{client.client_id}/docs/{db_obj.document_id}-{document.name}'
                pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'wb+') as destination:
                    for chunk in document.chunks():
                        destination.write(chunk)
            return JsonResponse({}, safe=False)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("case does not exist")
