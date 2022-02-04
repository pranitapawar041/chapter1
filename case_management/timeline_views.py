

import datetime
import json
import traceback
from django.core.exceptions import ObjectDoesNotExist
from case_user.base_view import JsonView, OnlyLoggedIn
from case_user.exceptions import UnAuthorized
from case_user.models import UserType
from django.http import HttpRequest, HttpResponse, request
from django.http.response import JsonResponse
from django.utils.timezone import now

from case_user.utils import permission_dec

from .models import Case, TimelineEntry, TimeLineType


class TimelineSingleEntryView(JsonView, OnlyLoggedIn):

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def delete(self, request: HttpRequest, case_id: int, timeline_id: int) -> HttpResponse:
        try:
            TimelineEntry.objects.delete(case_id=case_id, entry_id=timeline_id)
            return JsonResponse({"success": True, })
        except:
            return JsonResponse({}, 500)

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def patch(self, request: HttpRequest, case_id: int, timeline_id: int) -> HttpResponse:
        try:
            json_data = self.json(request)
            entry: TimelineEntry = TimelineEntry.objects.get(
                case_id=case_id, entry_id=timeline_id)
            if 'subject' in json_data:
                entry.subject = json_data['subject']
            match  entry.entry_type:
                case TimeLineType.CONVERSATION:
                    subject = json_data.get('c2d')
                    if json_data.get('c2d'):
                        subject = f"creditor --> debitor `{subject}`"
                    else:
                        subject = f"debitor --> creditor `{subject}`"
                    entry.subject = subject
                case TimeLineType.LEGAL:
                    # TODO update amount recovered
                    if json_data.get('legal_case_id'):
                        entry.legal_case_id = json_data.get('legal_case_id')
                case TimeLineType.TRANSACTION:
                    if json_data.get('amount_recovered'):
                        # TODO
                        # update amount recovered

                        entry.amount_recovered = json_data.get(
                            'amount_recovered')
            if 'date' in json_data:
                entry.convo_date = datetime.datetime.fromtimestamp(
                    json_data.get('date'))
            entry.updated_date = now()
            entry.save()
            return JsonResponse({"success": True, })
        except:
            traceback.print_exc()
            return JsonResponse({}, status=500)


class TimeLineEntryView(JsonView, OnlyLoggedIn):
    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER, UserType.CLIENT_USER])
    def get(self, request: HttpRequest, case_id: int) -> HttpResponse:
        filter = request.GET.get("filter", "all")
        skip = int(request.GET.get('skip', '0'))
        ret = []
        params = {"case_id": case_id}
        if filter == "transaction":
            params["entry_type"] = TimeLineType.TRANSACTION
        elif filter == "legal":
            params["entry_type"] = TimeLineType.LEGAL
        try:
            for entry in TimelineEntry.objects.filter(**params).order_by(
                    "-updated_date")[skip:skip+20]:
                ret.append(entry.get_dict())
            return JsonResponse(ret, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse(ret, safe=False)

    @permission_dec([UserType.ADMIN_USER, UserType.INTERNAL_USER])
    def post(self, request: HttpRequest, case_id: int) -> HttpResponse:
        try:
            json_data = self.json(request)
            case = Case.objects.get(case_id=case_id)
            entry_type = json_data.get("entry_type").lower()
            subject = json_data.get("subject")
            params = dict(
                entry_type=entry_type,
                case=case,
                convo_date=datetime.datetime.fromtimestamp(
                    json_data.get("date")),
            )
            match  entry_type:
                case TimeLineType.CONVERSATION:
                    if json_data.get('c2d'):
                        subject = f"creditor --> debitor `{subject}`"
                    else:
                        subject = f"debitor --> creditor `{subject}`"
                    params['subject'] = subject
                case TimeLineType.LEGAL:
                    # TODO update amount recovered
                    params['legal_case_id'] = json_data.get('legal_case_id')
                case TimeLineType.TRANSACTION:
                    params['amount_recovered'] = json_data.get(
                        'amount_recovered')
            entry = TimelineEntry(**params)
            entry.save()
            return JsonResponse({"success": True, "entry_id": entry.entry_id}, safe=False)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"message": str(e)}, status=500)
