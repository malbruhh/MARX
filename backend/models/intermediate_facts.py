"""
Intermediate Facts for Layered Forward Chaining
These facts are inferred during the reasoning process
"""
from experta import Fact

# Layer 1: Market Context Analysis
class MarketMaturityFact(Fact):
    """Inferred market maturity level"""
    level: str  # "emerging", "growth", "mature", "saturated"

class CompetitionLevelFact(Fact):
    """Inferred competition intensity"""
    level: str  # "low", "moderate", "high", "very_high"

class CustomerAcquisitionComplexityFact(Fact):
    """How complex is the customer acquisition process"""
    complexity: str  # "simple", "moderate", "complex", "very_complex"

# Layer 2: Strategic Direction
class StrategicApproachFact(Fact):
    """High-level strategic approach"""
    approach: str  # "aggressive_growth", "steady_growth", "defensive", "niche_domination"

class MarketingFocusFact(Fact):
    """Primary marketing focus"""
    focus: str  # "acquisition", "retention", "expansion", "brand_building"

class SalesCycleFact(Fact):
    """Inferred sales cycle length"""
    cycle: str  # "immediate", "short", "medium", "long", "very_long"

# Layer 3: Channel Suitability
class ChannelPriorityFact(Fact):
    """Priority level for a specific channel"""
    channel: str
    priority: int  # 1-5, where 1 is highest
    budget_percent: float

class ChannelReadinessFact(Fact):
    """Organizational readiness for a channel"""
    channel: str
    readiness: str  # "ready", "needs_preparation", "not_suitable"

# Layer 4: Content Strategy
class ContentTypePriorityFact(Fact):
    """Priority for content types"""
    content_type: str
    priority: int
    frequency: str

class MessagingAngleFact(Fact):
    """Key messaging angles to use"""
    angle: str  # "roi_focused", "innovation", "reliability", "cost_savings", etc.

# Layer 5: Tactical Execution
class QuickWinFact(Fact):
    """Identified quick win action"""
    action: str
    priority: str
    effort: str

class TacticalActionFact(Fact):
    """Specific tactical recommendation"""
    action: str
    timeline: str
    priority: str

# Layer 6: Measurement & KPIs
class KPIRecommendationFact(Fact):
    """Recommended KPI to track"""
    kpi: str
    target: str
    priority: str  # "primary", "secondary"

# Layer 7: Risk Assessment
class RiskIdentificationFact(Fact):
    """Identified risk factor"""
    risk: str
    severity: str
    mitigation: str

# Layer 8: Budget Allocation
class BudgetCategoryFact(Fact):
    """Budget allocation for a category"""
    category: str
    percentage: float

class CostOptimizationFact(Fact):
    """Cost optimization recommendation"""
    tip: str

# Layer 9: Scaling Strategy
class ScalingTriggerFact(Fact):
    """Condition that triggers scaling"""
    trigger: str

class ScalingActionFact(Fact):
    """Action to take when scaling"""
    action: str

# Layer 10: Tools & Resources
class ToolRecommendationFact(Fact):
    """Recommended marketing tool"""
    tool: str
    category: str

class CapabilityRequirementFact(Fact):
    """Required capability or skill"""
    capability: str
    importance: str

class PartnerRecommendationFact(Fact):
    """Recommended partner type"""
    partner_type: str
