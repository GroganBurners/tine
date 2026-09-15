from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Minifies CSS"

    def handle(self, *args, **options):
        raise CommandError("CSS minification is not implemented.")
