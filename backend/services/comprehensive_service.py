"""
Comprehensive Marketing Analysis Service
Integrates the layered expert system and produces structured recommendations
"""
from services.comprehensive_engine import ComprehensiveMarketingEngine
from models.model import *
from models.request import MarketingAnalysisRequest
from models.output import *
from models.intermediate_facts import *
from collections import defaultdict
import calendar

def run_comprehensive_analysis(request: MarketingAnalysisRequest) -> MarketingRecommendation:
    """
    Run comprehensive marketing analysis using layered forward chaining
    Returns structured, multi-dimensional recommendations
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

        # Aggregate inferred facts into structured output
        recommendation = _aggregate_recommendations(engine, request)

        return recommendation

    except Exception as e:
        import traceback
        error_detail = f"Error in comprehensive marketing analysis: {str(e)}\n{traceback.format_exc()}"
        raise Exception(error_detail)


def _aggregate_recommendations(engine: ComprehensiveMarketingEngine, request: MarketingAnalysisRequest) -> MarketingRecommendation:
    """
    Aggregate all inferred facts from the engine into a comprehensive recommendation
    """

    # Get facts from knowledge base
    facts = list(engine.facts.values())

    # Extract intermediate facts
    channel_priorities = _extract_channel_priorities(facts)
    content_priorities = _extract_content_priorities(facts)
    kpi_recommendations = _extract_kpi_recommendations(facts)
    risks = _extract_risks(facts)
    quick_wins = _extract_quick_wins(facts)
    tactical_actions = _extract_tactical_actions(facts, request)
    budget_categories = _extract_budget_categories(facts)
    cost_tips = _extract_cost_optimization(facts)
    scaling_triggers = _extract_scaling_triggers(facts)
    scaling_actions = _extract_scaling_actions(facts)
    tools = _extract_tools(facts)
    capabilities = _extract_capabilities(facts)
    partners = _extract_partners(facts)

    # Generate strategic summaries
    strategy_summary = _generate_strategy_summary(request, facts)
    strategic_positioning = _generate_strategic_positioning(request, facts)
    channel_mix_rationale = _generate_channel_rationale(request, channel_priorities)
    messaging_focus = _generate_messaging_focus(request, facts)
    differentiation_strategy = _generate_differentiation_strategy(request, facts)
    scaling_strategy = _generate_scaling_strategy(scaling_actions)

    # Generate content themes
    content_themes = _generate_content_themes(request)

    # Generate competitive advantages
    competitive_advantages = _generate_competitive_advantages(request)

    # Calculate monthly burn rate
    monthly_burn_rate = request.raw_budget_amount / _get_months_for_horizon(request.time_horizon)

    # Build comprehensive recommendation
    return MarketingRecommendation(
        strategy_summary=strategy_summary,
        strategic_positioning=strategic_positioning,
        primary_channels=channel_priorities[:5],  # Top 5 channels
        channel_mix_rationale=channel_mix_rationale,
        content_strategy=content_priorities[:5],  # Top 5 content types
        content_themes=content_themes,
        messaging_focus=messaging_focus,
        quick_wins=quick_wins,
        short_term_actions=tactical_actions['short_term'],
        medium_term_actions=tactical_actions['medium_term'],
        long_term_actions=tactical_actions['long_term'],
        primary_kpis=kpi_recommendations['primary'],
        secondary_kpis=kpi_recommendations['secondary'],
        risks_and_mitigations=risks,
        budget_allocation_summary=budget_categories,
        monthly_burn_rate=round(monthly_burn_rate, 2),
        cost_optimization_tips=cost_tips,
        competitive_advantages=competitive_advantages,
        differentiation_strategy=differentiation_strategy,
        scaling_triggers=scaling_triggers,
        scaling_strategy=scaling_strategy,
        recommended_tools=tools,
        required_capabilities=capabilities,
        potential_partners=partners
    )


def _extract_channel_priorities(facts) -> List[ChannelRecommendation]:
    """Extract and rank channel recommendations"""
    channel_map = defaultdict(lambda: {'priority': 5, 'budget': 0})

    for fact in facts:
        if isinstance(fact, ChannelPriorityFact):
            if fact['priority'] < channel_map[fact['channel']]['priority']:
                channel_map[fact['channel']]['priority'] = fact['priority']
            channel_map[fact['channel']]['budget'] = max(
                channel_map[fact['channel']]['budget'],
                fact['budget_percent']
            )

    # Convert to ChannelRecommendation objects
    channel_recommendations = []
    rationales = _get_channel_rationales()
    expected_impacts = _get_channel_impacts()

    for channel, data in channel_map.items():
        channel_recommendations.append(ChannelRecommendation(
            channel=_map_channel_string_to_enum(channel),
            priority=data['priority'],
            budget_allocation_percent=data['budget'],
            rationale=rationales.get(channel, "Recommended based on your business profile"),
            expected_impact=expected_impacts.get(channel, "Positive impact on key metrics")
        ))

    # Sort by priority (1 is highest)
    channel_recommendations.sort(key=lambda x: (x.priority, -x.budget_allocation_percent))

    # Normalize budget percentages to sum to 100%
    total_budget = sum(c.budget_allocation_percent for c in channel_recommendations[:5])
    if total_budget > 0:
        for channel in channel_recommendations[:5]:
            channel.budget_allocation_percent = round((channel.budget_allocation_percent / total_budget) * 100, 1)

    return channel_recommendations


def _extract_content_priorities(facts) -> List[ContentRecommendation]:
    """Extract content recommendations"""
    content_map = {}

    for fact in facts:
        if isinstance(fact, ContentTypePriorityFact):
            if fact['content_type'] not in content_map or fact['priority'] < content_map[fact['content_type']]['priority']:
                content_map[fact['content_type']] = {
                    'priority': fact['priority'],
                    'frequency': fact['frequency']
                }

    content_recommendations = []
    topic_map = _get_content_topic_map()
    distribution_map = _get_content_distribution_map()

    for content_type, data in content_map.items():
        content_recommendations.append(ContentRecommendation(
            content_type=_map_content_string_to_enum(content_type),
            frequency=data['frequency'],
            priority=data['priority'],
            target_topics=topic_map.get(content_type, ["Industry insights", "Product benefits", "Customer success"]),
            distribution_channels=distribution_map.get(content_type, ["Website", "Social media", "Email"])
        ))

    content_recommendations.sort(key=lambda x: x.priority)
    return content_recommendations


def _extract_kpi_recommendations(facts) -> Dict[str, List[KPITarget]]:
    """Extract KPI recommendations categorized by priority"""
    primary_kpis = []
    secondary_kpis = []

    for fact in facts:
        if isinstance(fact, KPIRecommendationFact):
            kpi = KPITarget(
                metric_name=fact['kpi'],
                target_value=fact['target'],
                measurement_frequency="Weekly" if 'conversion' in fact['kpi'].lower() else "Monthly",
                benchmark=None
            )

            if fact['priority'] == 'primary':
                primary_kpis.append(kpi)
            else:
                secondary_kpis.append(kpi)

    return {'primary': primary_kpis, 'secondary': secondary_kpis}


def _extract_risks(facts) -> List[RiskFactor]:
    """Extract risk factors"""
    risks = []

    for fact in facts:
        if isinstance(fact, RiskIdentificationFact):
            risks.append(RiskFactor(
                risk=fact['risk'],
                severity=fact['severity'],
                mitigation=fact['mitigation']
            ))

    return risks


def _extract_quick_wins(facts) -> List[TacticalAction]:
    """Extract quick win actions"""
    quick_wins = []

    for fact in facts:
        if isinstance(fact, QuickWinFact):
            quick_wins.append(TacticalAction(
                action=fact['action'],
                timeline="Week 1-4",
                priority=fact['priority'],
                estimated_effort=fact['effort'],
                expected_outcome="Immediate impact on marketing foundation",
                dependencies=[]
            ))

    # Sort by priority
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    quick_wins.sort(key=lambda x: priority_order.get(x.priority, 4))

    return quick_wins


def _extract_tactical_actions(facts, request: MarketingAnalysisRequest) -> Dict[str, List[TacticalAction]]:
    """Generate tactical actions for different time horizons"""

    # These are strategic actions based on the overall analysis
    short_term = [
        TacticalAction(
            action="Set up analytics tracking and conversion funnels",
            timeline="Month 1",
            priority="Critical",
            estimated_effort="Medium",
            expected_outcome="Complete visibility into marketing performance",
            dependencies=[]
        ),
        TacticalAction(
            action="Launch first campaign on primary channel",
            timeline="Month 1-2",
            priority="High",
            estimated_effort="High",
            expected_outcome="Initial lead flow and performance data",
            dependencies=["Analytics setup"]
        )
    ]

    # Add content-specific actions
    if request.content_capability == ContentCapability.HIGH:
        short_term.append(TacticalAction(
            action="Publish comprehensive content piece (whitepaper/guide)",
            timeline="Month 2-3",
            priority="High",
            estimated_effort="High",
            expected_outcome="Lead magnet and SEO authority building",
            dependencies=[]
        ))

    medium_term = [
        TacticalAction(
            action="Expand to secondary channels based on performance data",
            timeline="Month 3-4",
            priority="High",
            estimated_effort="Medium",
            expected_outcome="Diversified traffic sources and reduced channel risk",
            dependencies=["Primary channel performance validation"]
        ),
        TacticalAction(
            action="Implement marketing automation workflows",
            timeline="Month 4-5",
            priority="Medium",
            estimated_effort="High",
            expected_outcome="Improved lead nurturing and conversion efficiency",
            dependencies=["Email list of 500+ leads"]
        )
    ]

    # Add retention actions if applicable
    if request.primary_goal == PrimaryGoal.RETENTION:
        medium_term.append(TacticalAction(
            action="Launch customer loyalty or referral program",
            timeline="Month 5-6",
            priority="High",
            estimated_effort="High",
            expected_outcome="Increased customer lifetime value and organic growth",
            dependencies=["Customer base of 100+ active users"]
        ))

    long_term = [
        TacticalAction(
            action="Conduct comprehensive marketing audit and optimization",
            timeline="Month 6-9",
            priority="Medium",
            estimated_effort="Medium",
            expected_outcome="Refined strategy based on 6 months of data",
            dependencies=[]
        ),
        TacticalAction(
            action="Scale successful channels and test advanced tactics",
            timeline="Month 9-12",
            priority="High",
            estimated_effort="High",
            expected_outcome="Accelerated growth with proven playbooks",
            dependencies=["Positive ROI on existing channels"]
        )
    ]

    # Add brand-building actions for long-term awareness goals
    if request.primary_goal == PrimaryGoal.AWARENESS and request.time_horizon == TimeHorizon.LONG:
        long_term.append(TacticalAction(
            action="Develop brand partnership or sponsorship strategy",
            timeline="Month 10-12",
            priority="Medium",
            estimated_effort="High",
            expected_outcome="Enhanced brand recognition and credibility",
            dependencies=["Established market presence"]
        ))

    return {
        'short_term': short_term,
        'medium_term': medium_term,
        'long_term': long_term
    }


def _extract_budget_categories(facts) -> Dict[str, float]:
    """Extract budget allocation by category"""
    budget_dict = {}

    for fact in facts:
        if isinstance(fact, BudgetCategoryFact):
            budget_dict[fact['category']] = fact['percentage']

    return budget_dict


def _extract_cost_optimization(facts) -> List[str]:
    """Extract cost optimization tips"""
    tips = []

    for fact in facts:
        if isinstance(fact, CostOptimizationFact):
            tips.append(fact['tip'])

    return tips


def _extract_scaling_triggers(facts) -> List[str]:
    """Extract scaling triggers"""
    triggers = []

    for fact in facts:
        if isinstance(fact, ScalingTriggerFact):
            triggers.append(fact['trigger'])

    # Add default triggers if none found
    if not triggers:
        triggers = [
            "Consistent positive ROI for 3+ months",
            "Marketing qualified leads exceed sales capacity",
            "Customer acquisition cost below industry benchmark"
        ]

    return triggers


def _extract_scaling_actions(facts) -> List[str]:
    """Extract scaling actions"""
    actions = []

    for fact in facts:
        if isinstance(fact, ScalingActionFact):
            actions.append(fact['action'])

    return actions


def _extract_tools(facts) -> List[str]:
    """Extract recommended tools"""
    tools = []

    for fact in facts:
        if isinstance(fact, ToolRecommendationFact):
            tools.append(fact['tool'])

    # Remove duplicates while preserving order
    return list(dict.fromkeys(tools))


def _extract_capabilities(facts) -> List[str]:
    """Extract required capabilities"""
    capabilities = []

    for fact in facts:
        if isinstance(fact, CapabilityRequirementFact):
            capabilities.append(f"{fact['capability']} (Importance: {fact['importance']})")

    return capabilities


def _extract_partners(facts) -> List[str]:
    """Extract potential partners"""
    partners = []

    for fact in facts:
        if isinstance(fact, PartnerRecommendationFact):
            partners.append(fact['partner_type'])

    return partners


def _generate_strategy_summary(request: MarketingAnalysisRequest, facts) -> str:
    """Generate high-level strategy summary"""

    product_strategies = {
        ProductType.B2B_SAAS: "enterprise SaaS solution",
        ProductType.B2C_RETAIL: "consumer retail offering",
        ProductType.LOCAL_SERVICE: "local service business",
        ProductType.CONSULTING: "high-end consulting practice",
        ProductType.DIGITAL_PRODUCT: "digital product",
        ProductType.FMCG: "consumer packaged goods",
        ProductType.TECHNICAL_TOOLS: "technical tools",
        ProductType.HOSPITALITY: "hospitality business",
        ProductType.SUBSCRIPTION: "subscription service"
    }

    goal_strategies = {
        PrimaryGoal.AWARENESS: "brand awareness and market presence",
        PrimaryGoal.LEAD_GEN: "lead generation and customer acquisition",
        PrimaryGoal.RETENTION: "customer retention and lifetime value maximization"
    }

    budget_context = {
        BudgetLevel.MICRO: "with a focus on high-impact, low-cost tactics",
        BudgetLevel.SMALL: "balancing paid and organic channels",
        BudgetLevel.MEDIUM: "leveraging a multi-channel approach",
        BudgetLevel.LARGE: "with comprehensive demand generation",
        BudgetLevel.ENTERPRISE: "through full-scale enterprise marketing"
    }

    # Determine budget level from facts
    budget_level = BudgetLevel.MEDIUM
    for fact in facts:
        if isinstance(fact, BudgetLevelFact):
            budget_level = BudgetLevel(fact['tier'])
            break

    return f"Comprehensive marketing strategy for your {product_strategies.get(request.product_type, 'business')} " \
           f"focused on {goal_strategies.get(request.primary_goal, 'growth')} " \
           f"{budget_context.get(budget_level, '')} over a {request.time_horizon.value.replace('_', '-')} time horizon."


def _generate_strategic_positioning(request: MarketingAnalysisRequest, facts) -> str:
    """Generate strategic positioning recommendation"""

    if request.product_type in [ProductType.B2B_SAAS, ProductType.CONSULTING]:
        return "Position as a thought leader and trusted advisor in your industry. Emphasize expertise, reliability, and proven results through case studies and data-driven content."
    elif request.product_type == ProductType.B2C_RETAIL:
        if request.target_customer == TargetCustomer.LUXURY:
            return "Position as a premium, aspirational brand. Focus on exclusivity, quality, and brand storytelling to justify premium pricing."
        elif request.target_customer == TargetCustomer.BUDGET_SHOPPER:
            return "Position as the value leader in your category. Emphasize affordability, practicality, and smart shopping without compromising quality."
        else:
            return "Position based on unique product benefits and lifestyle alignment. Create emotional connections through authentic storytelling and social proof."
    elif request.product_type == ProductType.LOCAL_SERVICE:
        return "Position as the trusted local expert. Leverage community engagement, reviews, and local partnerships to build credibility and word-of-mouth referrals."
    elif request.product_type == ProductType.TECHNICAL_TOOLS:
        return "Position as the technical solution of choice for practitioners. Focus on product superiority, integration capabilities, and developer advocacy."
    else:
        return "Differentiate through unique value proposition and customer success stories. Build trust through transparency, proof points, and consistent delivery."


def _generate_channel_rationale(request: MarketingAnalysisRequest, channels: List[ChannelRecommendation]) -> str:
    """Generate rationale for channel mix"""

    if not channels:
        return "Diversified channel approach based on your business profile."

    primary_channel = channels[0].channel.value.replace('_', ' ').title()

    if request.primary_goal == PrimaryGoal.LEAD_GEN:
        return f"Channel mix optimized for lead generation with {primary_channel} as the primary driver. " \
               f"Secondary channels provide diversification and support the customer journey from awareness to conversion."
    elif request.primary_goal == PrimaryGoal.AWARENESS:
        return f"Broad-reach channel strategy with emphasis on {primary_channel} to maximize brand visibility. " \
               f"Multi-channel presence ensures consistent touchpoints across the customer journey."
    else:
        return f"Retention-focused channel mix with {primary_channel} as the anchor for ongoing customer engagement. " \
               f"Supporting channels nurture relationships and drive repeat business."


def _generate_messaging_focus(request: MarketingAnalysisRequest, facts) -> str:
    """Generate messaging focus recommendation"""

    messaging_angle = None
    for fact in facts:
        if isinstance(fact, MessagingAngleFact):
            messaging_angle = fact['angle']
            break

    if messaging_angle == "differentiation":
        return "Focus messaging on unique differentiators that set you apart from competitors. Emphasize what only you can offer."
    elif request.priority_kpi == PriorityKPI.CPA:
        return "ROI-focused messaging that emphasizes tangible business outcomes and fast time-to-value."
    elif request.priority_kpi == PriorityKPI.CLV:
        return "Value-driven messaging focused on long-term benefits, customer success, and partnership approach."
    elif request.product_type == ProductType.CONSULTING:
        return "Expertise-led messaging that positions you as the authority. Share insights, perspectives, and thought leadership."
    else:
        return "Customer-centric messaging that addresses pain points, aspirations, and desired outcomes. Focus on benefits over features."


def _generate_differentiation_strategy(request: MarketingAnalysisRequest, facts) -> str:
    """Generate differentiation strategy"""

    competition_level = "moderate"
    for fact in facts:
        if isinstance(fact, CompetitionLevelFact):
            competition_level = fact['level']
            break

    if competition_level == "very_high":
        return "In a highly competitive market, differentiate through niche specialization, exceptional customer experience, " \
               "or innovative positioning. Avoid competing purely on price or generic features."
    elif competition_level == "high":
        return "Stand out through superior content marketing, stronger social proof, and more personalized customer engagement. " \
               "Build brand preference through consistency and quality."
    else:
        return "Leverage your position in a less saturated market to establish category leadership. Focus on building trust " \
               "and becoming the go-to solution before competitors intensify."


def _generate_scaling_strategy(scaling_actions: List[str]) -> str:
    """Generate scaling strategy description"""

    if scaling_actions:
        return "Scale marketing investment systematically based on performance triggers. " + " ".join(scaling_actions[:2])
    else:
        return "Scale incrementally as channels prove ROI. Increase budgets 20-30% monthly while maintaining or improving efficiency metrics. " \
               "Test new channels only after optimizing existing ones."


def _generate_content_themes(request: MarketingAnalysisRequest) -> List[str]:
    """Generate content themes based on business type"""

    theme_map = {
        ProductType.B2B_SAAS: [
            "Industry trends and insights",
            "Product tutorials and best practices",
            "Customer success stories and ROI metrics",
            "Thought leadership on business challenges",
            "Competitive comparisons and buying guides"
        ],
        ProductType.B2C_RETAIL: [
            "Lifestyle content and inspiration",
            "Product styling and usage ideas",
            "Customer testimonials and reviews",
            "Behind-the-scenes and brand story",
            "Seasonal trends and gift guides"
        ],
        ProductType.LOCAL_SERVICE: [
            "Local community involvement",
            "Customer testimonials and before/after",
            "Service education and tips",
            "Team spotlights and company culture",
            "Local events and partnerships"
        ],
        ProductType.CONSULTING: [
            "Industry analysis and market insights",
            "Methodologies and frameworks",
            "Case studies and transformation stories",
            "Speaking engagements and conference content",
            "Research reports and original data"
        ],
        ProductType.DIGITAL_PRODUCT: [
            "Educational content and tutorials",
            "Success strategies and frameworks",
            "User-generated success stories",
            "Industry news and commentary",
            "Product updates and roadmap"
        ]
    }

    return theme_map.get(request.product_type, [
        "Industry insights and trends",
        "Product benefits and use cases",
        "Customer success stories",
        "Educational content",
        "Company news and updates"
    ])


def _generate_competitive_advantages(request: MarketingAnalysisRequest) -> List[str]:
    """Generate competitive advantages to emphasize"""

    advantages = []

    if request.content_capability == ContentCapability.HIGH:
        advantages.append("Strong content creation capability enables thought leadership positioning")

    if request.sales_structure == SalesStructure.SALES_TEAM:
        advantages.append("Dedicated sales team allows for high-touch customer engagement")
    elif request.sales_structure == SalesStructure.AUTOMATED:
        advantages.append("Automated sales process enables scalability and efficiency")

    if request.product_type in [ProductType.B2B_SAAS, ProductType.TECHNICAL_TOOLS]:
        advantages.append("Technical product depth creates barriers to switching")

    if request.product_type == ProductType.LOCAL_SERVICE:
        advantages.append("Local market presence and community relationships")

    if request.time_horizon == TimeHorizon.LONG:
        advantages.append("Long-term perspective allows for sustainable brand building")

    # Add at least a few generic advantages
    if len(advantages) < 3:
        advantages.extend([
            "Focused strategy aligned with business goals",
            "Data-driven approach to marketing investment",
            "Agile execution with continuous optimization"
        ])

    return advantages[:5]


def _get_months_for_horizon(horizon: TimeHorizon) -> int:
    """Convert time horizon to months"""
    if horizon == TimeHorizon.SHORT:
        return 2
    elif horizon == TimeHorizon.MEDIUM:
        return 4.5
    else:
        return 9


def _map_channel_string_to_enum(channel_str: str) -> ChannelType:
    """Map channel string to ChannelType enum"""
    mapping = {
        'paid_search': ChannelType.PAID_SEARCH,
        'paid_social': ChannelType.PAID_SOCIAL,
        'organic_seo': ChannelType.ORGANIC_SEO,
        'email_marketing': ChannelType.EMAIL_MARKETING,
        'content_marketing': ChannelType.CONTENT_MARKETING,
        'influencer': ChannelType.INFLUENCER,
        'events_webinars': ChannelType.EVENTS_WEBINARS,
        'community': ChannelType.COMMUNITY,
        'local_seo': ChannelType.LOCAL_SEO,
        'retargeting': ChannelType.RETARGETING,
        'referral': ChannelType.REFERRAL
    }
    return mapping.get(channel_str, ChannelType.ORGANIC_SEO)


def _map_content_string_to_enum(content_str: str) -> ContentType:
    """Map content string to ContentType enum"""
    mapping = {
        'blog_articles': ContentType.BLOG_ARTICLES,
        'video_content': ContentType.VIDEO_CONTENT,
        'case_studies': ContentType.CASE_STUDIES,
        'whitepapers': ContentType.WHITEPAPERS,
        'webinars': ContentType.WEBINARS,
        'social_posts': ContentType.SOCIAL_POSTS,
        'email_newsletters': ContentType.EMAIL_NEWSLETTERS,
        'user_generated': ContentType.USER_GENERATED
    }
    return mapping.get(content_str, ContentType.BLOG_ARTICLES)


def _get_channel_rationales() -> Dict[str, str]:
    """Get rationales for each channel"""
    return {
        'paid_search': "High-intent users actively searching for solutions like yours",
        'paid_social': "Precise targeting and visual storytelling capabilities",
        'organic_seo': "Long-term sustainable traffic with compound returns",
        'email_marketing': "Direct communication channel with highest ROI potential",
        'content_marketing': "Builds authority and supports entire customer journey",
        'influencer': "Leverage trusted voices to reach target audience authentically",
        'events_webinars': "Deep engagement and relationship building with prospects",
        'community': "Organic growth through engaged user base and advocates",
        'local_seo': "Critical for local discovery and mobile search traffic",
        'retargeting': "Re-engage warm audience with high conversion potential",
        'referral': "Lowest cost acquisition through existing customer advocacy"
    }


def _get_channel_impacts() -> Dict[str, str]:
    """Get expected impacts for each channel"""
    return {
        'paid_search': "Immediate qualified traffic and lead flow",
        'paid_social': "Brand awareness and engagement at scale",
        'organic_seo': "Sustainable traffic growth and authority building",
        'email_marketing': "Improved conversion and customer lifetime value",
        'content_marketing': "Thought leadership and inbound lead generation",
        'influencer': "Expanded reach and social proof",
        'events_webinars': "High-quality pipeline and relationship development",
        'community': "Customer retention and organic advocacy",
        'local_seo': "Increased local visibility and foot traffic",
        'retargeting': "Improved conversion rates and sales efficiency",
        'referral': "Lower CAC and higher quality customers"
    }


def _get_content_topic_map() -> Dict[str, List[str]]:
    """Get topic recommendations for content types"""
    return {
        'blog_articles': ["Industry insights", "How-to guides", "Best practices", "Trends analysis"],
        'video_content': ["Product demos", "Customer testimonials", "Behind-the-scenes", "Tutorials"],
        'case_studies': ["Customer success stories", "ROI demonstrations", "Implementation stories"],
        'whitepapers': ["Research findings", "Industry reports", "Strategic frameworks"],
        'webinars': ["Expert panels", "Product deep-dives", "Q&A sessions", "Training workshops"],
        'social_posts': ["Daily tips", "User stories", "Product highlights", "Industry news"],
        'email_newsletters': ["Curated insights", "Product updates", "Exclusive offers", "Success stories"],
        'user_generated': ["Customer photos", "Reviews", "Testimonials", "Community content"]
    }


def _get_content_distribution_map() -> Dict[str, List[str]]:
    """Get distribution channel recommendations for content types"""
    return {
        'blog_articles': ["Website/Blog", "LinkedIn", "Medium", "Email newsletter"],
        'video_content': ["YouTube", "Social media", "Website", "Email"],
        'case_studies': ["Website resources", "Sales collateral", "LinkedIn", "Email campaigns"],
        'whitepapers': ["Gated website content", "LinkedIn", "Industry publications"],
        'webinars': ["Email promotion", "LinkedIn", "Partner channels", "Website"],
        'social_posts': ["Instagram", "Facebook", "LinkedIn", "Twitter"],
        'email_newsletters': ["Email marketing platform", "Website signup"],
        'user_generated': ["Social media", "Website testimonials", "Marketing materials"]
    }
