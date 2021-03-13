from django.core.management.base import BaseCommand

from app.models import CustomUser


class Command(BaseCommand):
    help = 'Invalidates classifier daily cache'

    def handle(self, *args, **options):
        # CustomUser.objects.create(email="x@d.pl", password="testpwd")
        c = CustomUser.objects.get(email="somemail@a.com")
