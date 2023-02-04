from rest_framework import generics, exceptions
from rest_framework.response import Response
from .serializers import AveragePriceSerializer
from .queries import QueryHandler


class AveragePriceList(generics.ListAPIView):
    """
    Class for getting average price for the given origin, destination, and date range.

    Class attributes:
    serializer_class (AveragePriceSerializer): Serializer class for the result.

    Methods:
    get: Retrieves the average price
    by making a query to the database using QueryHandler class.

    """

    serializer_class = AveragePriceSerializer

    def get(self, request):
        origin = request.query_params.get("origin")
        destination = request.query_params.get("destination")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        QueryHandler.validate_params(origin, destination, date_from, date_to)

        result = QueryHandler.execute_query(origin, destination, date_from, date_to)

        # convert from list of tuples to dict
        result_list = [{"day": r[0], "average_price": r[1]} for r in result]

        serialized_result = AveragePriceSerializer(result_list, many=True)

        return Response(serialized_result.data)
