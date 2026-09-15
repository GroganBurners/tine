import unittest
from datetime import date, datetime, timezone
from io import BytesIO
from unittest.mock import patch
from zipfile import ZipFile

from django.test import override_settings

from gbs import utils


class UtilsTest(unittest.TestCase):
    def test_generate_zip(self):
        files = [("invoice.pdf", b"pdf content"), ("empty.txt", b"")]
        with ZipFile(BytesIO(utils.generate_zip(files))) as archive:
            self.assertEqual(archive.namelist(), [name for name, _ in files])
            for name, content in files:
                self.assertEqual(archive.read(name), content)

    def test_excel_response(self):
        pass

    def test_pdf_response(self):
        pass

    def test_zip_response(self):
        response = utils.zip_response([("report.txt", b"Report")], "reports.zip")
        self.assertEqual(response["Content-Type"], "application/zip")
        self.assertEqual(
            response["Content-Disposition"], 'attachment; filename="reports.zip"'
        )
        with ZipFile(BytesIO(response.content)) as archive:
            self.assertEqual(archive.read("report.txt"), b"Report")

    def test_format_currency(self):
        self.assertEqual(utils.format_currency(2), "€ 2.00")

    def test_meteorological_season_boundaries(self):
        cases = [
            (date(2026, 1, 1), "winter"),
            (date(2026, 2, 28), "winter"),
            (date(2024, 2, 29), "winter"),
            (date(2026, 3, 1), "spring"),
            (date(2026, 5, 31), "spring"),
            (date(2026, 6, 1), "summer"),
            (date(2026, 8, 31), "summer"),
            (date(2026, 9, 1), "autumn"),
            (date(2026, 11, 30), "autumn"),
            (date(2026, 12, 1), "winter"),
            (date(2026, 12, 31), "winter"),
        ]
        for on_date, expected in cases:
            with self.subTest(on_date=on_date):
                self.assertEqual(utils.get_season(on_date), expected)

    @override_settings(TIME_ZONE="America/New_York")
    def test_season_changes_at_irish_midnight(self):
        for instant, expected in [
            (datetime(2026, 5, 31, 22, 59, tzinfo=timezone.utc), "spring"),
            (datetime(2026, 5, 31, 23, 0, tzinfo=timezone.utc), "summer"),
        ]:
            with self.subTest(instant=instant):
                with patch("django.utils.timezone.now", return_value=instant):
                    self.assertEqual(utils.get_season(), expected)
