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
            "&date_to=2016-01-03"
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
        self.assertEqual(
            response.content,
            b'{"origin":' b'"origin must be a' b' string and cannot be None"}',
        )

    def test_none_destination_param(self):
        # Test case for none destination parameter
        response = self.client.get(
            "/api/rates?origin=CNSGH&" "date_from=2016-01-01&" "date_to=2016-01-28"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b'{"destination":'
            b'"destination must '
            b'be a string and cannot be None"}',
        )

    def test_invalid_month_date_from_param(self):
        # Test case for invalid date_from parameter
        response = self.client.get(
            "/api/rates?origin=CNSGH&destination=NOOSL&"
            "date_from=2022-13-01&date_to=2022-01-10"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, b'{"date_from":"bad month number 13;' b' must be 1-12"}'
        )

    def test_invalid_month_date_to_param(self):
        # Test case for invalid date_to parameter
        response = self.client.get(
            "/api/rates?origin=CNSGH&"
            "destination=NOOSL"
            "&date_from=2016-01-01"
            "&date_to=2016-13-10"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, b'{"date_to":"bad month number 13;' b' must be 1-12"}'
        )

    def test_date_from_after_date_to(self):
        response = self.client.get(
            "/api/rates?"
            "origin=AMS"
            "&destination=MOW&"
            "date_from=2016-12-01&"
            "date_to=2016-01-10"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b'{"date_from"' b':"date_from cannot' b' be after date_to"}',
        )

    def test_empty_list_in_response(self):
        #test to generate empty list with valid but not meaningful names
        response = self.client.get(
            "/api/rates"
            "?date_from=2016-01-01"
            "&date_to=2016-01-03"
            "&origin=notmeaningfulorigin"
            "&destination=notmeaningfuldestination"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b"[]",
        )
