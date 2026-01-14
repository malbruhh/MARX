"""
Simplified Output Model for Marketing Expert System (University Project)
Focuses on core recommendations with concise, actionable insights
"""
from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum

class StrategyCode(str, Enum):
    """Marketing Strategy Codes"""
    S1 = "S1 - Search Engine Optimization (SEO)"
    S2 = "S2 - Pay-Per-Click (PPC) Advertising"
    S3 = "S3 - Social Media Marketing (SMM)"
    S4 = "S4 - Email Marketing/Newsletters"
    S5 = "S5 - Content Marketing"
    S6 = "S6 - Local SEO (Google My Business)"
    S7 = "S7 - Account-Based Marketing (ABM)"
    S8 = "S8 - Trade Shows/Conferences"
    S9 = "S9 - Influencer/Partnership Marketing"

class BudgetAllocation(BaseModel):
    """Budget distribution across strategies"""
    strategy_code: str
    percentage: float = Field(..., ge=0, le=100)
    monthly_amount: float

class ChannelTactic(BaseModel):
    """Specific tactic for a marketing channel"""
    strategy_code: str
    tactic: str
    priority: str  # "High", "Medium", "Low"
    expected_outcome: str

class MarketingRecommendation(BaseModel):
    """Simplified marketing recommendation output"""

    # Core recommended strategies (S1-S9 format)
    recommended_strategies: List[str] = Field(
        ...,
        description="List of recommended strategy codes with labels (e.g., 'S1 - SEO')"
    )

    # 2-5 critical insights
    critical_insights: List[str] = Field(
        ...,
        min_items=2,
        max_items=5,
        description="Key strategic recommendations and insights"
    )

    # Budget allocation
    budget_allocation: List[BudgetAllocation] = Field(
        ...,
        description="How budget should be distributed across strategies"
    )

    total_monthly_budget: float

    # Channel-specific tactics
    channel_tactics: List[ChannelTactic] = Field(
        ...,
        description="Specific actionable tactics for each channel"
    )

    # === COMBINED SECTIONS: Action Plan & Resources ===

    # Action plan: Quick wins, KPIs, risks, and scaling triggers
    action_plan: List[str] = Field(
        default=[],
        description="Combined action items: quick wins, KPIs to track, risks to mitigate, and scaling triggers"
    )

    # Resources: Tools, capabilities, partners, and cost optimization tips
    resources: List[str] = Field(
        default=[],
        description="Combined resources: recommended tools, required capabilities, potential partners, and cost-saving tips"
    )
