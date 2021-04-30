from django.core.management.base import BaseCommand
from rest_framework_api_key.models import APIKey


class Command(BaseCommand):
    help = 'Invalidates classifier daily cache'

    def handle(self, *args, **options):
        api_key, key = APIKey.objects.create_key(name="worker")
        print(f'Do not share those! key: "{key}", api_key: {api_key}')
