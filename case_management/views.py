import json
import os
import pathlib
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http.request import HttpRequest
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from case_management.models import Case, CaseDocument, Contacts, DocumentType, Priority, Status

from case_user.base_view import JsonView, OnlyLoggedIn
from case_user.models import Client, User, UserType
from case_user.utils import bad_response, UnAuthorized, permission_dec
from task_system.settings import STORAGE_DIR

# Create your views here.


class ContactView(OnlyLoggedIn, JsonView):
    def get(self, request: HttpRequest, case_id: int):
        if request.user.user_type == UserType.CLIENT_USER:
            try:
                Case.objects.get(case_id=case_id, client=request.user.client)
            except:
                raise UnAuthorized()
        ret = []
        try:
            for contact in Contacts.objects.filter(case_id=case_id).order_by('-updated_date'):
                ret.append(contact.get_dict())
            return JsonResponse(ret, safe=False)
        except:
            return JsonResponse(ret, safe=False)

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def delete(self, request: HttpRequest, case_id: int):
        contact_id = self.json(request).get('contact_id', None)
        if not contact_id:
            return bad_response("contact_id is required")
        try:
            Contacts.objects.delete(case_id=case_id, contact_id=contact_id)
            return JsonResponse({})
        except:
            return JsonResponse({}, status=500)

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def patch(self, request: HttpRequest, case_id: int):
        json_data = self.json(request)
        try:
            contact: Contacts = Contacts.objects.get(
                contact_id=json_data.get('contact_id'), case_id=case_id)
            if 'name' in json_data:
                contact.name = json_data['name']
            if 'phone_number' in json_data:
                contact.name = json_data['phone_number']
            if 'username' in json_data:
                contact.username = json_data['username']
            if 'email' in json_data:
                contact.email = json_data['email']
            if 'address' in json_data:
                contact.address = json_data['address']
            contact.updated_date = now()
            contact.save()
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("case does not exist")

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def post(self, request: HttpRequest, case_id: int):
        json_data = self.json(request)
        try:
            case = Case.objects.get(
                case_id=case_id)
            contact = Contacts(
                case=case,
                # TODO validate name
                name=json_data.get('name'),
                # TODO validate phone_number
                phone_number=json_data.get('phone_number'),
                # TODO validate user_name
                username=json_data.get('username'),
                # TODO validate email
                email=json_data.get('email'),
                # TODO validate address
                address=json_data.get('address'),
            )
            contact.save()
            return JsonResponse({"success": True, "contact_id": contact.contact_id})
        except Exception as e:
            print(e)
            return bad_response("error creating case")


class DownloadDocumentView(OnlyLoggedIn, JsonView):
    def get(self, request: HttpRequest, case_id: int, document_id: int):
        try:
            params = {"case_id": case_id}
            if request.user.user_type == UserType.CLIENT_USER:
                case = Case.objects.get(case_id=case_id)
                if case.client.client_id != request.user.client.client_id:
                    raise UnAuthorized()
            case_doc: CaseDocument = CaseDocument.objects.get(
                document_id=document_id)
            path = f'{STORAGE_DIR}/{case_doc.case.client_id}/cases/{case_id}/{case_doc.doc_type.lower()}/{case_doc.document_id}-{case_doc.file_name}'
            if not os.path.exists(path):
                return bad_response("document not availabile")
            else:
                return FileResponse(open(path, 'rb'), as_attachment=True, filename=case_doc.file_name)
        except Exception as e:
            return bad_response("document not found")

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def delete(self, request: HttpRequest, case_id: int, document_id: int):
        try:
            params = {"case_id": case_id}
            case_doc: CaseDocument = CaseDocument.objects.get(
                document_id=document_id)
            case_doc.delete()
            # TODO delete from local store
            return JsonResponse({})
        except:
            return bad_response("document unavailabile")


class CaseDocumentsView(OnlyLoggedIn, JsonView):

    def get(self, request: HttpRequest, case_id: int):
        try:
            params = {"case_id": case_id}
            if request.user.user_type == UserType.CLIENT_USER:
                case = Case.objects.get(case_id=case_id)
                if case.client.client_id != request.user.client.client_id:
                    raise UnAuthorized()
                params["doc_type"] = DocumentType.CLIENT
            ret = []
            documents = CaseDocument.objects.filter(**params)
            for document in documents:
                ret.append(document.get_dict())
            return JsonResponse(ret, safe=False)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("case does not exist")

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def post(self, request: HttpRequest, case_id: int):
        try:
            if request.GET.get("is_internal", 'true').lower() == 'true':
                doc_type = DocumentType.INTERNAL
            else:
                doc_type = DocumentType.CLIENT
            documents = request.FILES.getlist('documents')
            if len(documents) == 0:
                return bad_response("no documents")
            case = Case.objects.get(case_id=case_id)
            for document in documents:
                db_obj = CaseDocument(
                    file_name=document.name, case=case, doc_type=doc_type)
                db_obj.save()
                path = f'{STORAGE_DIR}/{case.client_id}/cases/{case_id}/{doc_type}/{db_obj.document_id}-{document.name}'
                pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'wb+') as destination:
                    for chunk in document.chunks():
                        destination.write(chunk)
            return JsonResponse({}, safe=False)
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("case does not exist")


class ClientCaseView(OnlyLoggedIn, JsonView):
    @permission_dec([UserType.ADMIN_USER])
    def get(self, request: HttpRequest, client_id: int):
        try:
            cases = Case.objects.filter(
                client_id=client_id).order_by("-updated_date")
            ret = []
            for case in cases:
                ret.append(case.get_dict())
            return JsonResponse(ret, safe=False)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            return JsonResponse([], safe=False)
        except:
            return JsonResponse({}, status=500)


class CaseView(OnlyLoggedIn, JsonView):
    def get(self, request: HttpRequest):
        user: User = request.user
        client: Client = user.client
        ret = []
        if user.user_type == UserType.CLIENT_USER:
            cases = Case.objects.filter(
                client_id=client.client_id).order_by("-updated_date")
        else:
            cases = Case.objects.filter().order_by("-updated_date")
        for case in cases:
            ret.append(case.get_dict())
        return JsonResponse(ret, safe=False)

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def patch(self, request=HttpRequest):
        try:
            json_data = self.json(request)
            case_id = json_data.get('case_id')
            case = Case.objects.get(case_id=case_id)
            if 'subject' in json_data:
                case.subject = json_data['subject']
            if 'description' in json_data:
                case.description = json_data['description']
            if 'priority' in json_data:
                case.priority = json_data.get("priority")
            if 'status' in json_data:
                case.status = json_data.get("status")
            case.save()
            # TODO save docs
            # TODO save contacts
            return JsonResponse({"success": True, "case_id": case.case_id})
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def post(self, request=HttpRequest):
        try:
            json_data = self.json(request)
            client_id = json_data.get('client_id')
            if client_id == 1:
                return bad_response("cannot create cases in admin")
            client = Client.objects.get(client_id=client_id)
            case = Case(
                **dict(
                    client=client,
                    subject=json_data.get("subject"),
                    description=json_data.get("description", ""),
                    priority=Priority(json_data.get(
                        "priority", Priority.MEDIUM.value).lower()),
                    status=Status(json_data.get(
                        "status", Status.OPEN.value).lower()),
                    assignee=request.user,
                    debiter=json_data.get("debiter"),
                    total_amount=json_data.get("total_amount"),
                ))
            case.save()
            # TODO save docs
            # TODO save contacts
            return JsonResponse({"success": True, "case_id": case.case_id})
        except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
            return bad_response("client does not exist")
