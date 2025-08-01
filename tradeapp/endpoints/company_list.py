from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from django.db.models import Q
from tradeapp.controllers.company_controllers import CompanyController
import logging
logger = logging.getLogger(__name__)

class CompanyListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """API endpoint to list companies with optional filters (symbol, scripcode, search) and pagination."""

    def __init__(self):
        self.company_controller = CompanyController()

    def get(self, request):
        try:
            symbol = request.GET.get('symbol', None)
            scripcode = request.GET.get('scripcode', None)
            search = request.GET.get('search', None)
            # if not symbol and not scripcode and not search:
            #     logger.error("At least one filter (symbol, scripcode, search) is required")
            #     return Response({"error": "At least one filter (symbol, scripcode, search) is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                page = int(request.GET.get('page', 1))
                if page < 1:
                    logger.error("Page must be ≥ 1")
                    raise ValueError("Page must be ≥ 1")
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            try:
                per_page = int(request.GET.get('per_page', 10))
                if per_page > 100:
                    raise ValueError("per_page max is 100")
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Input validation
            if symbol and len(symbol) > 10:
                logger.error("Symbol too long")
                return Response({"error": "Symbol too long"}, status=status.HTTP_400_BAD_REQUEST)

            if scripcode and not scripcode.isdigit():
                logger.error("Scripcode must be numeric")
                return Response({"error": "Scripcode must be numeric"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                data = self.company_controller.get_filtered_companies(symbol, scripcode, search)
                logger.info(f"Fetched {len(data)} companies")
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error fetching data: {str(e)}")
                return Response(
                    {"error": "Error fetching data", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            logger.exception("Internal server error")
            return Response(
                {"error": "Internal server error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
