from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tradeapp.controllers.watchlist_controllers import WatchListController
from tradeapp.controllers.company_controllers import CompanyController
from django.core.paginator import Paginator
import logging
logger = logging.getLogger(__name__)

class AddToWatchlistView(APIView):
    permission_classes = [IsAuthenticated]
    """API endpoint to manage user watchlist.
    Allows users to add, remove, and view companies in their watchlist.
    - POST: Add a company to the watchlist.
    - DELETE: Remove a company from the watchlist.
    - GET: Retrieve the user's watchlist with pagination."""

    def __init__(self):
        self.watchlist_controller = WatchListController()
        self.company_controller = CompanyController()

    def post(self, request):
        try:
            company_id = request.data.get("company_id")
            if not company_id:
                logger.error("company_id is required")
                return Response({"message": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            company_data = self.company_controller.get_company_by_id(company_id)
            if not company_data:
                logger.error("Company not found")
                return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

            watch_list_data = self.watchlist_controller.filter_watchlist(request.user, company_id)
            if watch_list_data:
                logger.error("Company already in watchlist")
                return Response({"message": "Company already in watchlist"}, status=status.HTTP_400_BAD_REQUEST)

            add_watch_list= self.watchlist_controller.add_to_watchlist(request.user, company_id)
            if add_watch_list:
                logger.info(f"Company {company_data['company_name']} added to watchlist for user {request.user.username}")
                return Response({"message": "Company added to watchlist"}, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Failed to add company {company_data['company_name']} to watchlist for user {request.user.username}")
                return Response({"message": "Failed to add company to watchlist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception("Unexpected error")
            return Response({"message": "Unexpected error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request):
        """Remove a company from the watchlist."""
        try:
            company_id = request.data.get("company_id")
            if not company_id:
                logger.error("company_id is required")
                return Response({"message": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            company = self.company_controller.get_company_by_id(company_id)
            if not company:
                logger.error("Company not found")
                return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        
            removed = self.watchlist_controller.remove_from_watchlist(request.user, company_id)
            if removed:
                logger.info(f"Company {company['company_name']} removed from watchlist for user {request.user.username}")
                return Response({"message": "Company removed from watchlist"}, status=status.HTTP_200_OK)

            return Response({"message": "Company not in watchlist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error")
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            user = request.user
            watchlist_qs = self.watchlist_controller.get_user_watchlist(user)

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
                    logger.error("per_page max is 100")
                    raise ValueError("per_page max is 100")
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            paginator = Paginator(watchlist_qs, per_page)
            page_obj = paginator.get_page(page)

            results = [
                {
                    "company_name": entry.company.company_name,
                    "symbol": entry.company.symbol,
                    "scripcode": entry.company.scripcode,
                    "added_at": entry.added_at
                }
                for entry in page_obj
            ]
            logger.info(f"Fetched {len(results)} companies from watchlist for user {user.username}")
            return Response({
                "total": paginator.count,
                "pages": paginator.num_pages,
                "page": page_obj.number,
                "results": results
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Error fetching user watchlist")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)