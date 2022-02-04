from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.timezone import now

from case_user.models import Client, User


class Priority(models.TextChoices):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class Status(models.TextChoices):
    OPEN = 'open'
    INPROGRESS = 'inprogress'
    CLOSED = 'closed'


class Debitor(models.Model):
    debitor_id = models.AutoField(primary_key=True)
    name = models.TextField()


class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        Client, default=1, verbose_name="client_id", on_delete=models.SET_DEFAULT)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    priority = models.TextField(
        choices=Priority.choices, default=Priority.MEDIUM)
    status = models.TextField(
        choices=Status.choices, default=Status.OPEN)
    assignee = models.ForeignKey(
        User, verbose_name="assignee_id", on_delete=models.SET_NULL, null=True)
    debiter = models.CharField(max_length=40)
    # debitor = models.ForeignKey(
    #     Debitor, on_delete=SET_NULL, verbose_name='debitor_id', null=True)
    total_amount = models.BigIntegerField()
    recovered = models.BigIntegerField(default=0)
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True)
    updated_date = models.DateTimeField(
        default=now, editable=True, db_index=True)

    def get_dict(self):
        return {
            "case_id": self.case_id,
            "client": self.client.name,
            "client_id": self.client.client_id,
            "subject": self.subject,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "assignee": self.assignee.name,
            "assignee_id": self.assignee.user_id,
            "debiter": self.debiter,
            "total_amount": self.total_amount,
            "recovered": self.recovered,
            "created_date": self.created_date,
            "updated_date": self.updated_date,

        }


class Contacts(models.Model):
    contact_id = models.IntegerField(primary_key=True)
    case = models.ForeignKey(
        Case, default=1, verbose_name="case_id", on_delete=models.SET_DEFAULT)
    username = models.CharField(max_length=10)
    email = models.EmailField(max_length=40)
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True)
    updated_date = models.DateTimeField(
        default=now, editable=True, db_index=True)

    def get_dict(self):
        return {
            "contact_id": self.contact_id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "created_date": self.created_date,
            "updated_date": self.updated_date
        }


class DocumentType(models.TextChoices):
    CLIENT = "client"
    INTERNAL = "internal"


class CaseDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(
        Case, default=1, verbose_name="case_id", on_delete=models.SET_DEFAULT)
    file_name = models.CharField(max_length=20)
    doc_type = models.TextField(
        choices=DocumentType.choices, default=DocumentType.CLIENT)
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True, )

    def get_dict(self):
        return {
            "created_date": self.created_date,
            "doc_type": self.doc_type,
            "is_internal": self.doc_type == DocumentType.INTERNAL,
            "document_id": self.document_id,
            "file_name": self.file_name,
            "case": self.case.subject,
            "case_id": self.case.case_id
        }


class TimeLineType(models.TextChoices):
    CONVERSATION = "general"
    LEGAL = "legal"
    TRANSACTION = "transaction"


class TimelineEntry(models.Model):
    entry_id = models.IntegerField(primary_key=True)
    case = models.ForeignKey(
        Case, default=1, verbose_name="case_id", on_delete=models.SET_DEFAULT)
    entry_type = models.TextField(
        choices=TimeLineType.choices, default=TimeLineType.CONVERSATION)
    convo_date = models.DateTimeField(
        default=now, editable=False, db_index=True)
    legal_case_id = models.TextField()
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True)
    updated_date = models.DateTimeField(
        default=now, editable=True, db_index=True)
    amount_recovered = models.BigIntegerField(null=True)
    subject = models.CharField(max_length=2000)

    def get_dict(self):
        return {
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "date": self.convo_date,
            "entry_type":  self.entry_type,
            "case_id": self.case.case_id,
            "legal_case_id": self.legal_case_id,
            "case": self.case.subject,
            "entry_id": self.entry_id,
            "subject": self.subject,
            "amount_recovered": self.amount_recovered,
        }
        # match self.entry_type:
        #     case TimeLineType.CONVERSATION:
        #         ret[""] = ""
        #     case TimeLineType.LEGAL:
        #         ret[""] = ""
        #     case TimeLineType.TRANSACTION:
        #         ret[""] = ""


# class LegalEntry(models.Model):
#     entry_id = models.ForeignKey(
#         TimelineEntry, default=1, verbose_name="client_id", on_delete=models.SET_DEFAULT)
#     amount_recovered: models.BigIntegerField()
