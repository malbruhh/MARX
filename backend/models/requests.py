from pydantic import BaseModel
from models.models import ProductType, TargetCustomer

class MarketingAnalysisRequest(BaseModel):
    product_type: ProductType
    target_customer: TargetCustomer