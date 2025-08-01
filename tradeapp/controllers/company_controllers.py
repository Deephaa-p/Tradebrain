from tradeapp.db_models.company import CompanyModel

class CompanyController:

    def get_filtered_companies(self, symbol, scripcode, search):
        
        company_model = CompanyModel()
        company_data = company_model.get_filtered_companies(symbol, scripcode, search)
        return company_data
    
    def get_company_by_id(self, company_id):
        company_model = CompanyModel()
        company_data = company_model.get_company_by_id(company_id)
        return company_data