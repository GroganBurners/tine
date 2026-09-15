from io import StringIO
from subprocess import CalledProcessError
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase


class DevelopmentCommandTests(SimpleTestCase):
    def test_checks_report_success(self):
        for command, expected in [
            ("lint", "Successfully linted! No errors!"),
            ("check_format", "Code format is correct! No errors!"),
        ]:
            with self.subTest(command=command):
                output = StringIO()
                with patch(f"gbs.management.commands.{command}.check_output") as run:
                    call_command(command, stdout=output)
                run.assert_called_once()
                self.assertIn(expected, output.getvalue())

    def test_checks_report_failure_details(self):
        for command, expected in [
            ("lint", "Linting failed!"),
            ("check_format", "Code format errors!"),
        ]:
            with self.subTest(command=command):
                output = StringIO()
                failure = CalledProcessError(1, command, output=b"Invalid formatting")
                with patch(
                    f"gbs.management.commands.{command}.check_output",
                    side_effect=failure,
                ):
                    call_command(command, stdout=output)
                self.assertIn(expected, output.getvalue())
                self.assertIn("Invalid formatting", output.getvalue())

    def test_unimplemented_minifier_reports_clear_error(self):
        with self.assertRaisesMessage(
            CommandError, "CSS minification is not implemented."
        ):
            call_command("minify")
