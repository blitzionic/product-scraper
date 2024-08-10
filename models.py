from datetime import datetime

class Product:
    def __init__(self, retailer, link, brand, category, model_number, description, status=None, sku=None, listed_price=None, original_price=None, date=None):
        self.retailer = retailer # 
        self.link = link # 
        self.brand = brand # 
        self.category = category # 
        self.model_number = model_number # 
        self.sku = sku # 
        self.description = description  # 
        self.status = "Active" # other status otherwise 
        self.listed_price = 0.0 # 
        self.original_price = 0.0 # 
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'Retailer': self.retailer,
            'Link': self.link,
            'Brand': self.brand,
            'Category': self.category,
            'Model Number': self.model_number,
            'SKU': self.sku,
            'Description': self.description,
            'Status': self.status,
            'Listed Price': self.listed_price,
            'Original Price': self.original_price,
            'Date': self.date
        }