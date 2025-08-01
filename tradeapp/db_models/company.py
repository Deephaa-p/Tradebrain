from tradeapp.models import Company
from django.db.models import Q
from django.core.paginator import Paginator
class CompanyModel:
    def get_filtered_companies(self,symbol=None, scripcode=None, search=None,page=1,per_page=10):
        try:
            qs = Company.objects.all()
            
            if symbol:
                qs = qs.filter(symbol__iexact=symbol)
            if scripcode:
                qs = qs.filter(scripcode=scripcode)

            if search:
                qs = qs.filter(
                    Q(company_name__icontains=search) |
                    Q(symbol__icontains=search) |
                    Q(scripcode__icontains=search)
                )
            paginator = Paginator(qs, per_page)
            page_obj = paginator.get_page(page)

            results = [
                {
                    "company_name": obj.company_name,
                    "symbol": obj.symbol,
                    "scripcode": obj.scripcode
                }
                for obj in page_obj
            ]

            return {
                "total": paginator.count,
                "pages": paginator.num_pages,
                "page": page_obj.number,
                "results": results
            }

        except Company.DoesNotExist:
            return Company.objects.none()
        
    def get_company_by_id(self, company_id):
        try:
            result=Company.objects.get(id=company_id)
            company_data = {
            "company_id": result.id,
            "company_name": result.company_name,
            "symbol": result.symbol,
            "scripcode": result.scripcode
        }
            return company_data
        except Company.DoesNotExist:
            return {}
