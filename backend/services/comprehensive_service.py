"""
Simplified Comprehensive Marketing Analysis Service
Produces concise, actionable recommendations for university project
"""
from services.comprehensive_engine import ComprehensiveMarketingEngine
from models.model import *
from models.request import MarketingAnalysisRequest
from models.output import *
from models.intermediate_facts import *
from collections import defaultdict

# Channel to Strategy Code Mapping
CHANNEL_TO_STRATEGY = {
    "organic_seo_content": "S1",
    "paid_search_google_ads": "S2",
    "paid_social_facebook_instagram_linkedin": "S3",
    "email_marketing": "S4",
    "content_marketing_blog_video": "S5",
    "local_seo_gmb": "S6",
    # S7 is ABM - will be inferred from specific conditions
    "events_and_webinars": "S8",
    "influencer_partnerships": "S9",
    "strategic_partnerships": "S9",
}

STRATEGY_LABELS = {
    "S1": "S1 - Search Engine Optimization (SEO)",
    "S2": "S2 - Pay-Per-Click (PPC) Advertising",
    "S3": "S3 - Social Media Marketing (SMM)",
    "S4": "S4 - Email Marketing/Newsletters",
    "S5": "S5 - Content Marketing",
    "S6": "S6 - Local SEO (Google My Business)",
    "S7": "S7 - Account-Based Marketing (ABM)",
    "S8": "S8 - Trade Shows/Conferences",
    "S9": "S9 - Influencer/Partnership Marketing",
}


def run_comprehensive_analysis(request: MarketingAnalysisRequest) -> MarketingRecommendation:
    """
    Run comprehensive marketing analysis using layered forward chaining
    Returns simplified, actionable recommendations
    """
    try:
        # Initialize the expert system engine
        engine = ComprehensiveMarketingEngine()
        engine.reset()

        # Declare initial facts from user input
        engine.declare(ProductFact(product_type=request.product_type.value))
        engine.declare(RawBudget(amount=request.raw_budget_amount))
        engine.declare(TargetCustomerFact(customer=request.target_customer.value))
        engine.declare(PrimaryGoalFact(goal=request.primary_goal.value))
        engine.declare(TimeHorizonFact(horizon=request.time_horizon.value))
        engine.declare(ContentCapabilityFact(capability=request.content_capability.value))
        engine.declare(SalesStructureFact(structure=request.sales_structure.value))
        engine.declare(PriorityKPIFact(kpi=request.priority_kpi.value))

        # Run forward chaining - rules will fire in layers
        engine.run()

        # Aggregate inferred facts into simplified output
        recommendation = _aggregate_recommendations(engine, request)

        return recommendation

    except Exception as e:
        import traceback
        error_detail = f"Error in comprehensive marketing analysis: {str(e)}\n{traceback.format_exc()}"
        raise Exception(error_detail)


def _aggregate_recommendations(engine: ComprehensiveMarketingEngine, request: MarketingAnalysisRequest) -> MarketingRecommendation:
    """
    Aggregate all inferred facts from the engine into a simplified recommendation
    """

    # Get facts from knowledge base
    facts = list(engine.facts.values())

    # Extract channel priorities
    channel_facts = [f for f in facts if isinstance(f, ChannelPriorityFact)]

    # Map channels to strategy codes
    strategy_codes = _extract_strategy_codes(channel_facts, request)

    # Generate 2-5 critical insights
    critical_insights = _generate_critical_insights(facts, request)

    # Generate budget allocation
    budget_allocation = _generate_budget_allocation(channel_facts, request, strategy_codes)

    # Generate channel tactics
    channel_tactics = _generate_channel_tactics(channel_facts, facts, request)

    # Calculate monthly budget
    monthly_budget = _calculate_monthly_budget(request)

    return MarketingRecommendation(
        recommended_strategies=strategy_codes,
        critical_insights=critical_insights,
        budget_allocation=budget_allocation,
        total_monthly_budget=monthly_budget,
        channel_tactics=channel_tactics
    )


def _extract_strategy_codes(channel_facts: list, request: MarketingAnalysisRequest) -> list:
    """Map recommended channels to strategy codes (S1-S9)"""

    # Sort channels by priority
    sorted_channels = sorted(channel_facts, key=lambda f: f['priority'])

    strategy_set = set()

    # Map channels to strategies
    for fact in sorted_channels[:5]:  # Top 5 channels
        channel_name = fact['channel']
        if channel_name in CHANNEL_TO_STRATEGY:
            strategy_set.add(CHANNEL_TO_STRATEGY[channel_name])

    # Add ABM (S7) for B2B enterprise with sales team
    if (request.product_type in [ProductType.B2B_SAAS, ProductType.CONSULTING] and
        request.target_customer == TargetCustomer.B2B_LARGE and
        request.sales_structure == SalesStructure.SALES_TEAM):
        strategy_set.add("S7")

    # Convert to labeled format
    strategy_codes = [STRATEGY_LABELS[code] for code in sorted(strategy_set)]

    # Ensure at least 3 strategies
    if len(strategy_codes) < 3:
        # Add default strategies
        defaults = ["S1", "S2", "S5"]
        for default in defaults:
            if STRATEGY_LABELS[default] not in strategy_codes:
                strategy_codes.append(STRATEGY_LABELS[default])
                if len(strategy_codes) >= 3:
                    break

    return strategy_codes[:5]  # Max 5 strategies


def _generate_critical_insights(facts: list, request: MarketingAnalysisRequest) -> list:
    """Generate 2-5 critical strategic insights"""

    insights = []

    # Extract key facts
    strategic_approach = next((f['approach'] for f in facts if isinstance(f, StrategicApproachFact)), None)
    marketing_focus = next((f['focus'] for f in facts if isinstance(f, MarketingFocusFact)), None)
    sales_cycle = next((f['cycle'] for f in facts if isinstance(f, SalesCycleFact)), None)

    # Insight 1: Primary strategic direction
    if request.primary_goal == PrimaryGoal.AWARENESS:
        insights.append("Focus on brand visibility and reach - prioritize content distribution and thought leadership to build market presence")
    elif request.primary_goal == PrimaryGoal.LEAD_GEN:
        insights.append("Optimize for conversion - implement targeted campaigns with clear CTAs and lead capture mechanisms")
    else:  # RETENTION
        insights.append("Strengthen customer relationships - invest in personalized communication and value-added content for existing customers")

    # Insight 2: Budget and channel strategy
    budget_level = _determine_budget_level(request.raw_budget_amount)
    if budget_level in [BudgetLevel.MICRO, BudgetLevel.SMALL]:
        insights.append("With limited budget, concentrate on high-ROI organic channels (SEO, content) and test paid channels with small experiments")
    elif budget_level in [BudgetLevel.LARGE, BudgetLevel.ENTERPRISE]:
        insights.append("Leverage multi-channel approach - diversify across paid and organic to maximize reach while maintaining efficiency")
    else:
        insights.append("Balance paid acquisition with organic growth - allocate 60% to proven channels and 40% to testing new opportunities")

    # Insight 3: Product-specific strategy
    if request.product_type in [ProductType.B2B_SAAS, ProductType.CONSULTING]:
        insights.append("B2B buyers need education and trust - create case studies, whitepapers, and demonstrate ROI through content")
    elif request.product_type == ProductType.LOCAL_SERVICE:
        insights.append("Local dominance is key - prioritize Google My Business, local SEO, and community engagement to capture nearby customers")
    elif request.product_type in [ProductType.B2C_RETAIL, ProductType.FMCG]:
        insights.append("Focus on purchase intent moments - use retargeting, social proof, and time-sensitive offers to drive conversions")

    # Insight 4: Time horizon consideration
    if request.time_horizon == TimeHorizon.SHORT and len(insights) < 5:
        insights.append("Short timeline requires immediate action - prioritize paid channels and quick-win optimizations over long-term SEO")
    elif request.time_horizon == TimeHorizon.LONG and len(insights) < 5:
        insights.append("Long-term perspective enables compound growth - invest in SEO, content library, and brand equity that appreciates over time")

    # Insight 5: Content capability leverage
    if request.content_capability == ContentCapability.HIGH and len(insights) < 5:
        insights.append("Maximize your content strength - produce authoritative resources that attract organic traffic and establish industry credibility")
    elif request.content_capability == ContentCapability.LOW and len(insights) < 5:
        insights.append("Outsource or simplify content creation - focus on curated content, user-generated content, and paid channels that don't require heavy content production")

    return insights[:5]  # Max 5 insights


def _generate_budget_allocation(channel_facts: list, request: MarketingAnalysisRequest, strategy_codes: list) -> list:
    """Generate simplified budget allocation"""

    monthly_budget = _calculate_monthly_budget(request)

    # Sort channels by priority
    sorted_channels = sorted(channel_facts, key=lambda f: f['priority'])

    allocations = []
    total_percent = 0

    # Map channels to strategies and allocate budget
    strategy_budget_map = {}

    for fact in sorted_channels[:7]:  # Top channels
        channel_name = fact['channel']
        budget_percent = fact.get('budget_percent', 0)

        if channel_name in CHANNEL_TO_STRATEGY:
            strategy_code = CHANNEL_TO_STRATEGY[channel_name]

            # Aggregate budget for same strategy
            if strategy_code not in strategy_budget_map:
                strategy_budget_map[strategy_code] = 0
            strategy_budget_map[strategy_code] += budget_percent

    # Create allocation objects
    for strategy_code, percentage in sorted(strategy_budget_map.items(), key=lambda x: x[1], reverse=True):
        if percentage > 0:
            allocations.append(BudgetAllocation(
                strategy_code=STRATEGY_LABELS[strategy_code],
                percentage=round(percentage, 1),
                monthly_amount=round(monthly_budget * (percentage / 100), 2)
            ))
            total_percent += percentage

    # Normalize if over 100%
    if total_percent > 100:
        for alloc in allocations:
            alloc.percentage = round((alloc.percentage / total_percent) * 100, 1)
            alloc.monthly_amount = round(monthly_budget * (alloc.percentage / 100), 2)

    # If no allocations, create default
    if not allocations:
        defaults = [
            ("S1", 30),
            ("S2", 40),
            ("S5", 30)
        ]
        for code, pct in defaults:
            allocations.append(BudgetAllocation(
                strategy_code=STRATEGY_LABELS[code],
                percentage=pct,
                monthly_amount=round(monthly_budget * (pct / 100), 2)
            ))

    return allocations


def _generate_channel_tactics(channel_facts: list, all_facts: list, request: MarketingAnalysisRequest) -> list:
    """Generate specific tactics for each channel"""

    tactics = []

    # Sort channels by priority
    sorted_channels = sorted(channel_facts, key=lambda f: f['priority'])

    # Get quick wins and tactical actions
    quick_wins = [f for f in all_facts if isinstance(f, QuickWinFact)]
    tactical_actions = [f for f in all_facts if isinstance(f, TacticalActionFact)]

    processed_strategies = set()

    for fact in sorted_channels[:5]:  # Top 5 channels
        channel_name = fact['channel']
        priority_num = fact['priority']

        if channel_name not in CHANNEL_TO_STRATEGY:
            continue

        strategy_code = CHANNEL_TO_STRATEGY[channel_name]
        strategy_label = STRATEGY_LABELS[strategy_code]

        if strategy_label in processed_strategies:
            continue

        processed_strategies.add(strategy_label)

        # Determine priority label
        priority_label = "High" if priority_num <= 2 else ("Medium" if priority_num <= 3 else "Low")

        # Generate tactic based on strategy
        tactic_text, outcome = _get_tactic_for_strategy(strategy_code, request, channel_name)

        tactics.append(ChannelTactic(
            strategy_code=strategy_label,
            tactic=tactic_text,
            priority=priority_label,
            expected_outcome=outcome
        ))

    # Ensure at least 3 tactics
    if len(tactics) < 3:
        default_tactics = _get_default_tactics(request)
        for dt in default_tactics:
            if dt.strategy_code not in processed_strategies:
                tactics.append(dt)
                if len(tactics) >= 3:
                    break

    return tactics[:6]  # Max 6 tactics


def _get_tactic_for_strategy(strategy_code: str, request: MarketingAnalysisRequest, channel_name: str):
    """Get specific tactic and expected outcome for a strategy"""

    tactics_map = {
        "S1": (
            "Optimize website for target keywords and create SEO-focused content pillars",
            "Increase organic traffic by 30-50% over 3-6 months"
        ),
        "S2": (
            "Launch targeted PPC campaigns on Google Ads with A/B tested ad copy",
            "Generate qualified leads with target CPA below industry average"
        ),
        "S3": (
            "Build consistent social presence with daily posts and engagement",
            "Grow follower base and drive 15-20% of website traffic from social"
        ),
        "S4": (
            "Develop email nurture sequences and monthly newsletter campaigns",
            "Achieve 20-25% open rate and 3-5% click-through rate"
        ),
        "S5": (
            "Create value-driven content (blogs, videos, guides) addressing customer pain points",
            "Establish thought leadership and generate inbound leads"
        ),
        "S6": (
            "Optimize Google My Business profile and collect customer reviews",
            "Rank in top 3 local map pack for primary keywords"
        ),
        "S7": (
            "Identify top 20 target accounts and create personalized outreach campaigns",
            "Increase enterprise deal closure rate by 40%"
        ),
        "S8": (
            "Attend industry conferences and host booth/speaking sessions",
            "Generate 50-100 qualified leads per event"
        ),
        "S9": (
            "Partner with industry influencers or complementary brands",
            "Expand reach to new audiences and increase brand credibility"
        ),
    }

    return tactics_map.get(strategy_code, ("Implement marketing initiatives", "Drive business growth"))


def _get_default_tactics(request: MarketingAnalysisRequest) -> list:
    """Get default tactics when not enough are generated"""

    defaults = [
        ChannelTactic(
            strategy_code=STRATEGY_LABELS["S1"],
            tactic="Optimize website for target keywords and create SEO-focused content pillars",
            priority="High",
            expected_outcome="Increase organic traffic by 30-50% over 3-6 months"
        ),
        ChannelTactic(
            strategy_code=STRATEGY_LABELS["S2"],
            tactic="Launch targeted PPC campaigns on Google Ads with A/B tested ad copy",
            priority="High",
            expected_outcome="Generate qualified leads with target CPA below industry average"
        ),
        ChannelTactic(
            strategy_code=STRATEGY_LABELS["S5"],
            tactic="Create value-driven content (blogs, videos, guides) addressing customer pain points",
            priority="Medium",
            expected_outcome="Establish thought leadership and generate inbound leads"
        ),
    ]

    return defaults


def _calculate_monthly_budget(request: MarketingAnalysisRequest) -> float:
    """Calculate monthly budget based on time horizon"""

    months = {
        TimeHorizon.SHORT: 2,
        TimeHorizon.MEDIUM: 4,
        TimeHorizon.LONG: 9
    }.get(request.time_horizon, 6)

    return round(request.raw_budget_amount / months, 2)


def _determine_budget_level(amount: float) -> BudgetLevel:
    """Determine budget level from raw amount"""

    if amount < 1000:
        return BudgetLevel.MICRO
    elif amount < 10000:
        return BudgetLevel.SMALL
    elif amount < 100000:
        return BudgetLevel.MEDIUM
    elif amount < 1000000:
        return BudgetLevel.LARGE
    else:
        return BudgetLevel.ENTERPRISE
