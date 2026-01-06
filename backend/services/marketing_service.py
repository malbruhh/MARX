# Convert Pydantic data (JSON) into KnowledgeBase
from experta import KnowledgeEngine, Rule, MATCH, AND, OR
from models.model import *
from models.request import MarketingAnalysisRequest

class MarketingEngine(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.marketing_strategy = "Standard Marketing Mix Recommended."  # Changed from 'strategy' to 'marketing_strategy'

    # Budget classification rules
    @Rule(RawBudget(amount=MATCH.a))
    def classify_budget(self, a):
        if a <= 1000:
            self.declare(BudgetLevelFact(tier=BudgetLevel.MICRO.value))
        elif a <= 10000:
            self.declare(BudgetLevelFact(tier=BudgetLevel.SMALL.value))
        elif a <= 100000:
            self.declare(BudgetLevelFact(tier=BudgetLevel.MEDIUM.value))
        elif a <= 1000000:
            self.declare(BudgetLevelFact(tier=BudgetLevel.LARGE.value))
        else:
            self.declare(BudgetLevelFact(tier=BudgetLevel.ENTERPRISE.value))

    # Strategy rules - B2B SaaS
    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value),
        BudgetLevelFact(tier=BudgetLevel.MICRO.value)
    )
    def saas_micro_strategy(self):
        self.marketing_strategy = 'B2B SaaS Micro Budget Strategy: Focus on organic content marketing, LinkedIn presence, and community building. Leverage free tools and platforms.'

    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value),
        BudgetLevelFact(tier=BudgetLevel.SMALL.value)
    )
    def saas_small_strategy(self):
        self.marketing_strategy = 'B2B SaaS Small Budget Strategy: Start with targeted Google Ads, basic content marketing, and email campaigns. Focus on SEO and thought leadership.'

    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value),
        BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
    )
    def saas_medium_strategy(self):
        self.marketing_strategy = 'B2B SaaS Medium Budget Strategy: Scale with multi-channel campaigns including paid search, content syndication, webinars, and account-based marketing.'

    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value),
        BudgetLevelFact(tier=BudgetLevel.LARGE.value)
    )
    def saas_large_strategy(self):
        self.marketing_strategy = 'B2B SaaS Large Budget Strategy: Full-scale enterprise marketing with dedicated sales teams, conferences, partnerships, and comprehensive demand generation.'

    # B2C Retail strategies
    @Rule(
        ProductFact(product_type=ProductType.B2C_RETAIL.value),
        BudgetLevelFact(tier=BudgetLevel.MICRO.value),
        PrimaryGoalFact(goal=PrimaryGoal.AWARENESS.value)
    )
    def retail_micro_awareness_strategy(self):
        self.marketing_strategy = 'B2C Retail Micro Budget + Awareness Strategy: Use social media (Instagram/TikTok), user-generated content, and local partnerships. Focus on viral content.'

    @Rule(
        ProductFact(product_type=ProductType.B2C_RETAIL.value),
        BudgetLevelFact(tier=BudgetLevel.SMALL.value)
    )
    def retail_small_strategy(self):
        self.marketing_strategy = 'B2C Retail Small Budget Strategy: Combine social media ads, influencer partnerships, and email marketing. Test different channels for ROI.'

    @Rule(
        ProductFact(product_type=ProductType.B2C_RETAIL.value),
        BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
    )
    def retail_medium_strategy(self):
        self.marketing_strategy = 'B2C Retail Medium Budget Strategy: Scale winning channels, add display advertising, retargeting, and seasonal campaigns.'

    # Local Service strategies
    @Rule(
        ProductFact(product_type=ProductType.LOCAL_SERVICE.value),
        BudgetLevelFact(tier=BudgetLevel.MICRO.value)
    )
    def local_service_micro_strategy(self):
        self.marketing_strategy = 'Local Service Micro Budget Strategy: Focus on Google My Business, local SEO, community engagement, and word-of-mouth referrals.'

    @Rule(
        ProductFact(product_type=ProductType.LOCAL_SERVICE.value),
        BudgetLevelFact(tier=BudgetLevel.SMALL.value)
    )
    def local_service_small_strategy(self):
        self.marketing_strategy = 'Local Service Small Budget Strategy: Add local PPC ads, directory listings, review management, and basic content marketing.'

    # Digital Product strategies
    @Rule(
        ProductFact(product_type=ProductType.DIGITAL_PRODUCT.value),
        BudgetLevelFact(tier=BudgetLevel.SMALL.value),
        PrimaryGoalFact(goal=PrimaryGoal.LEAD_GEN.value)
    )
    def digital_product_lead_gen_strategy(self):
        self.marketing_strategy = 'Digital Product Lead Generation Strategy: Use content marketing, SEO, lead magnets, email funnels, and retargeting ads to capture and nurture leads.'

    @Rule(
        ProductFact(product_type=ProductType.DIGITAL_PRODUCT.value),
        BudgetLevelFact(tier=BudgetLevel.MICRO.value)
    )
    def digital_product_micro_strategy(self):
        self.marketing_strategy = 'Digital Product Micro Budget Strategy: Focus on organic content, SEO, free webinars, and building an email list through valuable free resources.'

    # Consulting strategies
    @Rule(
        ProductFact(product_type=ProductType.CONSULTING.value)
    )
    def consulting_strategy(self):
        self.marketing_strategy = 'High-End Consulting Strategy: Focus on thought leadership, speaking engagements, published research, networking, and high-touch relationship building.'

    # FMCG strategies
    @Rule(
        ProductFact(product_type=ProductType.FMCG.value),
        BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
    )
    def fmcg_medium_strategy(self):
        self.marketing_strategy = 'FMCG Medium Budget Strategy: Focus on retail partnerships, in-store promotions, regional advertising, and sampling campaigns.'

    # Technical Tools strategies
    @Rule(
        ProductFact(product_type=ProductType.TECHNICAL_TOOLS.value)
    )
    def technical_tools_strategy(self):
        self.marketing_strategy = 'Niche Technical Tools Strategy: Developer marketing, technical documentation, API integrations, community building, and developer advocacy.'

    # Hospitality strategies
    @Rule(
        ProductFact(product_type=ProductType.HOSPITALITY.value)
    )
    def hospitality_strategy(self):
        self.marketing_strategy = 'Hospitality Strategy: OTA optimization, local SEO, reputation management, social proof, and guest experience marketing.'

    # Subscription strategies
    @Rule(
        ProductFact(product_type=ProductType.SUBSCRIPTION.value),
        PrimaryGoalFact(goal=PrimaryGoal.RETENTION.value)
    )
    def subscription_retention_strategy(self):
        self.marketing_strategy = 'Subscription Retention Strategy: Focus on reducing churn, customer success programs, engagement campaigns, and maximizing customer lifetime value.'

    
def run_analysis_service(request: MarketingAnalysisRequest):
    """
    Run marketing analysis using the expert system
    """
    try:
        engine = MarketingEngine()
        engine.reset()
        
        # Declare facts with .value to get string values from enums
        engine.declare(ProductFact(product_type=request.product_type.value))
        engine.declare(RawBudget(amount=request.raw_budget_amount))
        engine.declare(TargetCustomerFact(customer=request.target_customer.value))
        engine.declare(PrimaryGoalFact(goal=request.primary_goal.value))
        engine.declare(TimeHorizonFact(horizon=request.time_horizon.value))
        engine.declare(ContentCapabilityFact(capability=request.content_capability.value))
        engine.declare(SalesStructureFact(structure=request.sales_structure.value))
        engine.declare(PriorityKPIFact(kpi=request.priority_kpi.value))
        
        # Run the engine
        engine.run()
        
        return engine.marketing_strategy if engine.marketing_strategy else "Standard Marketing Mix Recommended."
    
    except Exception as e:
        # Re-raise with more context
        import traceback
        error_detail = f"Error in marketing analysis engine: {str(e)}\n{traceback.format_exc()}"
        raise Exception(error_detail)