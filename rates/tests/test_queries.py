import unittest
from unittest.mock import patch
from rest_framework import exceptions
from ..queries import QueryHandler


class QueryHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.query_handler = QueryHandler()

    def test_validate_params_with_valid_input(self):
        origin = "CNGGZ"
        destination = "NOOSL"
        date_from = "2016-01-01"
        date_to = "2016-01-03"
        self.query_handler.validate_params(origin, destination, date_from, date_to)

    def test_validate_params_with_invalid_origin(self):
        origin = None
        destination = "NOOSL"
        date_from = "2016-01-01"
        date_to = "2016-01-31"
        with self.assertRaises(exceptions.ValidationError) as cm:
            self.query_handler.validate_params(origin, destination, date_from, date_to)

        self.assertEqual(
            str(cm.exception),
            "{'origin':"
            " ErrorDetail(string='origin must be a string and cannot be None'"
            ", code='invalid')}",
        )

    def test_validate_params_with_invalid_destination(self):
        origin = "CNGHZ"
        destination = None
        date_from = "2016-01-01"
        date_to = "2016-01-31"
        with self.assertRaises(exceptions.ValidationError) as cm:
            self.query_handler.validate_params(origin, destination, date_from, date_to)

        self.assertEqual(
            str(cm.exception),
            "{'destination':"
            " ErrorDetail"
            "(string='destination must be a string and cannot be None'"
            ", code='invalid')}",
        )

    def test_validate_params_with_invalid_date_from(self):
        origin = "test"
        destination = "test1"
        date_from = "2022-13-01"
        date_to = "2022-01-31"
        with self.assertRaises(exceptions.ValidationError) as cm:
            self.query_handler.validate_params(origin, destination, date_from, date_to)
        self.assertEqual(
            str(cm.exception),
            "{'date_from':"
            " ErrorDetail"
            "(string='bad month number 13;"
            " must be 1-12', code='invalid')}",
        )

    def test_validate_params_with_invalid_date_to(self):
        origin = "CNGH"
        destination = "NOOSL"
        date_from = "2022-01-01"
        date_to = "2022-02-31"
        with self.assertRaises(exceptions.ValidationError) as cm:
            self.query_handler.validate_params(origin, destination, date_from, date_to)
        self.assertEqual(
            str(cm.exception),
            "{'date_to':"
            " ErrorDetail(string='Day must be between 1 and"
            " 28 for the specified month and year',"
            " code='invalid')}",
        )

    @patch("django.db.connection.cursor")
    def test_execute_query(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
            ("2016-01-01", 1541.3333333333333333),
            ("2016-01-02", 1541.0000000000000000),
        ]

        result = QueryHandler.execute_query(
            "CNGGZ", "NOOSL", "2016-01-01", "2016-01-03"
        )
        self.assertEqual(
            result,
            [
                ("2016-01-01", 1541.3333333333333333),
                ("2016-01-02", 1541.0000000000000000),
            ],
        )
