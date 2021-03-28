from django.core.management.base import BaseCommand

from persistence.data_reader.reader import Reader


class Command(BaseCommand):
    help = 'Invalidates classifier daily cache'

    def handle(self, *args, **options):
        reader = Reader()
        reader.read_data()
