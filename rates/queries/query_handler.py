import re
from django.db import connection
from rest_framework import exceptions
import calendar
import datetime


class QueryHandler:
    """
    The QueryHandler class contains methods for validating parameters and executing
    a query to retrieve average prices
    for a specific origin and destination port within a date range.

    The class uses regular expression to validate date input and Django's
    connection to execute the query.
    In case of invalid input,
     it raises ValidationError from the rest_framework exceptions.

    Attributes:
        date_regex (re.Pattern): A regular expression pattern to match the date format.
    """

    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    @staticmethod
    def validate_params(origin, destination, date_from, date_to):
        """
        Validates the input parameters for origin, destination, date_from and date_to.

        Args:
            origin (str): The code of the origin port.
            destination (str): The code of the destination port.
            date_from (str): The start date in the format 'YYYY-MM-DD'.
            date_to (str): The end date in the format 'YYYY-MM-DD'.

        Raises:
            ValidationError: If the origin is None or not a string.
                             If the destination is None or not a string.
                             If the date_from does not match the format 'YYYY-MM-DD'.
                             If the date_to does not match the format 'YYYY-MM-DD'.
                             If the date_from > date_to.
                             If the month of the date is not between 1 and 12 .
                             If day is lower than 1 and bigger than last day of month.
        """
        if origin is None or not isinstance(origin, str):
            raise exceptions.ValidationError(
                {"origin": "origin must be a string and cannot be None"}
            )

        if destination is None or not isinstance(destination, str):
            raise exceptions.ValidationError(
                {"destination": "destination must be a string and cannot be None"}
            )

        if not QueryHandler.date_regex.match(date_from):
            raise exceptions.ValidationError(
                {"date_from": "date_from must be in the format 'YYYY-MM-DD'"}
            )

        if not QueryHandler.date_regex.match(date_to):
            raise exceptions.ValidationError(
                {"date_to": "date_to must be in the format 'YYYY-MM-DD'"}
            )
        try:
            year, month, day = map(int, date_from.split("-"))
            _, last_day_of_month = calendar.monthrange(year, month)
            if day < 1 or day > last_day_of_month:
                raise exceptions.ValidationError(
                    {
                        "date_from": f"Day must be between 1 and {last_day_of_month} for the specified month and year"
                    }
                )
        except calendar.IllegalMonthError as e:
            raise exceptions.ValidationError({"date_from": str(e)})

        try:
            year, month, day = map(int, date_to.split("-"))
            _, last_day_of_month = calendar.monthrange(year, month)
            if day < 1 or day > last_day_of_month:
                raise exceptions.ValidationError(
                    {
                        "date_to": f"Day must be between 1 and {last_day_of_month} for the specified month and year"
                    }
                )
        except calendar.IllegalMonthError as e:
            raise exceptions.ValidationError({"date_to": str(e)})

        date_from_dt = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to_dt = datetime.datetime.strptime(date_to, "%Y-%m-%d")

        if date_from_dt > date_to_dt:
            raise exceptions.ValidationError(
                {"date_from": "date_from cannot be after date_to"}
            )

    @staticmethod
    def execute_query(origin, destination, date_from, date_to):
        """
        Executes a query to retrieve average prices for a specific
        origin and destination port within a date range.

        Args:
            origin (str): The code of the origin port.
            destination (str): The code of the destination port.
            date_from (str): The start date in the format 'YYYY-MM-DD'.
            date_to (str): The end date in the format 'YYYY-MM-DD'.

        Returns:
            result (List[Tuple[str, float]]): A list of tuples containing the date and average price.
        """
        query = f"""
            SELECT day AS day,
            CASE  WHEN COUNT(*) >= 3 then
            AVG(price) ELSE NULL END AS avg_price
            FROM prices
            LEFT JOIN ports AS origin_port ON origin_port.code = prices.orig_code
            LEFT JOIN ports AS dest_port ON dest_port.code = prices.dest_code
            WHERE (origin_port.code = %s OR origin_port.parent_slug = %s)
            AND (dest_port.code = %s OR dest_port.parent_slug  = %s)
            AND day BETWEEN %s AND %s
            GROUP BY day
        """

        with connection.cursor() as cursor:
            cursor.execute(
                query, [origin, origin, destination, destination, date_from, date_to]
            )
            result = cursor.fetchall()

        return result
