# Only fixed developer-tool commands are run, without a shell or user input.
import sys
from subprocess import CalledProcessError, check_output  # nosec B404

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Lints the code with flake8"

    def handle(self, *args, **options):
        try:
            # Run a fixed module with the current interpreter, without a shell.
            check_output(  # nosec B603
                [
                    sys.executable,
                    "-m",
                    "flake8",
                    ".",
                    "--exclude=env/",
                    "--ignore=E203,E231,E266,E501,W503,F403,F401",
                    "--max-line-length=88",
                    "--select=B,C,E,F,W,T4,B9",
                    "--max-complexity=18",
                ],
                shell=False,
            )
            self.stdout.write(self.style.SUCCESS("Successfully linted! No errors!"))
        except CalledProcessError as e:
            self.stdout.write(self.style.ERROR("Linting failed! Output is:"))
            self.stdout.write(e.output.decode("utf-8"))
