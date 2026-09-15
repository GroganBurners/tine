# Only fixed developer-tool commands are run, without a shell or user input.
import sys
from subprocess import CalledProcessError, check_output  # nosec B404

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Checks the code format with black"

    def handle(self, *args, **options):
        try:
            # Run a fixed module with the current interpreter, without a shell.
            check_output(  # nosec B603
                [sys.executable, "-m", "black", "--check", "."], shell=False
            )
            self.stdout.write(self.style.SUCCESS("Code format is correct! No errors!"))
        except CalledProcessError as e:
            self.stdout.write(self.style.ERROR("Code format errors! Output is:"))
            self.stdout.write(e.output.decode("utf-8"))
