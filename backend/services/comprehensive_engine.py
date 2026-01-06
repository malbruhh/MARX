"""
Comprehensive Marketing Expert System with Layered Forward Chaining
100+ rules organized in 10 layers for systematic inference
"""
from experta import KnowledgeEngine, Rule, MATCH, AND, OR, NOT
from models.model import *
from models.intermediate_facts import *
from models.output import *
from typing import List, Dict

class ComprehensiveMarketingEngine(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        # Storage for recommendations
        self.channel_recommendations = []
        self.content_recommendations = []
        self.quick_wins = []
        self.short_term_actions = []
        self.medium_term_actions = []
        self.long_term_actions = []
        self.primary_kpis = []
        self.secondary_kpis = []
        self.risks = []
        self.budget_categories = {}
        self.cost_optimization_tips = []
        self.scaling_triggers = []
        self.recommended_tools = []
        self.required_capabilities = []
        self.potential_partners = []
        self.content_themes = []
        self.competitive_advantages = []
        self.strategy_summary = ""
        self.strategic_positioning = ""
        self.channel_mix_rationale = ""
        self.messaging_focus = ""
        self.differentiation_strategy = ""
        self.scaling_strategy = ""

    # ==================== LAYER 0: Budget Classification ====================

    @Rule(RawBudget(amount=MATCH.a))
    def classify_budget(self, a):
        """Rule 1: Classify budget into tiers"""
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

    # ==================== LAYER 1: Market Context Analysis ====================

    @Rule(ProductFact(product_type=ProductType.B2B_SAAS.value))
    def market_maturity_b2b_saas(self):
        """Rule 2: B2B SaaS market maturity"""
        self.declare(MarketMaturityFact(level="growth"))
        self.declare(CompetitionLevelFact(level="high"))

    @Rule(ProductFact(product_type=ProductType.B2C_RETAIL.value))
    def market_maturity_b2c_retail(self):
        """Rule 3: B2C Retail market maturity"""
        self.declare(MarketMaturityFact(level="mature"))
        self.declare(CompetitionLevelFact(level="very_high"))

    @Rule(ProductFact(product_type=ProductType.LOCAL_SERVICE.value))
    def market_maturity_local_service(self):
        """Rule 4: Local service market"""
        self.declare(MarketMaturityFact(level="mature"))
        self.declare(CompetitionLevelFact(level="moderate"))

    @Rule(ProductFact(product_type=ProductType.CONSULTING.value))
    def market_maturity_consulting(self):
        """Rule 5: Consulting market"""
        self.declare(MarketMaturityFact(level="mature"))
        self.declare(CompetitionLevelFact(level="high"))

    @Rule(ProductFact(product_type=ProductType.DIGITAL_PRODUCT.value))
    def market_maturity_digital_product(self):
        """Rule 6: Digital product market"""
        self.declare(MarketMaturityFact(level="growth"))
        self.declare(CompetitionLevelFact(level="high"))

    @Rule(ProductFact(product_type=ProductType.FMCG.value))
    def market_maturity_fmcg(self):
        """Rule 7: FMCG market"""
        self.declare(MarketMaturityFact(level="saturated"))
        self.declare(CompetitionLevelFact(level="very_high"))

    @Rule(ProductFact(product_type=ProductType.TECHNICAL_TOOLS.value))
    def market_maturity_technical_tools(self):
        """Rule 8: Technical tools market"""
        self.declare(MarketMaturityFact(level="growth"))
        self.declare(CompetitionLevelFact(level="moderate"))

    @Rule(ProductFact(product_type=ProductType.HOSPITALITY.value))
    def market_maturity_hospitality(self):
        """Rule 9: Hospitality market"""
        self.declare(MarketMaturityFact(level="mature"))
        self.declare(CompetitionLevelFact(level="high"))

    @Rule(ProductFact(product_type=ProductType.SUBSCRIPTION.value))
    def market_maturity_subscription(self):
        """Rule 10: Subscription market"""
        self.declare(MarketMaturityFact(level="growth"))
        self.declare(CompetitionLevelFact(level="high"))

    # Customer Acquisition Complexity Rules

    @Rule(
        TargetCustomerFact(customer=TargetCustomer.B2B_LARGE.value)
    )
    def acquisition_complexity_enterprise(self):
        """Rule 11: Enterprise acquisition complexity"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="very_complex"))
        self.declare(SalesCycleFact(cycle="very_long"))

    @Rule(
        TargetCustomerFact(customer=TargetCustomer.B2B_SME.value)
    )
    def acquisition_complexity_sme(self):
        """Rule 12: SME acquisition complexity"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="complex"))
        self.declare(SalesCycleFact(cycle="medium"))

    @Rule(
        OR(
            TargetCustomerFact(customer=TargetCustomer.GEN_Z.value),
            TargetCustomerFact(customer=TargetCustomer.MILLENIAL.value)
        )
    )
    def acquisition_complexity_digital_natives(self):
        """Rule 13: Digital natives acquisition"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="moderate"))
        self.declare(SalesCycleFact(cycle="short"))

    @Rule(TargetCustomerFact(customer=TargetCustomer.SENIOR.value))
    def acquisition_complexity_senior(self):
        """Rule 14: Senior customer acquisition"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="moderate"))
        self.declare(SalesCycleFact(cycle="medium"))

    @Rule(TargetCustomerFact(customer=TargetCustomer.LOCAL.value))
    def acquisition_complexity_local(self):
        """Rule 15: Local community acquisition"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="simple"))
        self.declare(SalesCycleFact(cycle="short"))

    @Rule(TargetCustomerFact(customer=TargetCustomer.NICHE.value))
    def acquisition_complexity_niche(self):
        """Rule 16: Niche industry acquisition"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="complex"))
        self.declare(SalesCycleFact(cycle="long"))

    @Rule(TargetCustomerFact(customer=TargetCustomer.BUDGET_SHOPPER.value))
    def acquisition_complexity_budget(self):
        """Rule 17: Budget shopper acquisition"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="simple"))
        self.declare(SalesCycleFact(cycle="immediate"))

    @Rule(TargetCustomerFact(customer=TargetCustomer.LUXURY.value))
    def acquisition_complexity_luxury(self):
        """Rule 18: Luxury customer acquisition"""
        self.declare(CustomerAcquisitionComplexityFact(complexity="complex"))
        self.declare(SalesCycleFact(cycle="long"))

    # ==================== LAYER 2: Strategic Direction ====================

    @Rule(
        PrimaryGoalFact(goal=PrimaryGoal.AWARENESS.value),
        TimeHorizonFact(horizon=TimeHorizon.LONG.value)
    )
    def strategic_approach_brand_building(self):
        """Rule 19: Brand building strategy"""
        self.declare(StrategicApproachFact(approach="niche_domination"))
        self.declare(MarketingFocusFact(focus="brand_building"))

    @Rule(
        PrimaryGoalFact(goal=PrimaryGoal.LEAD_GEN.value),
        TimeHorizonFact(horizon=TimeHorizon.SHORT.value)
    )
    def strategic_approach_aggressive_growth(self):
        """Rule 20: Aggressive growth strategy"""
        self.declare(StrategicApproachFact(approach="aggressive_growth"))
        self.declare(MarketingFocusFact(focus="acquisition"))

    @Rule(
        PrimaryGoalFact(goal=PrimaryGoal.RETENTION.value)
    )
    def strategic_approach_retention(self):
        """Rule 21: Retention-focused strategy"""
        self.declare(StrategicApproachFact(approach="defensive"))
        self.declare(MarketingFocusFact(focus="retention"))

    @Rule(
        PrimaryGoalFact(goal=PrimaryGoal.LEAD_GEN.value),
        TimeHorizonFact(horizon=TimeHorizon.MEDIUM.value)
    )
    def strategic_approach_steady_growth(self):
        """Rule 22: Steady growth strategy"""
        self.declare(StrategicApproachFact(approach="steady_growth"))
        self.declare(MarketingFocusFact(focus="acquisition"))

    @Rule(
        PrimaryGoalFact(goal=PrimaryGoal.AWARENESS.value),
        CompetitionLevelFact(level="very_high")
    )
    def strategic_approach_differentiation(self):
        """Rule 23: Differentiation in crowded market"""
        self.declare(StrategicApproachFact(approach="niche_domination"))
        self.declare(MessagingAngleFact(angle="differentiation"))

    # ==================== LAYER 3: Channel Suitability - Paid Search ====================

    @Rule(
        AND(
            OR(
                ProductFact(product_type=ProductType.B2B_SAAS.value),
                ProductFact(product_type=ProductType.LOCAL_SERVICE.value)
            ),
            BudgetLevelFact(tier=BudgetLevel.SMALL.value),
            PrimaryGoalFact(goal=PrimaryGoal.LEAD_GEN.value)
        )
    )
    def channel_paid_search_high_intent(self):
        """Rule 24: Paid search for high-intent products"""
        self.declare(ChannelPriorityFact(
            channel="paid_search",
            priority=1,
            budget_percent=35.0
        ))
        self.declare(ChannelReadinessFact(channel="paid_search", readiness="ready"))

    @Rule(
        BudgetLevelFact(tier=BudgetLevel.MICRO.value)
    )
    def channel_paid_search_limited_budget(self):
        """Rule 25: Limited paid search for micro budgets"""
        self.declare(ChannelPriorityFact(
            channel="paid_search",
            priority=4,
            budget_percent=10.0
        ))

    @Rule(
        AND(
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value),
            PriorityKPIFact(kpi=PriorityKPI.CPA.value)
        )
    )
    def channel_paid_search_performance_focus(self):
        """Rule 26: Paid search for CPA optimization"""
        self.declare(ChannelPriorityFact(
            channel="paid_search",
            priority=2,
            budget_percent=30.0
        ))

    # Channel Suitability - Paid Social

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2C_RETAIL.value),
            OR(
                TargetCustomerFact(customer=TargetCustomer.GEN_Z.value),
                TargetCustomerFact(customer=TargetCustomer.MILLENIAL.value)
            )
        )
    )
    def channel_paid_social_b2c_youth(self):
        """Rule 27: Paid social for B2C targeting youth"""
        self.declare(ChannelPriorityFact(
            channel="paid_social",
            priority=1,
            budget_percent=40.0
        ))
        self.declare(ChannelReadinessFact(channel="paid_social", readiness="ready"))

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2B_SAAS.value),
            TargetCustomerFact(customer=TargetCustomer.B2B_SME.value),
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
        )
    )
    def channel_linkedin_b2b(self):
        """Rule 28: LinkedIn for B2B SME"""
        self.declare(ChannelPriorityFact(
            channel="paid_social",
            priority=2,
            budget_percent=25.0
        ))

    @Rule(
        AND(
            PrimaryGoalFact(goal=PrimaryGoal.AWARENESS.value),
            BudgetLevelFact(tier=BudgetLevel.LARGE.value)
        )
    )
    def channel_paid_social_awareness(self):
        """Rule 29: Paid social for awareness at scale"""
        self.declare(ChannelPriorityFact(
            channel="paid_social",
            priority=1,
            budget_percent=30.0
        ))

    # Channel Suitability - Organic SEO

    @Rule(
        AND(
            TimeHorizonFact(horizon=TimeHorizon.LONG.value),
            PriorityKPIFact(kpi=PriorityKPI.TRAFFIC.value)
        )
    )
    def channel_organic_seo_longterm(self):
        """Rule 30: SEO for long-term traffic"""
        self.declare(ChannelPriorityFact(
            channel="organic_seo",
            priority=1,
            budget_percent=25.0
        ))

    @Rule(
        ContentCapabilityFact(capability=ContentCapability.HIGH.value)
    )
    def channel_organic_seo_content_strength(self):
        """Rule 31: SEO when content capability is high"""
        self.declare(ChannelPriorityFact(
            channel="organic_seo",
            priority=2,
            budget_percent=20.0
        ))
        self.declare(ChannelReadinessFact(channel="organic_seo", readiness="ready"))

    @Rule(
        AND(
            BudgetLevelFact(tier=BudgetLevel.MICRO.value),
            TimeHorizonFact(horizon=TimeHorizon.LONG.value)
        )
    )
    def channel_organic_seo_budget_constrained(self):
        """Rule 32: SEO for budget-constrained long-term plays"""
        self.declare(ChannelPriorityFact(
            channel="organic_seo",
            priority=1,
            budget_percent=40.0
        ))

    # Channel Suitability - Email Marketing

    @Rule(
        PrimaryGoalFact(goal=PrimaryGoal.RETENTION.value)
    )
    def channel_email_retention(self):
        """Rule 33: Email for retention"""
        self.declare(ChannelPriorityFact(
            channel="email_marketing",
            priority=1,
            budget_percent=20.0
        ))

    @Rule(
        AND(
            SalesCycleFact(cycle="long"),
            PrimaryGoalFact(goal=PrimaryGoal.LEAD_GEN.value)
        )
    )
    def channel_email_nurture(self):
        """Rule 34: Email for long sales cycle nurture"""
        self.declare(ChannelPriorityFact(
            channel="email_marketing",
            priority=2,
            budget_percent=15.0
        ))

    @Rule(
        ProductFact(product_type=ProductType.SUBSCRIPTION.value)
    )
    def channel_email_subscription(self):
        """Rule 35: Email critical for subscriptions"""
        self.declare(ChannelPriorityFact(
            channel="email_marketing",
            priority=1,
            budget_percent=25.0
        ))

    # Channel Suitability - Content Marketing

    @Rule(
        AND(
            ContentCapabilityFact(capability=ContentCapability.HIGH.value),
            OR(
                ProductFact(product_type=ProductType.B2B_SAAS.value),
                ProductFact(product_type=ProductType.CONSULTING.value)
            )
        )
    )
    def channel_content_thought_leadership(self):
        """Rule 36: Content marketing for thought leadership"""
        self.declare(ChannelPriorityFact(
            channel="content_marketing",
            priority=1,
            budget_percent=30.0
        ))

    @Rule(
        AND(
            PrimaryGoalFact(goal=PrimaryGoal.AWARENESS.value),
            TimeHorizonFact(horizon=TimeHorizon.LONG.value)
        )
    )
    def channel_content_brand_building(self):
        """Rule 37: Content for brand building"""
        self.declare(ChannelPriorityFact(
            channel="content_marketing",
            priority=2,
            budget_percent=25.0
        ))

    # Channel Suitability - Influencer Marketing

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2C_RETAIL.value),
            OR(
                TargetCustomerFact(customer=TargetCustomer.GEN_Z.value),
                TargetCustomerFact(customer=TargetCustomer.MILLENIAL.value)
            ),
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
        )
    )
    def channel_influencer_b2c_youth(self):
        """Rule 38: Influencer marketing for B2C youth"""
        self.declare(ChannelPriorityFact(
            channel="influencer",
            priority=2,
            budget_percent=20.0
        ))

    # Channel Suitability - Events & Webinars

    @Rule(
        AND(
            OR(
                ProductFact(product_type=ProductType.B2B_SAAS.value),
                ProductFact(product_type=ProductType.CONSULTING.value)
            ),
            BudgetLevelFact(tier=BudgetLevel.LARGE.value)
        )
    )
    def channel_events_b2b_enterprise(self):
        """Rule 39: Events for B2B enterprise"""
        self.declare(ChannelPriorityFact(
            channel="events_webinars",
            priority=2,
            budget_percent=20.0
        ))

    @Rule(
        AND(
            CustomerAcquisitionComplexityFact(complexity="very_complex"),
            SalesCycleFact(cycle="very_long")
        )
    )
    def channel_events_complex_sales(self):
        """Rule 40: Events for complex sales"""
        self.declare(ChannelPriorityFact(
            channel="events_webinars",
            priority=1,
            budget_percent=25.0
        ))

    # Channel Suitability - Community Building

    @Rule(
        AND(
            ProductFact(product_type=ProductType.TECHNICAL_TOOLS.value),
            TargetCustomerFact(customer=TargetCustomer.NICHE.value)
        )
    )
    def channel_community_technical(self):
        """Rule 41: Community for technical/niche products"""
        self.declare(ChannelPriorityFact(
            channel="community",
            priority=1,
            budget_percent=15.0
        ))

    @Rule(
        ProductFact(product_type=ProductType.LOCAL_SERVICE.value)
    )
    def channel_community_local(self):
        """Rule 42: Community for local services"""
        self.declare(ChannelPriorityFact(
            channel="community",
            priority=2,
            budget_percent=10.0
        ))

    # Channel Suitability - Local SEO

    @Rule(
        AND(
            ProductFact(product_type=ProductType.LOCAL_SERVICE.value),
            TargetCustomerFact(customer=TargetCustomer.LOCAL.value)
        )
    )
    def channel_local_seo_service(self):
        """Rule 43: Local SEO for local services"""
        self.declare(ChannelPriorityFact(
            channel="local_seo",
            priority=1,
            budget_percent=30.0
        ))

    @Rule(
        ProductFact(product_type=ProductType.HOSPITALITY.value)
    )
    def channel_local_seo_hospitality(self):
        """Rule 44: Local SEO for hospitality"""
        self.declare(ChannelPriorityFact(
            channel="local_seo",
            priority=1,
            budget_percent=25.0
        ))

    # Channel Suitability - Retargeting

    @Rule(
        AND(
            PriorityKPIFact(kpi=PriorityKPI.CR.value),
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
        )
    )
    def channel_retargeting_conversion(self):
        """Rule 45: Retargeting for conversion optimization"""
        self.declare(ChannelPriorityFact(
            channel="retargeting",
            priority=2,
            budget_percent=15.0
        ))

    @Rule(
        SalesCycleFact(cycle="medium")
    )
    def channel_retargeting_nurture(self):
        """Rule 46: Retargeting for medium sales cycles"""
        self.declare(ChannelPriorityFact(
            channel="retargeting",
            priority=3,
            budget_percent=10.0
        ))

    # Channel Suitability - Referral Programs

    @Rule(
        AND(
            PriorityKPIFact(kpi=PriorityKPI.CLV.value),
            PrimaryGoalFact(goal=PrimaryGoal.RETENTION.value)
        )
    )
    def channel_referral_clv_focus(self):
        """Rule 47: Referral programs for CLV"""
        self.declare(ChannelPriorityFact(
            channel="referral",
            priority=2,
            budget_percent=10.0
        ))

    @Rule(
        ProductFact(product_type=ProductType.SUBSCRIPTION.value)
    )
    def channel_referral_subscription(self):
        """Rule 48: Referral for subscription models"""
        self.declare(ChannelPriorityFact(
            channel="referral",
            priority=2,
            budget_percent=12.0
        ))

    # ==================== LAYER 4: Content Strategy ====================

    @Rule(
        AND(
            ContentCapabilityFact(capability=ContentCapability.HIGH.value),
            OR(
                ProductFact(product_type=ProductType.B2B_SAAS.value),
                ProductFact(product_type=ProductType.CONSULTING.value)
            )
        )
    )
    def content_thought_leadership_blog(self):
        """Rule 49: Blog content for thought leadership"""
        self.declare(ContentTypePriorityFact(
            content_type="blog_articles",
            priority=1,
            frequency="3-4 per week"
        ))

    @Rule(
        AND(
            OR(
                TargetCustomerFact(customer=TargetCustomer.GEN_Z.value),
                TargetCustomerFact(customer=TargetCustomer.MILLENIAL.value)
            ),
            ContentCapabilityFact(capability=ContentCapability.MEDIUM.value)
        )
    )
    def content_video_youth(self):
        """Rule 50: Video content for youth audiences"""
        self.declare(ContentTypePriorityFact(
            content_type="video_content",
            priority=1,
            frequency="2-3 per week"
        ))

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2B_SAAS.value),
            TargetCustomerFact(customer=TargetCustomer.B2B_LARGE.value)
        )
    )
    def content_case_studies_enterprise(self):
        """Rule 51: Case studies for enterprise B2B"""
        self.declare(ContentTypePriorityFact(
            content_type="case_studies",
            priority=1,
            frequency="2 per month"
        ))

    @Rule(
        AND(
            CustomerAcquisitionComplexityFact(complexity="very_complex"),
            ContentCapabilityFact(capability=ContentCapability.HIGH.value)
        )
    )
    def content_whitepapers_complex(self):
        """Rule 52: Whitepapers for complex sales"""
        self.declare(ContentTypePriorityFact(
            content_type="whitepapers",
            priority=2,
            frequency="1 per month"
        ))

    @Rule(
        AND(
            SalesCycleFact(cycle="long"),
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
        )
    )
    def content_webinars_nurture(self):
        """Rule 53: Webinars for long sales cycles"""
        self.declare(ContentTypePriorityFact(
            content_type="webinars",
            priority=2,
            frequency="2 per month"
        ))

    @Rule(
        ProductFact(product_type=ProductType.B2C_RETAIL.value)
    )
    def content_social_posts_retail(self):
        """Rule 54: Social posts for retail"""
        self.declare(ContentTypePriorityFact(
            content_type="social_posts",
            priority=1,
            frequency="daily"
        ))

    @Rule(
        AND(
            PrimaryGoalFact(goal=PrimaryGoal.RETENTION.value),
            ProductFact(product_type=ProductType.SUBSCRIPTION.value)
        )
    )
    def content_newsletter_retention(self):
        """Rule 55: Newsletter for subscription retention"""
        self.declare(ContentTypePriorityFact(
            content_type="email_newsletters",
            priority=1,
            frequency="weekly"
        ))

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2C_RETAIL.value),
            BudgetLevelFact(tier=BudgetLevel.MICRO.value)
        )
    )
    def content_ugc_budget(self):
        """Rule 56: User-generated content for budget constraints"""
        self.declare(ContentTypePriorityFact(
            content_type="user_generated",
            priority=1,
            frequency="ongoing"
        ))

    # ==================== LAYER 5: Tactical Quick Wins ====================

    @Rule(
        AND(
            ProductFact(product_type=ProductType.LOCAL_SERVICE.value),
            BudgetLevelFact(tier=BudgetLevel.MICRO.value)
        )
    )
    def quickwin_gmb_optimization(self):
        """Rule 57: Quick win - Google My Business"""
        self.declare(QuickWinFact(
            action="Optimize Google My Business listing",
            priority="Critical",
            effort="Low"
        ))

    @Rule(
        AND(
            ContentCapabilityFact(capability=ContentCapability.LOW.value),
            BudgetLevelFact(tier=BudgetLevel.MICRO.value)
        )
    )
    def quickwin_content_calendar(self):
        """Rule 58: Quick win - Content calendar"""
        self.declare(QuickWinFact(
            action="Set up 30-day content calendar",
            priority="High",
            effort="Low"
        ))

    @Rule(
        SalesStructureFact(structure=SalesStructure.AUTOMATED.value)
    )
    def quickwin_email_automation(self):
        """Rule 59: Quick win - Email automation"""
        self.declare(QuickWinFact(
            action="Implement welcome email sequence",
            priority="High",
            effort="Medium"
        ))

    @Rule(
        AND(
            PriorityKPIFact(kpi=PriorityKPI.CR.value),
            SalesStructureFact(structure=SalesStructure.AUTOMATED.value)
        )
    )
    def quickwin_cro_audit(self):
        """Rule 60: Quick win - CRO audit"""
        self.declare(QuickWinFact(
            action="Conduct conversion funnel audit",
            priority="Critical",
            effort="Medium"
        ))

    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value)
    )
    def quickwin_linkedin_optimization(self):
        """Rule 61: Quick win - LinkedIn"""
        self.declare(QuickWinFact(
            action="Optimize LinkedIn company page and start posting",
            priority="High",
            effort="Low"
        ))

    @Rule(
        BudgetLevelFact(tier=BudgetLevel.MICRO.value)
    )
    def quickwin_competitor_analysis(self):
        """Rule 62: Quick win - Competitor research"""
        self.declare(QuickWinFact(
            action="Complete competitor marketing analysis",
            priority="High",
            effort="Low"
        ))

    # ==================== LAYER 6: KPI Recommendations ====================

    @Rule(PriorityKPIFact(kpi=PriorityKPI.CR.value))
    def kpi_conversion_rate(self):
        """Rule 63: Conversion rate KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Website Conversion Rate",
            target="2-5% improvement per quarter",
            priority="primary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="Landing Page Conversion Rate",
            target="10-20% for cold traffic",
            priority="primary"
        ))

    @Rule(PriorityKPIFact(kpi=PriorityKPI.CLV.value))
    def kpi_customer_lifetime_value(self):
        """Rule 64: CLV KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Customer Lifetime Value",
            target="3x customer acquisition cost minimum",
            priority="primary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="Repeat Purchase Rate",
            target="25-40% depending on industry",
            priority="primary"
        ))

    @Rule(PriorityKPIFact(kpi=PriorityKPI.TRAFFIC.value))
    def kpi_organic_traffic(self):
        """Rule 65: Traffic KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Organic Traffic Growth",
            target="15-30% monthly growth",
            priority="primary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="Domain Authority",
            target="+5 points per quarter",
            priority="secondary"
        ))

    @Rule(PriorityKPIFact(kpi=PriorityKPI.CPA.value))
    def kpi_cost_per_acquisition(self):
        """Rule 66: CPA KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Cost Per Acquisition",
            target="<33% of customer LTV",
            priority="primary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="Return on Ad Spend",
            target="3:1 minimum, 5:1 target",
            priority="primary"
        ))

    @Rule(PriorityKPIFact(kpi=PriorityKPI.SQL.value))
    def kpi_sales_qualified_leads(self):
        """Rule 67: SQL KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Sales Qualified Leads",
            target="20% MQL to SQL conversion",
            priority="primary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="SQL to Close Rate",
            target="25-40% depending on sales cycle",
            priority="primary"
        ))

    # Secondary KPIs

    @Rule(PrimaryGoalFact(goal=PrimaryGoal.AWARENESS.value))
    def kpi_awareness_metrics(self):
        """Rule 68: Awareness KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Brand Awareness (Surveys)",
            target="15-25% increase quarterly",
            priority="secondary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="Social Media Reach",
            target="20% monthly growth",
            priority="secondary"
        ))

    @Rule(ProductFact(product_type=ProductType.B2B_SAAS.value))
    def kpi_saas_specific(self):
        """Rule 69: SaaS-specific KPIs"""
        self.declare(KPIRecommendationFact(
            kpi="Monthly Recurring Revenue Growth",
            target="10-20% monthly",
            priority="secondary"
        ))
        self.declare(KPIRecommendationFact(
            kpi="Churn Rate",
            target="<5% monthly",
            priority="secondary"
        ))

    # ==================== LAYER 7: Risk Assessment ====================

    @Rule(BudgetLevelFact(tier=BudgetLevel.MICRO.value))
    def risk_limited_budget(self):
        """Rule 70: Risk of limited budget"""
        self.declare(RiskIdentificationFact(
            risk="Limited budget may restrict channel diversification",
            severity="High",
            mitigation="Focus on 1-2 high-ROI channels, leverage organic and low-cost tactics"
        ))

    @Rule(
        AND(
            CompetitionLevelFact(level="very_high"),
            BudgetLevelFact(tier=BudgetLevel.SMALL.value)
        )
    )
    def risk_high_competition(self):
        """Rule 71: Risk of high competition with limited budget"""
        self.declare(RiskIdentificationFact(
            risk="High competition may make paid channels expensive",
            severity="High",
            mitigation="Focus on long-tail keywords, niche positioning, and organic growth"
        ))

    @Rule(ContentCapabilityFact(capability=ContentCapability.LOW.value))
    def risk_low_content_capability(self):
        """Rule 72: Risk of low content capability"""
        self.declare(RiskIdentificationFact(
            risk="Low content capability limits content marketing effectiveness",
            severity="Medium",
            mitigation="Invest in content training, hire freelancers, or use AI tools"
        ))

    @Rule(
        AND(
            SalesCycleFact(cycle="very_long"),
            TimeHorizonFact(horizon=TimeHorizon.SHORT.value)
        )
    )
    def risk_sales_timeline_mismatch(self):
        """Rule 73: Risk of sales cycle vs timeline mismatch"""
        self.declare(RiskIdentificationFact(
            risk="Short timeline incompatible with long sales cycle",
            severity="High",
            mitigation="Set realistic expectations, focus on pipeline building not closed deals"
        ))

    @Rule(
        SalesStructureFact(structure=SalesStructure.OWNER_DRIVEN.value)
    )
    def risk_owner_bottleneck(self):
        """Rule 74: Risk of owner-driven bottleneck"""
        self.declare(RiskIdentificationFact(
            risk="Owner-driven sales may limit scalability",
            severity="Medium",
            mitigation="Implement marketing automation, nurture sequences, and self-service options"
        ))

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2C_RETAIL.value),
            PriorityKPIFact(kpi=PriorityKPI.CPA.value)
        )
    )
    def risk_cpa_volatility(self):
        """Rule 75: Risk of CPA volatility in B2C"""
        self.declare(RiskIdentificationFact(
            risk="B2C ad costs can fluctuate seasonally",
            severity="Medium",
            mitigation="Diversify traffic sources, build organic channels, reserve budget for peak seasons"
        ))

    # ==================== LAYER 8: Budget Allocation ====================

    @Rule(BudgetLevelFact(tier=BudgetLevel.MICRO.value))
    def budget_allocation_micro(self):
        """Rule 76: Budget allocation for micro budgets"""
        self.declare(BudgetCategoryFact(category="Organic Marketing", percentage=60.0))
        self.declare(BudgetCategoryFact(category="Paid Advertising", percentage=20.0))
        self.declare(BudgetCategoryFact(category="Tools & Software", percentage=10.0))
        self.declare(BudgetCategoryFact(category="Content Creation", percentage=10.0))

    @Rule(BudgetLevelFact(tier=BudgetLevel.SMALL.value))
    def budget_allocation_small(self):
        """Rule 77: Budget allocation for small budgets"""
        self.declare(BudgetCategoryFact(category="Paid Advertising", percentage=35.0))
        self.declare(BudgetCategoryFact(category="Content Marketing", percentage=25.0))
        self.declare(BudgetCategoryFact(category="Tools & Software", percentage=15.0))
        self.declare(BudgetCategoryFact(category="SEO & Organic", percentage=15.0))
        self.declare(BudgetCategoryFact(category="Marketing Operations", percentage=10.0))

    @Rule(BudgetLevelFact(tier=BudgetLevel.MEDIUM.value))
    def budget_allocation_medium(self):
        """Rule 78: Budget allocation for medium budgets"""
        self.declare(BudgetCategoryFact(category="Paid Advertising", percentage=40.0))
        self.declare(BudgetCategoryFact(category="Content & SEO", percentage=25.0))
        self.declare(BudgetCategoryFact(category="Marketing Technology", percentage=15.0))
        self.declare(BudgetCategoryFact(category="Events & Partnerships", percentage=10.0))
        self.declare(BudgetCategoryFact(category="Team & Freelancers", percentage=10.0))

    @Rule(BudgetLevelFact(tier=BudgetLevel.LARGE.value))
    def budget_allocation_large(self):
        """Rule 79: Budget allocation for large budgets"""
        self.declare(BudgetCategoryFact(category="Paid Media Mix", percentage=45.0))
        self.declare(BudgetCategoryFact(category="Brand & Content", percentage=20.0))
        self.declare(BudgetCategoryFact(category="Marketing Team", percentage=15.0))
        self.declare(BudgetCategoryFact(category="Technology Stack", percentage=10.0))
        self.declare(BudgetCategoryFact(category="Events & PR", percentage=10.0))

    @Rule(BudgetLevelFact(tier=BudgetLevel.ENTERPRISE.value))
    def budget_allocation_enterprise(self):
        """Rule 80: Budget allocation for enterprise budgets"""
        self.declare(BudgetCategoryFact(category="Multi-Channel Paid Media", percentage=40.0))
        self.declare(BudgetCategoryFact(category="Brand & Demand Gen", percentage=20.0))
        self.declare(BudgetCategoryFact(category="Marketing Organization", percentage=20.0))
        self.declare(BudgetCategoryFact(category="MarTech & Analytics", percentage=10.0))
        self.declare(BudgetCategoryFact(category="Strategic Partnerships", percentage=10.0))

    # Cost Optimization

    @Rule(BudgetLevelFact(tier=BudgetLevel.MICRO.value))
    def cost_optimization_micro(self):
        """Rule 81: Cost optimization for micro budgets"""
        self.declare(CostOptimizationFact(tip="Use free tools: Google Analytics, Google Search Console, Mailchimp free tier"))
        self.declare(CostOptimizationFact(tip="Leverage organic social media before paid ads"))
        self.declare(CostOptimizationFact(tip="Create content in-house or use AI writing assistants"))

    @Rule(
        AND(
            BudgetLevelFact(tier=BudgetLevel.SMALL.value),
            PriorityKPIFact(kpi=PriorityKPI.CPA.value)
        )
    )
    def cost_optimization_performance(self):
        """Rule 82: Cost optimization for performance focus"""
        self.declare(CostOptimizationFact(tip="Start with long-tail keywords for lower CPCs"))
        self.declare(CostOptimizationFact(tip="Use retargeting to improve conversion efficiency"))
        self.declare(CostOptimizationFact(tip="A/B test ad creative weekly to improve CTR"))

    @Rule(ContentCapabilityFact(capability=ContentCapability.LOW.value))
    def cost_optimization_content(self):
        """Rule 83: Cost optimization for content"""
        self.declare(CostOptimizationFact(tip="Repurpose content across multiple channels"))
        self.declare(CostOptimizationFact(tip="Use user-generated content and testimonials"))
        self.declare(CostOptimizationFact(tip="Curate industry content instead of always creating original"))

    # ==================== LAYER 9: Scaling Strategy ====================

    @Rule(PriorityKPIFact(kpi=PriorityKPI.CPA.value))
    def scaling_trigger_cpa(self):
        """Rule 84: Scaling trigger for CPA optimization"""
        self.declare(ScalingTriggerFact(
            trigger="When CPA is below target for 2 consecutive weeks"
        ))

    @Rule(PriorityKPIFact(kpi=PriorityKPI.TRAFFIC.value))
    def scaling_trigger_traffic(self):
        """Rule 85: Scaling trigger for traffic focus"""
        self.declare(ScalingTriggerFact(
            trigger="When organic traffic grows 20% month-over-month"
        ))

    @Rule(PriorityKPIFact(kpi=PriorityKPI.CLV.value))
    def scaling_trigger_clv(self):
        """Rule 86: Scaling trigger for CLV optimization"""
        self.declare(ScalingTriggerFact(
            trigger="When CLV:CAC ratio exceeds 3:1"
        ))

    @Rule(
        AND(
            StrategicApproachFact(approach="aggressive_growth"),
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
        )
    )
    def scaling_action_aggressive(self):
        """Rule 87: Aggressive scaling actions"""
        self.declare(ScalingActionFact(
            action="Increase winning channel budgets by 50% when efficiency maintained"
        ))
        self.declare(ScalingActionFact(
            action="Expand to 2-3 new channels after proving core channels"
        ))

    @Rule(
        StrategicApproachFact(approach="steady_growth")
    )
    def scaling_action_steady(self):
        """Rule 88: Steady scaling actions"""
        self.declare(ScalingActionFact(
            action="Increase budgets 20% monthly while maintaining target metrics"
        ))
        self.declare(ScalingActionFact(
            action="Test one new channel per quarter"
        ))

    # ==================== LAYER 10: Tools & Resources ====================

    @Rule(BudgetLevelFact(tier=BudgetLevel.MICRO.value))
    def tools_micro_budget(self):
        """Rule 89: Tools for micro budgets"""
        self.declare(ToolRecommendationFact(tool="Google Analytics (free)", category="analytics"))
        self.declare(ToolRecommendationFact(tool="Mailchimp Free Tier", category="email"))
        self.declare(ToolRecommendationFact(tool="Canva Free", category="design"))
        self.declare(ToolRecommendationFact(tool="Buffer Free", category="social_media"))

    @Rule(BudgetLevelFact(tier=BudgetLevel.SMALL.value))
    def tools_small_budget(self):
        """Rule 90: Tools for small budgets"""
        self.declare(ToolRecommendationFact(tool="Google Ads", category="paid_search"))
        self.declare(ToolRecommendationFact(tool="Mailchimp or ConvertKit", category="email"))
        self.declare(ToolRecommendationFact(tool="SEMrush or Ahrefs (basic)", category="seo"))
        self.declare(ToolRecommendationFact(tool="Hootsuite or Buffer", category="social_media"))

    @Rule(BudgetLevelFact(tier=BudgetLevel.MEDIUM.value))
    def tools_medium_budget(self):
        """Rule 91: Tools for medium budgets"""
        self.declare(ToolRecommendationFact(tool="HubSpot or Marketo", category="marketing_automation"))
        self.declare(ToolRecommendationFact(tool="SEMrush Enterprise", category="seo"))
        self.declare(ToolRecommendationFact(tool="Google Analytics + Data Studio", category="analytics"))
        self.declare(ToolRecommendationFact(tool="Sprout Social", category="social_media"))

    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value)
    )
    def tools_b2b_saas(self):
        """Rule 92: B2B SaaS specific tools"""
        self.declare(ToolRecommendationFact(tool="LinkedIn Sales Navigator", category="prospecting"))
        self.declare(ToolRecommendationFact(tool="Clearbit", category="data_enrichment"))
        self.declare(ToolRecommendationFact(tool="Intercom or Drift", category="conversational_marketing"))

    @Rule(
        ProductFact(product_type=ProductType.B2C_RETAIL.value)
    )
    def tools_b2c_retail(self):
        """Rule 93: B2C Retail specific tools"""
        self.declare(ToolRecommendationFact(tool="Facebook Ads Manager", category="paid_social"))
        self.declare(ToolRecommendationFact(tool="Klaviyo", category="email_ecommerce"))
        self.declare(ToolRecommendationFact(tool="Google Merchant Center", category="product_ads"))

    @Rule(
        ContentCapabilityFact(capability=ContentCapability.HIGH.value)
    )
    def tools_content_creation(self):
        """Rule 94: Content creation tools"""
        self.declare(ToolRecommendationFact(tool="BuzzSumo", category="content_research"))
        self.declare(ToolRecommendationFact(tool="Grammarly Premium", category="content_quality"))
        self.declare(ToolRecommendationFact(tool="Loom or Descript", category="video_content"))

    # Capability Requirements

    @Rule(
        AND(
            ContentCapabilityFact(capability=ContentCapability.LOW.value),
            OR(
                ProductFact(product_type=ProductType.B2B_SAAS.value),
                ProductFact(product_type=ProductType.CONSULTING.value)
            )
        )
    )
    def capability_content_writing(self):
        """Rule 95: Need content writing capability"""
        self.declare(CapabilityRequirementFact(
            capability="Content Writing & Thought Leadership",
            importance="Critical"
        ))

    @Rule(
        SalesStructureFact(structure=SalesStructure.AUTOMATED.value)
    )
    def capability_marketing_automation(self):
        """Rule 96: Need marketing automation skills"""
        self.declare(CapabilityRequirementFact(
            capability="Marketing Automation & Email Workflows",
            importance="High"
        ))

    @Rule(
        BudgetLevelFact(tier=BudgetLevel.MEDIUM.value)
    )
    def capability_data_analysis(self):
        """Rule 97: Need data analysis capability"""
        self.declare(CapabilityRequirementFact(
            capability="Data Analysis & Performance Optimization",
            importance="High"
        ))

    @Rule(
        OR(
            TargetCustomerFact(customer=TargetCustomer.GEN_Z.value),
            TargetCustomerFact(customer=TargetCustomer.MILLENIAL.value)
        )
    )
    def capability_social_media(self):
        """Rule 98: Need social media expertise"""
        self.declare(CapabilityRequirementFact(
            capability="Social Media Management & Community Engagement",
            importance="High"
        ))

    @Rule(
        ProductFact(product_type=ProductType.B2B_SAAS.value)
    )
    def capability_seo_technical(self):
        """Rule 99: Need technical SEO"""
        self.declare(CapabilityRequirementFact(
            capability="Technical SEO & Content Optimization",
            importance="Medium"
        ))

    # Partner Recommendations

    @Rule(
        AND(
            BudgetLevelFact(tier=BudgetLevel.MEDIUM.value),
            ContentCapabilityFact(capability=ContentCapability.LOW.value)
        )
    )
    def partner_content_agency(self):
        """Rule 100: Content agency partner"""
        self.declare(PartnerRecommendationFact(
            partner_type="Content Marketing Agency or Freelance Writers"
        ))

    @Rule(
        AND(
            BudgetLevelFact(tier=BudgetLevel.LARGE.value),
            CompetitionLevelFact(level="very_high")
        )
    )
    def partner_paid_media_agency(self):
        """Rule 101: Paid media agency"""
        self.declare(PartnerRecommendationFact(
            partner_type="Specialized Paid Media Agency (Google Ads, Facebook Ads)"
        ))

    @Rule(
        ProductFact(product_type=ProductType.B2C_RETAIL.value)
    )
    def partner_influencer_platform(self):
        """Rule 102: Influencer marketing platform"""
        self.declare(PartnerRecommendationFact(
            partner_type="Influencer Marketing Platform or Agency"
        ))

    @Rule(
        AND(
            ProductFact(product_type=ProductType.B2B_SAAS.value),
            TargetCustomerFact(customer=TargetCustomer.B2B_LARGE.value)
        )
    )
    def partner_pr_firm(self):
        """Rule 103: PR firm for enterprise"""
        self.declare(PartnerRecommendationFact(
            partner_type="B2B PR Firm for Media Relations"
        ))

    @Rule(
        ProductFact(product_type=ProductType.LOCAL_SERVICE.value)
    )
    def partner_local_seo(self):
        """Rule 104: Local SEO specialist"""
        self.declare(PartnerRecommendationFact(
            partner_type="Local SEO Specialist or Agency"
        ))
