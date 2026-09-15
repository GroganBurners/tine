# CalledProcessError only simulates tool failures; this test starts no processes.
import sys
from io import StringIO
from subprocess import CalledProcessError  # nosec B404
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
                executable, flag, module = run.call_args.args[0][:3]
                self.assertEqual(executable, sys.executable)
                self.assertEqual(flag, "-m")
                self.assertEqual(module, "flake8" if command == "lint" else "black")
                self.assertIs(run.call_args.kwargs["shell"], False)
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
