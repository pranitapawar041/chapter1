from enum import Enum
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.db.models.enums import IntegerChoices, TextChoices
from django.utils.timezone import now


class UserType(TextChoices):
    CLIENT_USER = "client_user"  # read only user
    INTERNAL_USER = "internal_user"  # internal user
    ADMIN_USER = "admin_user"  # admin user


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    # TODO CREDITOR
    creditor = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=  # 4
                                  30
                                  )
    description = models.CharField(max_length=200)
    extra_fields = models.CharField(max_length=40)  # gst or other fields
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True)
    updated_date = models.DateTimeField(
        default=now, editable=True, db_index=True)

    def get_dict(self):
        return {
            "client_id": self.client_id,
            "name": self.name,
            "short_name": self.short_name,
            "description": self.description,
            "extra_fields": self.extra_fields,
            "is_active": self.is_active,
            "creditor": self.creditor,
            "created_date": self.created_date,
            "updated_date": self.updated_date
        }


class ClientDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        Client, default=1, verbose_name="case_id", on_delete=models.SET_DEFAULT)
    file_name = models.CharField(max_length=20)
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True)

    def get_dict(self):
        return {
            "created_date": self.created_date,
            "document_id": self.document_id,
            "file_name": self.file_name,
        }


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, unique=True, )
    name = models.CharField(max_length=20, )
    email = models.EmailField(max_length=30, unique=True, )
    phone_number = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=40, null=True)
    password = models.CharField(max_length=32, )
    notify = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, )
    user_type = models.TextField(
        default=UserType.INTERNAL_USER, choices=UserType.choices)
    # for internal users
    # client name will be admin
    # for external users, client name will be actual client name
    client = models.ForeignKey(
        Client, default=1, verbose_name="client_id", on_delete=models.SET_DEFAULT)
    created_date = models.DateTimeField(
        default=now, editable=False, db_index=True)
    updated_date = models.DateTimeField(default=now, editable=True)
    last_login = models.DateTimeField(
        default=now, editable=True, db_index=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"

    def get_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_active": self.is_active,
            "user_type": self.user_type,
            "client": self.client.name,
            "client_id": self.client.client_id,
            "is_admin": self.user_type == UserType.ADMIN_USER,
            "name": self.name
        }
