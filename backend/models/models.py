from experta import Fact, Field
from pydantic import BaseModel
from enum import Enum

# 1. Category in Enum (dropdown)
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
    # FNB = 'food_and_beverage'

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


class ProductFact(Fact): pass
class TargetCustomerFact(Fact): pass


