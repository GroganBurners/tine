import unittest
from datetime import date

from gbs import utils


class UtilsTest(unittest.TestCase):
    def test_generate_zip(self):
        pass

    def test_excel_response(self):
        pass

    def test_pdf_response(self):
        pass

    def test_zip_response(self):
        pass

    def test_format_currency(self):
        self.assertEqual(utils.format_currency(2), "€ 2.00")

    def test_season(self):
        from datetime import date

        doy = date.today().timetuple().tm_yday
        # "day of year" ranges for the northern hemisphere
        spring = range(80, 172)
        summer = range(172, 264)
        autumn = range(264, 355)
        # winter = everything else

        if doy in spring:
            season = "spring"
        elif doy in summer:
            season = "summer"
        elif doy in autumn:
            season = "autumn"
        else:
            season = "winter"

        self.assertEqual(utils.get_season(), season)
