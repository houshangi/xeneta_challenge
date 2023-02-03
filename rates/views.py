from rest_framework import generics
from rest_framework.response import Response
from django.db import connection
import json


class AveragePriceList(generics.ListAPIView):
    def get(self,request):
        query = f"""
            SELECT DATE(day) AS day, AVG(price) AS avg_price
        FROM prices
        LEFT JOIN ports AS origin_port ON origin_port.code = prices.orig_code
        LEFT JOIN ports AS dest_port ON dest_port.code = prices.dest_code
        WHERE (origin_port.code = 'CNSGH' OR origin_port.parent_slug = 'asdasd')
        AND (dest_port.code = 'NOOSL' OR dest_port.parent_slug  = 'dasads')
        AND day BETWEEN DATE('2016-01-01') AND DATE('2016-01-10')
        GROUP BY DATE(day)
        HAVING COUNT(*) >= 3
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        return Response(result)