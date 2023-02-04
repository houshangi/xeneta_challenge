from rest_framework import generics, exceptions
from rest_framework.response import Response
from .serializers import AveragePriceSerializer
from .queries import QueryHandler
from django.db.utils import DataError


class AveragePriceList(generics.ListAPIView):
    """
    Class for getting average price for the given origin, destination, and date range.

    Class attributes:
    serializer_class (AveragePriceSerializer): Serializer class for the result.

    Methods:
    get: Retrieves the average price by making a query to the database using QueryHandler class.

    Raises:
    DataError: If date is not in proper format 'YYYY-MM-DD'.
    """

    serializer_class = AveragePriceSerializer

    def get(self, request):
        origin = request.query_params.get("origin")
        destination = request.query_params.get("destination")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        QueryHandler.validate_params(origin, destination, date_from, date_to)
        try:
            result = QueryHandler.execute_query(origin, destination, date_from, date_to)

            result_list = [{"day": r[0], "average_price": r[1]} for r in result]

            serialized_result = AveragePriceSerializer(result_list, many=True)

            return Response(serialized_result.data)
        except DataError:
            return Response(
                {
                    "date_error": "in YYYY-MM-DD format all days must "
                    "be between 1 and 31 and"
                    " all months must be between 1 and 12 "
                },
                status=400,
            )
