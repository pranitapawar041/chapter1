from django.core.management.base import BaseCommand, CommandError
from ...models import Client, User, UserType


class Command(BaseCommand):
    help = 'Create Admin User'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone_number', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('-user_type', type=str,
                            default=UserType.ADMIN_USER.value)

    def handle(self, username, name, email, phone_number, password, user_type, *args, **kwargs):
        client = Client(name='admin', short_name='adm',)
        client.save()
        user = User(
            username=username,
            name=name,
            email=email,
            phone_number=phone_number,
            user_type=UserType(user_type)
        )
        user.set_password(password)
        user.save()
