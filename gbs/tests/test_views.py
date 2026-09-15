from datetime import datetime, timezone
from unittest.mock import patch

from django.test import Client, TestCase

from gbs.models import HeroImage, Price


class ViewsTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_homepage(self):
        # Issue a GET request.
        price = Price(type="repair_call_out", cost=80.00, summer_offer=False)
        price.save()
        response = self.client.get("/")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str(response.context["repair_fees"][0]),
            "Repair Call Out Fee (First Hour) €80",
        )


class SeasonalBannerTests(TestCase):
    def create_banner(self, title, season="", active=True):
        return HeroImage.objects.create(
            title=title,
            image=f"images/hero/{title}.jpg",
            img_alt=f"{title} banner",
            teaser_text=f"{title} message",
            active=active,
            season=season,
            use_button=True,
            button_text="Contact us",
            button_link="/#contact",
        )

    def homepage_at(self, instant):
        with patch("django.utils.timezone.now", return_value=instant):
            return self.client.get("/")

    def test_each_season_selects_its_image_and_message(self):
        self.create_banner("Default")
        banners = {
            3: self.create_banner("Spring", "spring"),
            6: self.create_banner("Summer", "summer"),
            9: self.create_banner("Autumn", "autumn"),
            12: self.create_banner("Winter", "winter"),
        }
        for month, banner in banners.items():
            with self.subTest(month=month):
                response = self.homepage_at(
                    datetime(2026, month, 1, tzinfo=timezone.utc)
                )
                self.assertEqual(response.context["hero"], banner)
                self.assertContains(response, banner.image.url)
                self.assertContains(response, banner.teaser_text)
                self.assertContains(response, banner.img_alt)
                self.assertContains(response, 'href="/#contact"')
                self.assertNotContains(response, "Default message")

    def test_inactive_and_other_season_banners_use_all_year_fallback(self):
        self.create_banner("Inactive summer", "summer", active=False)
        self.create_banner("Winter", "winter")
        fallback = self.create_banner("Default")
        response = self.homepage_at(datetime(2026, 7, 1, tzinfo=timezone.utc))
        self.assertEqual(response.context["hero"], fallback)

    def test_no_matching_banner_hides_hero(self):
        self.create_banner("Winter", "winter")
        self.create_banner("Inactive default", active=False)
        response = self.homepage_at(datetime(2026, 7, 1, tzinfo=timezone.utc))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["hero"])
        self.assertNotContains(response, '<section class="hero">')

    def test_multiple_matches_choose_oldest(self):
        first = self.create_banner("First", "summer")
        self.create_banner("Second", "summer")
        response = self.homepage_at(datetime(2026, 7, 1, tzinfo=timezone.utc))
        self.assertEqual(response.context["hero"], first)

    def test_banner_switches_at_irish_midnight(self):
        spring = self.create_banner("Spring", "spring")
        summer = self.create_banner("Summer", "summer")
        before = self.homepage_at(datetime(2026, 5, 31, 22, 59, tzinfo=timezone.utc))
        after = self.homepage_at(datetime(2026, 5, 31, 23, 0, tzinfo=timezone.utc))
        self.assertEqual(before.context["hero"], spring)
        self.assertEqual(after.context["hero"], summer)
