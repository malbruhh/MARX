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
    # Primary channels (match engine rule names)
    "organic_seo": "S1",
    "paid_search": "S2",
    "paid_social": "S3",
    "email_marketing": "S4",
    "content_marketing": "S5",
    "local_seo": "S6",
    # S7 is ABM - will be inferred from specific conditions
    "events_webinars": "S8",
    "influencer": "S9",
    # Secondary channels mapped to related strategies
    "community": "S5",
    "retargeting": "S2",
    "referral": "S4",
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

    # Map channels to strategy codes (TOP 3)
    strategy_codes = _extract_strategy_codes(channel_facts, request)

    # Generate 2-5 critical insights
    critical_insights = _generate_critical_insights(facts, request)

    # Generate budget allocation (ONLY for top 3 strategies)
    budget_allocation = _generate_budget_allocation(channel_facts, request, strategy_codes)

    # Generate channel tactics (ONLY for top 3 strategies)
    channel_tactics = _generate_channel_tactics(channel_facts, facts, request, strategy_codes)

    # Calculate monthly budget
    monthly_budget = _calculate_monthly_budget(request)

    # === BUILD COMBINED SECTIONS ===

    # Build action plan (quick wins + KPIs + risks + scaling)
    action_plan = _build_action_plan(facts)

    # Build resources (tools + capabilities + partners + cost tips)
    resources = _build_resources(facts)

    return MarketingRecommendation(
        recommended_strategies=strategy_codes,
        critical_insights=critical_insights,
        budget_allocation=budget_allocation,
        total_monthly_budget=monthly_budget,
        channel_tactics=channel_tactics,
        action_plan=action_plan,
        resources=resources
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

    # Ensure at least 3 strategies with context-aware defaults
    if len(strategy_codes) < 3:
        # Choose defaults based on time horizon
        if request.time_horizon == TimeHorizon.SHORT:
            # Short-term: favor paid channels over SEO
            defaults = ["S2", "S3", "S4"]  # PPC, Social, Email
        elif request.time_horizon == TimeHorizon.LONG:
            # Long-term: favor organic channels
            defaults = ["S1", "S5", "S2"]  # SEO, Content, PPC
        else:
            # Medium: balanced
            defaults = ["S2", "S5", "S1"]  # PPC, Content, SEO

        for default in defaults:
            if STRATEGY_LABELS[default] not in strategy_codes:
                strategy_codes.append(STRATEGY_LABELS[default])
                if len(strategy_codes) >= 3:
                    break

    return strategy_codes[:3]  # Max 3 strategies


def _generate_critical_insights(facts: list, request: MarketingAnalysisRequest) -> list:
    """Generate 2-5 critical strategic insights"""

    insights = []

    # Extract key facts
    # strategic_approach = next((f['approach'] for f in facts if isinstance(f, StrategicApproachFact)), None)
    # marketing_focus = next((f['focus'] for f in facts if isinstance(f, MarketingFocusFact)), None)
    # sales_cycle = next((f['cycle'] for f in facts if isinstance(f, SalesCycleFact)), None)

    # Insight 1: Primary strategic direction
    if request.primary_goal == PrimaryGoal.AWARENESS:
        insights.append("Focus on brand visibility and reach - prioritize content distribution and thought leadership to build market presence")
    elif request.primary_goal == PrimaryGoal.LEAD_GEN:
        insights.append("Optimize for conversion - implement targeted campaigns with clear CTAs and lead capture mechanisms")
    else:  # RETENTION
        insights.append("Strengthen customer relationships - invest in personalized communication and value-added content for existing customers")

    # Insight 2: Budget and channel strategy
    # Extract budget level from inferred facts (already classified by engine Rule 1)
    budget_level_fact = next((f for f in facts if isinstance(f, BudgetLevelFact)), None)

    if budget_level_fact:
        budget_tier = budget_level_fact.get('tier', '')
        if budget_tier in [BudgetLevel.MICRO.value, BudgetLevel.SMALL.value]:
            insights.append("With limited budget, concentrate on high-ROI organic channels (SEO, content) and test paid channels with small experiments")
        elif budget_tier in [BudgetLevel.LARGE.value, BudgetLevel.ENTERPRISE.value]:
            insights.append("Leverage multi-channel approach - diversify across paid and organic to maximize reach while maintaining efficiency")
        else:
            insights.append("Balance paid acquisition with organic growth - allocate 60% to proven channels and 40% to testing new opportunities")
    else:
        # Fallback if no budget fact (shouldn't happen)
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
    """Generate simplified budget allocation - ONLY for recommended strategies"""

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
            strategy_label = STRATEGY_LABELS[strategy_code]

            # ONLY include if this strategy is in recommended_strategies
            if strategy_label not in strategy_codes:
                continue

            # Aggregate budget for same strategy
            if strategy_code not in strategy_budget_map:
                strategy_budget_map[strategy_code] = 0
            strategy_budget_map[strategy_code] += budget_percent

    # Ensure every recommended strategy has a budget allocation
    # Default percentages for strategies without channel facts
    default_budget_per_strategy = {
        "S1": 20, "S2": 35, "S3": 30, "S4": 20, "S5": 25,
        "S6": 25, "S7": 30, "S8": 25, "S9": 20
    }

    for strategy_label in strategy_codes:
        # Extract code from label (e.g., "S1 - ..." -> "S1")
        strategy_code = strategy_label.split(" - ")[0]
        if strategy_code not in strategy_budget_map:
            # Add default budget for strategies without channel facts
            strategy_budget_map[strategy_code] = default_budget_per_strategy.get(strategy_code, 20)

    # Calculate total to normalize BEFORE creating allocation objects
    total_percent = sum(p for p in strategy_budget_map.values() if p > 0)

    # Create allocation objects with normalized percentages
    for strategy_code, percentage in sorted(strategy_budget_map.items(), key=lambda x: x[1], reverse=True):
        if percentage > 0:
            # Normalize to 100% during creation to avoid Pydantic validation errors
            normalized_pct = round((percentage / total_percent) * 100, 1) if total_percent > 0 else percentage
            allocations.append(BudgetAllocation(
                strategy_code=STRATEGY_LABELS[strategy_code],
                percentage=normalized_pct,
                monthly_amount=round(monthly_budget * (normalized_pct / 100), 2)
            ))

    # If no allocations, create default (should match recommended strategies)
    if not allocations:
        defaults = [
            ("S2", 40),
            ("S3", 35),
            ("S5", 25)
        ]
        for code, pct in defaults:
            allocations.append(BudgetAllocation(
                strategy_code=STRATEGY_LABELS[code],
                percentage=pct,
                monthly_amount=round(monthly_budget * (pct / 100), 2)
            ))

    return allocations


def _generate_channel_tactics(channel_facts: list, all_facts: list, request: MarketingAnalysisRequest, strategy_codes: list) -> list:
    """Generate specific tactics for each channel - ONLY for recommended strategies"""

    tactics = []

    # Sort channels by priority
    sorted_channels = sorted(channel_facts, key=lambda f: f['priority'])

    # Get quick wins and tactical actions
    quick_wins = [f for f in all_facts if isinstance(f, QuickWinFact)]
    tactical_actions = [f for f in all_facts if isinstance(f, TacticalActionFact)]

    processed_strategies = set()

    for fact in sorted_channels[:10]:  # Check more channels to find matches
        channel_name = fact['channel']
        priority_num = fact['priority']

        if channel_name not in CHANNEL_TO_STRATEGY:
            continue

        strategy_code = CHANNEL_TO_STRATEGY[channel_name]
        strategy_label = STRATEGY_LABELS[strategy_code]

        # ONLY include if this strategy is in recommended_strategies
        if strategy_label not in strategy_codes:
            continue

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

        # Stop when we have tactics for all recommended strategies
        if len(tactics) >= len(strategy_codes):
            break

    # Ensure we have tactics for all recommended strategies
    if len(tactics) < len(strategy_codes):
        default_tactics = _get_default_tactics(request)
        for dt in default_tactics:
            if dt.strategy_code in strategy_codes and dt.strategy_code not in processed_strategies:
                tactics.append(dt)
                if len(tactics) >= len(strategy_codes):
                    break

    return tactics[:3]  # Max 3 tactics (matching recommended strategies)


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


# ==================== COMBINED OUTPUT BUILDERS ====================

def _build_action_plan(facts: list) -> list:
    """Build combined action plan from quick wins, KPIs, risks, and scaling triggers"""
    action_plan = []

    # Extract quick wins (top 2)
    quick_win_facts = [f for f in facts if isinstance(f, QuickWinFact)]
    priority_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
    sorted_wins = sorted(quick_win_facts, key=lambda f: priority_order.get(f.get('priority', 'Medium'), 3))

    for win_fact in sorted_wins[:2]:
        action = win_fact.get('action', '')
        priority = win_fact.get('priority', 'High')
        action_plan.append(f"[Quick Win - {priority}] {action}")

    # Extract KPIs (top 2 primary)
    kpi_facts = [f for f in facts if isinstance(f, KPIRecommendationFact)]
    primary_kpis = [f for f in kpi_facts if f.get('priority') == 'primary']

    for kpi_fact in primary_kpis[:2]:
        kpi = kpi_fact.get('kpi', '')
        target = kpi_fact.get('target', '')
        action_plan.append(f"[KPI] {kpi}: {target}")

    # Extract risks (top 2, simplified)
    risk_facts = [f for f in facts if isinstance(f, RiskIdentificationFact)]

    for risk_fact in risk_facts[:2]:
        risk = risk_fact.get('risk', '')
        mitigation = risk_fact.get('mitigation', '')
        action_plan.append(f"[Risk] {risk} - {mitigation}")

    # Extract scaling trigger (top 1)
    trigger_facts = [f for f in facts if isinstance(f, ScalingTriggerFact)]

    for trigger_fact in trigger_facts[:1]:
        trigger = trigger_fact.get('trigger', '')
        action_plan.append(f"[Scaling] {trigger}")

    return action_plan


def _build_resources(facts: list) -> list:
    """Build combined resources from tools, capabilities, partners, and cost tips"""
    resources = []

    # Extract tools (top 3)
    tool_facts = [f for f in facts if isinstance(f, ToolRecommendationFact)]

    for tool_fact in tool_facts[:3]:
        tool = tool_fact.get('tool', '')
        category = tool_fact.get('category', '').replace('_', ' ').title()
        resources.append(f"[Tool] {tool} - {category}")

    # Extract capabilities (top 2)
    capability_facts = [f for f in facts if isinstance(f, CapabilityRequirementFact)]
    importance_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
    sorted_capabilities = sorted(capability_facts, key=lambda f: importance_order.get(f.get('importance', 'Medium'), 3))

    for cap_fact in sorted_capabilities[:2]:
        capability = cap_fact.get('capability', '')
        importance = cap_fact.get('importance', 'Medium')
        resources.append(f"[Capability - {importance}] {capability}")

    # Extract partners (top 1)
    partner_facts = [f for f in facts if isinstance(f, PartnerRecommendationFact)]

    for partner_fact in partner_facts[:1]:
        partner = partner_fact.get('partner_type', '')
        resources.append(f"[Partner] {partner}")

    # Extract cost tips (top 2)
    cost_facts = [f for f in facts if isinstance(f, CostOptimizationFact)]

    for cost_fact in cost_facts[:2]:
        tip = cost_fact.get('tip', '')
        if tip:
            resources.append(f"[Cost Tip] {tip}")

    return resources
