from tradeapp.models import WatchlistEntry,Company

class WatchListModel:
    def filter_watchlist(self, user,company):
        try:
            watchlist_entries = WatchlistEntry.objects.filter(user=user, company=company)
            print(watchlist_entries,'1111111111111111111111')
            return [
                {
                    "company_name": entry.company.company_name,
                    "symbol": entry.company.symbol,
                    "scripcode": entry.company.scripcode,
                    "added_at": entry.added_at
                }
                for entry in watchlist_entries
            ]
        except WatchlistEntry.DoesNotExist:
            return []
        
    
    def add_to_watchlist(self, user, company_id):
        try:
            company = Company.objects.get(id=company_id)
            entry, created = WatchlistEntry.objects.get_or_create(user=user, company=company)
            return created 
        except Company.DoesNotExist:
            return None

    def remove_from_watchlist(self, user, company_id):
        try:
            entry = WatchlistEntry.objects.get(user=user, company_id=company_id)
            entry.delete()
            return True
        except WatchlistEntry.DoesNotExist:
            return False
        
    def get_user_watchlist(self, user):
        try:
            watchlist_entries = WatchlistEntry.objects.filter(user=user).select_related("company").order_by('-added_at')
            return watchlist_entries
        except WatchlistEntry.DoesNotExist:
            return []