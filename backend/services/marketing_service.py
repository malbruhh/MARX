# Convert Pydantic data (JSON) into KnowledgeBase
from experta import KnowledgeEngine,Rule, AS, MATCH, AND
from models.model import *
from models.request import MarketingAnalysisRequest

class MarketingEngine(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.strategy = "Standard Marketing Mix Recommended."

    @Rule(RawBudget(amount=MATCH.a & (lambda a: a <= 1000)))
    def mark_micro_budget(self):
        self.declare(BudgetLevelFact(tier=BudgetLevel.MICRO))

    @Rule(RawBudget(amount=MATCH.a & (lambda a: 1000 < a <= 10000)))
    def mark_small_budget(self):
        self.declare(BudgetLevelFact(tier=BudgetLevel.SMALL))
    
    @Rule(RawBudget(amount=MATCH.a & (lambda a: 10000 <= a <= 100000)))
    def mark_medium_budget(self):
        self.declare(BudgetLevelFact(tier=BudgetLevel.MEDIUM))
    @Rule(RawBudget(amount=MATCH.a & (lambda a: 100000 <= a <= 1000000)))

    def mark_large_budget(self):
        self.declare(BudgetLevelFact(tier=BudgetLevel.LARGE))
    
    @Rule(RawBudget(amount=MATCH.a & (lambda a: a > 1000000)))
    def mark_enterprise_budget(self):
        self.declare(BudgetLevelFact(tier=BudgetLevel.ENTERPRISE))

    #Rule 1: 
    @Rule(
        AND(
            ProductFact(type=ProductType.B2B_SAAS),
            BudgetLevelFact(tier=BudgetLevel.MICRO)
            )
        )
    def some_strategy(self):
        self.strategy = 'Strategy 1'

    
def run_analysis_service(request: MarketingAnalysisRequest):
    engine = MarketingEngine()
    engine.reset()
    
    # Pass the enum objects directly, not their string values
    engine.declare(ProductFact(type=request.product_type))
    engine.declare(RawBudget(amount=request.raw_budget_amount))
    engine.declare(TargetCustomerFact(type=request.target_customer))
    engine.declare(PrimaryGoalFact(type=request.primary_goal))
    engine.declare(TimeHorizonFact(type=request.time_horizon))
    engine.declare(ContentCapabilityFact(type=request.content_capability))
    engine.declare(SalesStructureFact(type=request.sales_structure))
    engine.declare(PriorityKPIFact(type=request.priority_kpi))
    
    engine.run()
    return engine.strategy if engine.strategy else "Standard Marketing Mix Recommended."



