from django.core.management.base import BaseCommand, CommandError
from csscompressor import compress

class MinifyCSSCommand(BaseCommand):
    help = 'Minifies CSS'

    def handle(self, *args, **options):
        # TODO
        pass

