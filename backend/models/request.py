from pydantic import BaseModel, Field as PydanticField
from models.model import ProductType, TargetCustomer, BudgetLevel, PrimaryGoal, TimeHorizon, ContentCapability, SalesStructure, PriorityKPI

#FastAPI Pydantic data validation
class MarketingAnalysisRequest(BaseModel):
    product_type: ProductType
    target_customer: TargetCustomer
    primary_goal: PrimaryGoal
    time_horizon: TimeHorizon
    content_capability: ContentCapability
    sales_structure: SalesStructure
    priority_kpi: PriorityKPI
    raw_budget_amount: float = PydanticField(..., gt=0, description="Total marketing budget in USD") #only positive value
