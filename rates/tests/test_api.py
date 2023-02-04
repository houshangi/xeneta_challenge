from unittest import TestCase
from django.test import Client


class AveragePriceListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_params(self):
        # Test case for valid parameters
        response = self.client.get(
            "/api/rates?"
            "origin=CNGGZ&"
            "destination=NOOSL"
            "&date_from=2016-01-01"
            "&date_to=2016-01-28"
        )
        self.assertEqual(response.status_code, 200)

    def test_none_origin_param(self):
        # Test case for none origin parameter
        response = self.client.get(
            "/api/rates"
            "?destination=NOOSL"
            "&date_from=2016-01-01"
            "&date_to=2016-01-28"
        )
        self.assertEqual(response.status_code, 400)

    def test_none_destination_param(self):
        # Test case for none destination parameter
        response = self.client.get(
            "/api/rates?" "origin=CNSGH&" "date_from=2016-01-01&" "date_to=2016-01-28"
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_month_date_from_param(self):
        # Test case for invalid date_from parameter
        response = self.client.get(
            "/api/rates?origin=CNSGH&destination=NOOSL&date_from=2022-13-01&date_to=2022-01-10"
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_month_date_to_param(self):
        # Test case for invalid date_to parameter
        response = self.client.get(
            "/api/rates?origin=CNSGH&destination=NOOSL&date_from=2016-01-01&date_to=2016-13-10"
        )
        self.assertEqual(response.status_code, 400)

    def test_date_from_after_date_to(self):
        response = self.client.get(
            "/api/rates?"
            "origin=AMS"
            "&destination=MOW&"
            "date_from=2016-12-01&"
            "date_to=2016-01-10"
        )
        self.assertEqual(response.status_code, 400)
