"""
Comprehensive Output Model for Marketing Expert System
This model captures multi-dimensional marketing recommendations
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class ChannelType(str, Enum):
    PAID_SEARCH = "paid_search_google_ads"
    PAID_SOCIAL = "paid_social_facebook_instagram_linkedin"
    ORGANIC_SEO = "organic_seo_content"
    EMAIL_MARKETING = "email_marketing"
    CONTENT_MARKETING = "content_marketing_blog_video"
    INFLUENCER = "influencer_partnerships"
    PR_MEDIA = "pr_and_media_relations"
    EVENTS_WEBINARS = "events_and_webinars"
    AFFILIATE = "affiliate_marketing"
    DIRECT_MAIL = "direct_mail"
    COMMUNITY = "community_building"
    PARTNERSHIPS = "strategic_partnerships"
    RETARGETING = "retargeting_remarketing"
    DISPLAY_ADS = "display_advertising"
    VIDEO_ADS = "video_advertising_youtube"
    PODCAST = "podcast_sponsorships"
    LOCAL_SEO = "local_seo_gmb"
    MARKETPLACE = "marketplace_optimization"
    CRO = "conversion_rate_optimization"
    REFERRAL = "referral_programs"

class ChannelRecommendation(BaseModel):
    channel: ChannelType
    priority: int = Field(..., ge=1, le=5, description="1=highest, 5=lowest")
    budget_allocation_percent: float = Field(..., ge=0, le=100)
    rationale: str
    expected_impact: str

class ContentType(str, Enum):
    BLOG_ARTICLES = "blog_articles_seo"
    VIDEO_CONTENT = "video_content"
    INFOGRAPHICS = "infographics"
    CASE_STUDIES = "case_studies"
    WHITEPAPERS = "whitepapers_ebooks"
    WEBINARS = "webinars_workshops"
    PODCASTS = "podcast_episodes"
    SOCIAL_POSTS = "social_media_posts"
    EMAIL_NEWSLETTERS = "email_newsletters"
    USER_GENERATED = "user_generated_content"
    INTERACTIVE = "interactive_content_tools"
    TESTIMONIALS = "customer_testimonials"

class ContentRecommendation(BaseModel):
    content_type: ContentType
    frequency: str  # e.g., "2-3 per week", "monthly"
    priority: int = Field(..., ge=1, le=5)
    target_topics: List[str]
    distribution_channels: List[str]

class TacticalAction(BaseModel):
    action: str
    timeline: str  # e.g., "Week 1-2", "Month 1", "Ongoing"
    priority: str  # "Critical", "High", "Medium", "Low"
    estimated_effort: str  # "Low", "Medium", "High"
    expected_outcome: str
    dependencies: List[str] = []

class KPITarget(BaseModel):
    metric_name: str
    target_value: str
    measurement_frequency: str
    benchmark: Optional[str] = None

class RiskFactor(BaseModel):
    risk: str
    severity: str  # "High", "Medium", "Low"
    mitigation: str

class MarketingRecommendation(BaseModel):
    # Core Strategy
    strategy_summary: str = Field(..., description="High-level strategic direction")
    strategic_positioning: str = Field(..., description="How to position in market")

    # Channel Strategy
    primary_channels: List[ChannelRecommendation] = Field(..., description="Prioritized marketing channels")
    channel_mix_rationale: str

    # Content Strategy
    content_strategy: List[ContentRecommendation]
    content_themes: List[str]
    messaging_focus: str

    # Tactical Execution
    quick_wins: List[TacticalAction] = Field(..., description="Actions for first 30 days")
    short_term_actions: List[TacticalAction] = Field(..., description="1-3 months")
    medium_term_actions: List[TacticalAction] = Field(..., description="3-6 months")
    long_term_actions: List[TacticalAction] = Field(..., description="6+ months")

    # Measurement
    primary_kpis: List[KPITarget]
    secondary_kpis: List[KPITarget]

    # Risk Management
    risks_and_mitigations: List[RiskFactor]

    # Budget Guidance
    budget_allocation_summary: Dict[str, float] = Field(..., description="Category-level budget distribution")
    monthly_burn_rate: float
    cost_optimization_tips: List[str]

    # Competitive Positioning
    competitive_advantages: List[str]
    differentiation_strategy: str

    # Scaling Guidance
    scaling_triggers: List[str] = Field(..., description="When to scale up investment")
    scaling_strategy: str

    # Tools and Resources
    recommended_tools: List[str]
    required_capabilities: List[str]
    potential_partners: List[str]
