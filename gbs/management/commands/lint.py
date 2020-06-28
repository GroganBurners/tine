from subprocess import CalledProcessError, check_output

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Lints the code with flake8"

    def handle(self, *args, **options):
        try:
            check_output(
                [
                    "flake8",
                    ".",
                    "--exclude=env/",
                    "--ignore=E203,E231,E266,E501,W503,F403,F401 ",
                    "--max-line-length=88",
                    "--select=B,C,E,F,W,T4,B9",
                    "--max-complexity=18",
                ]
            )
            self.stdout.write(self.style.SUCCESS("Successfully linted! No errors!"))
        except CalledProcessError as e:
            self.stdout.write(self.style.ERROR("Linting failed! Output is:"))
            self.stdout.write(e.output.decode("utf-8"))
