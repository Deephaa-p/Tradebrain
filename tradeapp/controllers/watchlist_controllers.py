from tradeapp.db_models.watch_list import WatchListModel

class WatchListController:
    def filter_watchlist(self, user, company):
       watchlist_entries = WatchListModel()
       watch_list_data = watchlist_entries.filter_watchlist(user, company)
       return watch_list_data
            
        
    def add_to_watchlist(self, user, company):
        entry =  WatchListModel()
        watch_list_data = entry.add_to_watchlist(user, company)
        return watch_list_data
    
    def remove_from_watchlist(self, user, company_id):
        entry = WatchListModel()
        removed = entry.remove_from_watchlist(user, company_id)
        return removed
    
    def get_user_watchlist(self, user):
        watchlist_entries = WatchListModel()
        watch_list_data = watchlist_entries.get_user_watchlist(user)
        return watch_list_data