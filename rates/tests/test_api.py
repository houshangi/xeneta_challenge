from django.test import TestCase
from django.db import connection


# Create your tests here.
class APITestCase(TestCase):
    def test_one(self):
        with connection.cursor() as cursor:
            cursor.execute("select * from prices")
