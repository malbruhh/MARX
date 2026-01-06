from experta import Fact, Field
from enum import Enum

# Category in Enum (dropdown)
class ProductType(str, Enum):
    B2B_SAAS = 'b2b_enterprise_saas'
    B2C_RETAIL = 'b2c_retail_goods'
    LOCAL_SERVICE = 'local_service'
    CONSULTING = 'high_end_consulting'
    DIGITAL_PRODUCT = 'digital_info_product'
    FMCG = 'fast_moving_consumer_goods'
    TECHNICAL_TOOLS = 'niche_technical_tools'
    HOSPITALITY = 'hospitality'
    SUBSCRIPTION = 'subscription_recurring'

class TargetCustomer(str, Enum):
    B2B_LARGE = 'large_enterprise'
    B2B_SME = 'small_to_medium_enterprise'
    GEN_Z = 'gen_z'
    MILLENIAL = 'millenial'
    SENIOR = 'senior'
    LOCAL = 'local_community'
    NICHE = 'niche_industry'
    BUDGET_SHOPPER = 'budget_shopper'
    LUXURY = 'luxury'

class BudgetLevel(str, Enum):
    MICRO = 'micro' # 0 - 1k
    SMALL = 'low' # 1k - 10k
    MEDIUM = 'medium' # 10k - 100k
    LARGE = 'high' # 100k - 1M
    ENTERPRISE = 'enterprise' # 1M+

class PrimaryGoal(str, Enum):
    AWARENESS = "brand_awareness"
    LEAD_GEN = "immediate_lead_generation"
    RETENTION = "customer_retention_loyalty"

class TimeHorizon(str, Enum):
    SHORT = "short_term"   # 1-3 months
    MEDIUM = "medium_term" # 3-6 months
    LONG = "long_term"     # 6+ months

class ContentCapability(str, Enum):
    HIGH = "high_capability"
    MEDIUM = "medium_capability"
    LOW = "low_capability"

class SalesStructure(str, Enum):
    AUTOMATED = "automated_ecommerce"
    SALES_TEAM = "dedicated_sales_team"
    OWNER_DRIVEN = "owner_driven"

class PriorityKPI(str, Enum):
    CR = "conversion_rate"
    CLV = "customer_lifetime_value"
    TRAFFIC = "organic_traffic_impressions"
    CPA = "cost_per_acquisition"
    SQL = "sales_qualified_leads"

# Knowledge Base Scheme (Experta Facts)
class ProductFact(Fact):
    """Product type fact"""
    pass

class TargetCustomerFact(Fact):
    """Target customer fact"""
    pass

class BudgetLevelFact(Fact):
    """Predefined budget range fact"""
    pass

class RawBudget(Fact):
    """Raw budget amount fact"""
    pass

class PrimaryGoalFact(Fact):
    """Primary goal fact"""
    pass

class TimeHorizonFact(Fact):
    """Time horizon fact"""
    pass

class ContentCapabilityFact(Fact):
    """Content capability fact"""
    pass

class SalesStructureFact(Fact):
    """Sales structure fact"""
    pass

class PriorityKPIFact(Fact):
    """Priority KPI fact"""
    pass