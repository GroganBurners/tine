from subprocess import CalledProcessError, check_output

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Checks the code format with black"

    def handle(self, *args, **options):
        try:
            check_output(["black", "--check", "."])
            self.stdout.write(self.style.SUCCESS("Code format is correct! No errors!"))
        except CalledProcessError as e:
            self.stdout.write(self.style.ERROR("Code format errors! Output is:"))
            self.stdout.write(e.output.decode("utf-8"))
