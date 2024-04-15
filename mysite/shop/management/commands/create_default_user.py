from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shop.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create default User")
        result = User.objects.get_or_create(name="empty_user")
        self.stdout.write(result)
