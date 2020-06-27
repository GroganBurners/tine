from csscompressor import compress
from django.core.management.base import BaseCommand, CommandError


class MinifyCSSCommand(BaseCommand):
    help = "Minifies CSS"

    def handle(self, *args, **options):
        # TODO
        pass
