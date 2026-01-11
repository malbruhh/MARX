# MARX Backend System Documentation

**Marketing Analysis Recommendation eXpert System**
Comprehensive Documentation for Expert System Backend

---

## Table of Contents
1. [Backend Flow: Button Click to JSON Response](#1-backend-flow)
2. [Input Facts (F1-F8)](#2-input-facts-f1-f8)
3. [Intermediate Facts](#3-intermediate-facts)
4. [Expert System Rules (104 Rules)](#4-expert-system-rules)
5. [Output Structure](#5-output-structure)
6. [Example Scenarios](#6-example-scenarios)

---

## 1. Backend Flow

### Complete Request-Response Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER CLICKS "ANALYZE" BUTTON IN FRONTEND                      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. HTTP POST REQUEST to /api/analyze                             │
│    - Endpoint: http://localhost:8000/api/analyze                 │
│    - Body: MarketingAnalysisRequest (JSON)                       │
│    - Content-Type: application/json                              │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. FASTAPI APP (app.py)                                          │
│    - Receives request at @app.post('/api/analyze')               │
│    - Validates request using Pydantic model                      │
│    - Calls: run_analysis(request)                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. CONTROLLER (controller.py)                                    │
│    - Function: run_analysis(request)                             │
│    - Calls: run_comprehensive_analysis(request)                  │
│    - Wraps result in {status: 'success', data: result}           │
│    - Handles exceptions → HTTPException(500)                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. SERVICE (comprehensive_service.py)                            │
│    - Function: run_comprehensive_analysis(request)               │
│    - Creates ComprehensiveMarketingEngine instance               │
│    - Declares initial facts (F1-F8) from request                 │
│    - Calls engine.run() to execute forward chaining              │
│    - Aggregates inferred facts into output                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. EXPERT SYSTEM ENGINE (comprehensive_engine.py)                │
│    - LAYERED FORWARD CHAINING EXECUTION                          │
│                                                                   │
│    Layer 0: Budget Classification (1 rule)                       │
│         F8 (RawBudget) → BudgetLevelFact                         │
│                                                                   │
│    Layer 1: Market Context Analysis (18 rules)                   │
│         F1, F2 → MarketMaturityFact, CompetitionLevelFact,       │
│                  CustomerAcquisitionComplexityFact, SalesCycleFact│
│                                                                   │
│    Layer 2: Strategic Direction (5 rules)                        │
│         F3, F4 + Layer 1 → StrategicApproachFact,                │
│                            MarketingFocusFact, MessagingAngleFact│
│                                                                   │
│    Layer 3: Channel Suitability (29 rules)                       │
│         All previous facts → ChannelPriorityFact (for each channel)│
│                              ChannelReadinessFact                │
│                                                                   │
│    Layer 4: Content Strategy (8 rules)                           │
│         F1, F2, F5 → ContentTypePriorityFact                     │
│                                                                   │
│    Layer 5: Tactical Quick Wins (6 rules)                        │
│         F1, F5, F6 + Budget → QuickWinFact                       │
│                                                                   │
│    Layer 6: KPI Recommendations (7 rules)                        │
│         F7, F3 → KPIRecommendationFact (primary & secondary)     │
│                                                                   │
│    Layer 7: Risk Assessment (6 rules)                            │
│         Budget, Competition, Content, Sales Cycle →              │
│              RiskIdentificationFact                              │
│                                                                   │
│    Layer 8: Budget Allocation (9 rules)                          │
│         Budget Level → BudgetCategoryFact, CostOptimizationFact  │
│                                                                   │
│    Layer 9: Scaling Strategy (5 rules)                           │
│         Strategic Approach, KPI → ScalingTriggerFact,            │
│                                   ScalingActionFact              │
│                                                                   │
│    Layer 10: Tools & Resources (15 rules)                        │
│         Budget, Product, Content → ToolRecommendationFact,       │
│                                    CapabilityRequirementFact,    │
│                                    PartnerRecommendationFact     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. AGGREGATION (comprehensive_service.py)                        │
│    - Extract all inferred facts from engine.facts                │
│    - Map ChannelPriorityFact → Strategy Codes (S1-S9)            │
│    - Generate 2-5 critical insights based on facts               │
│    - Calculate budget allocation per strategy                    │
│    - Generate channel tactics from facts                         │
│    - Build MarketingRecommendation object                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 8. JSON RESPONSE RETURNED TO FRONTEND                            │
│    {                                                              │
│      "status": "success",                                         │
│      "data": {                                                    │
│        "recommended_strategies": ["S1 - SEO", "S2 - PPC", ...],   │
│        "critical_insights": [...],                                │
│        "budget_allocation": [...],                                │
│        "total_monthly_budget": 1666.67,                           │
│        "channel_tactics": [...]                                   │
│      }                                                             │
│    }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

### How the Rules Work (Forward Chaining)

**Forward Chaining** is a data-driven inference method where the expert system starts with known facts and applies rules to infer new facts.

**Process:**
1. **Initialize**: Declare input facts (F1-F8) into the working memory
2. **Match**: Find all rules whose conditions are satisfied by current facts
3. **Fire**: Execute the matching rules (can fire multiple rules in parallel)
4. **Declare**: Rules declare new intermediate facts
5. **Repeat**: Steps 2-4 repeat until no new rules can fire
6. **Extract**: Collect all inferred facts for output generation

**Layered Approach:**
- Rules are organized in 10 layers (0-10)
- Each layer builds upon facts from previous layers
- This ensures systematic, hierarchical reasoning
- Prevents circular dependencies and infinite loops

**Example Rule Firing:**
```
Initial Fact: ProductFact(product_type="b2b_enterprise_saas")
              ↓
Rule Fires: market_maturity_b2b_saas()
              ↓
New Facts Declared: MarketMaturityFact(level="growth")
                    CompetitionLevelFact(level="high")
              ↓
These new facts can trigger more rules in next layer...
```

---

## 2. Input Facts (F1-F8)

Input facts are provided by the user through the frontend form.

| Code | Fact Category | Description | Possible Values |
|------|---------------|-------------|-----------------|
| **F1** | ProductFact | Product | b2b_enterprise_saas, b2c_retail_goods, local_service, high_end_consulting, digital_info_product, fast_moving_consumer_goods, niche_technical_tools, hospitality, subscription_recurring |
| **F2** | TargetCustomerFact | Customer | large_enterprise, small_to_medium_enterprise, gen_z, millenial, senior, local_community, niche_industry, budget_shopper, luxury |
| **F3** | PrimaryGoalFact | Goal | brand_awareness, immediate_lead_generation, customer_retention_loyalty |
| **F4** | TimeHorizonFact | Timeline | short_term (1-3mo), medium_term (3-6mo), long_term (6+mo) |
| **F5** | ContentCapabilityFact | Content | high_capability, medium_capability, low_capability |
| **F6** | SalesStructureFact | Sales | automated_ecommerce, dedicated_sales_team, owner_driven |
| **F7** | PriorityKPIFact | KPI | conversion_rate, customer_lifetime_value, organic_traffic_impressions, cost_per_acquisition, sales_qualified_leads |
| **F8** | RawBudget | Budget | Positive float value (USD) |

---

## 3. Intermediate Facts

Intermediate facts are inferred by the expert system during forward chaining. They represent derived knowledge.

### Layer 0 & 1: Context Facts
| Fact Type | Description | Possible Values |
|-----------|-------------|-----------------|
| **BudgetLevelFact** | Budget tier classification | micro (<$1k), low ($1k-$10k), medium ($10k-$100k), high ($100k-$1M), enterprise (>$1M) |
| **MarketMaturityFact** | Market development stage | emerging, growth, mature, saturated |
| **CompetitionLevelFact** | Competition intensity | low, moderate, high, very_high |
| **CustomerAcquisitionComplexityFact** | How hard to acquire customers | simple, moderate, complex, very_complex |

### Layer 2: Strategic Facts
| Fact Type | Description | Possible Values |
|-----------|-------------|-----------------|
| **StrategicApproachFact** | High-level strategy type | aggressive_growth, steady_growth, defensive, niche_domination |
| **MarketingFocusFact** | Primary marketing focus | acquisition, retention, expansion, brand_building |
| **SalesCycleFact** | Sales cycle length | immediate, short, medium, long, very_long |

### Layer 3-10: Tactical & Execution Facts
| Fact Type | Description | Attributes |
|-----------|-------------|------------|
| **ChannelPriorityFact** | Channel recommendation | channel (string), priority (1-5), budget_percent (float) |
| **ChannelReadinessFact** | Org readiness for channel | channel (string), readiness (ready/needs_preparation/not_suitable) |
| **ContentTypePriorityFact** | Content type priority | content_type (string), priority (1-5), frequency (string) |
| **MessagingAngleFact** | Messaging approach | angle (roi_focused, innovation, reliability, differentiation, etc.) |
| **QuickWinFact** | Immediate action items | action (string), priority (Critical/High/Medium/Low), effort (Low/Medium/High) |
| **TacticalActionFact** | Specific tactical step | action (string), timeline (string), priority (string) |
| **KPIRecommendationFact** | KPI to track | kpi (string), target (string), priority (primary/secondary) |
| **RiskIdentificationFact** | Identified risk | risk (string), severity (High/Medium/Low), mitigation (string) |
| **BudgetCategoryFact** | Budget category allocation | category (string), percentage (float) |
| **CostOptimizationFact** | Cost-saving tip | tip (string) |
| **ScalingTriggerFact** | When to scale | trigger (string) |
| **ScalingActionFact** | How to scale | action (string) |
| **ToolRecommendationFact** | Recommended tool | tool (string), category (string) |
| **CapabilityRequirementFact** | Required skill/capability | capability (string), importance (Critical/High/Medium) |
| **PartnerRecommendationFact** | Partner type to consider | partner_type (string) |

---

## 4. Expert System Rules

### Format Convention
```
IF: [Condition(s)]
THEN: [Action(s) - Declare new facts]
```

---

### LAYER 0: Budget Classification (1 Rule)

**Rule 1: classify_budget**
```
IF: RawBudget(amount=X)
THEN:
  - IF X ≤ 1000 → Declare BudgetLevelFact(tier=MICRO)
  - ELSE IF X ≤ 10000 → Declare BudgetLevelFact(tier=SMALL)
  - ELSE IF X ≤ 100000 → Declare BudgetLevelFact(tier=MEDIUM)
  - ELSE IF X ≤ 1000000 → Declare BudgetLevelFact(tier=LARGE)
  - ELSE → Declare BudgetLevelFact(tier=ENTERPRISE)
```

---

### LAYER 1: Market Context Analysis (18 Rules)

#### Market Maturity & Competition Rules (9 rules)

**Rule 2: market_maturity_b2b_saas**
```
IF: ProductFact(product_type=B2B_SAAS)
THEN:
  - Declare MarketMaturityFact(level="growth")
  - Declare CompetitionLevelFact(level="high")
```

**Rule 3: market_maturity_b2c_retail**
```
IF: ProductFact(product_type=B2C_RETAIL)
THEN:
  - Declare MarketMaturityFact(level="mature")
  - Declare CompetitionLevelFact(level="very_high")
```

**Rule 4: market_maturity_local_service**
```
IF: ProductFact(product_type=LOCAL_SERVICE)
THEN:
  - Declare MarketMaturityFact(level="mature")
  - Declare CompetitionLevelFact(level="moderate")
```

**Rule 5: market_maturity_consulting**
```
IF: ProductFact(product_type=CONSULTING)
THEN:
  - Declare MarketMaturityFact(level="mature")
  - Declare CompetitionLevelFact(level="high")
```

**Rule 6: market_maturity_digital_product**
```
IF: ProductFact(product_type=DIGITAL_PRODUCT)
THEN:
  - Declare MarketMaturityFact(level="growth")
  - Declare CompetitionLevelFact(level="high")
```

**Rule 7: market_maturity_fmcg**
```
IF: ProductFact(product_type=FMCG)
THEN:
  - Declare MarketMaturityFact(level="saturated")
  - Declare CompetitionLevelFact(level="very_high")
```

**Rule 8: market_maturity_technical_tools**
```
IF: ProductFact(product_type=TECHNICAL_TOOLS)
THEN:
  - Declare MarketMaturityFact(level="growth")
  - Declare CompetitionLevelFact(level="moderate")
```

**Rule 9: market_maturity_hospitality**
```
IF: ProductFact(product_type=HOSPITALITY)
THEN:
  - Declare MarketMaturityFact(level="mature")
  - Declare CompetitionLevelFact(level="high")
```

**Rule 10: market_maturity_subscription**
```
IF: ProductFact(product_type=SUBSCRIPTION)
THEN:
  - Declare MarketMaturityFact(level="growth")
  - Declare CompetitionLevelFact(level="high")
```

#### Customer Acquisition Complexity Rules (9 rules)

**Rule 11: acquisition_complexity_enterprise**
```
IF: TargetCustomerFact(customer=B2B_LARGE)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="very_complex")
  - Declare SalesCycleFact(cycle="very_long")
```

**Rule 12: acquisition_complexity_sme**
```
IF: TargetCustomerFact(customer=B2B_SME)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="complex")
  - Declare SalesCycleFact(cycle="medium")
```

**Rule 13: acquisition_complexity_digital_natives**
```
IF: TargetCustomerFact(customer=GEN_Z) OR TargetCustomerFact(customer=MILLENIAL)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="moderate")
  - Declare SalesCycleFact(cycle="short")
```

**Rule 14: acquisition_complexity_senior**
```
IF: TargetCustomerFact(customer=SENIOR)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="moderate")
  - Declare SalesCycleFact(cycle="medium")
```

**Rule 15: acquisition_complexity_local**
```
IF: TargetCustomerFact(customer=LOCAL)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="simple")
  - Declare SalesCycleFact(cycle="short")
```

**Rule 16: acquisition_complexity_niche**
```
IF: TargetCustomerFact(customer=NICHE)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="complex")
  - Declare SalesCycleFact(cycle="long")
```

**Rule 17: acquisition_complexity_budget**
```
IF: TargetCustomerFact(customer=BUDGET_SHOPPER)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="simple")
  - Declare SalesCycleFact(cycle="immediate")
```

**Rule 18: acquisition_complexity_luxury**
```
IF: TargetCustomerFact(customer=LUXURY)
THEN:
  - Declare CustomerAcquisitionComplexityFact(complexity="complex")
  - Declare SalesCycleFact(cycle="long")
```

---

### LAYER 2: Strategic Direction (5 Rules)

**Rule 19: strategic_approach_brand_building**
```
IF: PrimaryGoalFact(goal=AWARENESS) AND TimeHorizonFact(horizon=LONG)
THEN:
  - Declare StrategicApproachFact(approach="niche_domination")
  - Declare MarketingFocusFact(focus="brand_building")
```

**Rule 20: strategic_approach_aggressive_growth**
```
IF: PrimaryGoalFact(goal=LEAD_GEN) AND TimeHorizonFact(horizon=SHORT)
THEN:
  - Declare StrategicApproachFact(approach="aggressive_growth")
  - Declare MarketingFocusFact(focus="acquisition")
```

**Rule 21: strategic_approach_retention**
```
IF: PrimaryGoalFact(goal=RETENTION)
THEN:
  - Declare StrategicApproachFact(approach="defensive")
  - Declare MarketingFocusFact(focus="retention")
```

**Rule 22: strategic_approach_steady_growth**
```
IF: PrimaryGoalFact(goal=LEAD_GEN) AND TimeHorizonFact(horizon=MEDIUM)
THEN:
  - Declare StrategicApproachFact(approach="steady_growth")
  - Declare MarketingFocusFact(focus="acquisition")
```

**Rule 23: strategic_approach_differentiation**
```
IF: PrimaryGoalFact(goal=AWARENESS) AND CompetitionLevelFact(level="very_high")
THEN:
  - Declare StrategicApproachFact(approach="niche_domination")
  - Declare MessagingAngleFact(angle="differentiation")
```

---

### LAYER 3: Channel Suitability (29 Rules)

#### Paid Search Rules (3 rules)

**Rule 24: channel_paid_search_high_intent**
```
IF: (ProductFact(product_type=B2B_SAAS) OR ProductFact(product_type=LOCAL_SERVICE))
    AND BudgetLevelFact(tier=SMALL)
    AND PrimaryGoalFact(goal=LEAD_GEN)
THEN:
  - Declare ChannelPriorityFact(channel="paid_search", priority=1, budget_percent=35.0)
  - Declare ChannelReadinessFact(channel="paid_search", readiness="ready")
```

**Rule 25: channel_paid_search_limited_budget**
```
IF: BudgetLevelFact(tier=MICRO)
THEN:
  - Declare ChannelPriorityFact(channel="paid_search", priority=4, budget_percent=10.0)
```

**Rule 26: channel_paid_search_performance_focus**
```
IF: BudgetLevelFact(tier=MEDIUM) AND PriorityKPIFact(kpi=CPA)
THEN:
  - Declare ChannelPriorityFact(channel="paid_search", priority=2, budget_percent=30.0)
```

#### Paid Social Rules (3 rules)

**Rule 27: channel_paid_social_b2c_youth**
```
IF: ProductFact(product_type=B2C_RETAIL)
    AND (TargetCustomerFact(customer=GEN_Z) OR TargetCustomerFact(customer=MILLENIAL))
THEN:
  - Declare ChannelPriorityFact(channel="paid_social", priority=1, budget_percent=40.0)
  - Declare ChannelReadinessFact(channel="paid_social", readiness="ready")
```

**Rule 28: channel_linkedin_b2b**
```
IF: ProductFact(product_type=B2B_SAAS)
    AND TargetCustomerFact(customer=B2B_SME)
    AND BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare ChannelPriorityFact(channel="paid_social", priority=2, budget_percent=25.0)
```

**Rule 29: channel_paid_social_awareness**
```
IF: PrimaryGoalFact(goal=AWARENESS) AND BudgetLevelFact(tier=LARGE)
THEN:
  - Declare ChannelPriorityFact(channel="paid_social", priority=1, budget_percent=30.0)
```

#### Organic SEO Rules (3 rules)

**Rule 30: channel_organic_seo_longterm**
```
IF: TimeHorizonFact(horizon=LONG) AND PriorityKPIFact(kpi=TRAFFIC)
THEN:
  - Declare ChannelPriorityFact(channel="organic_seo", priority=1, budget_percent=25.0)
```

**Rule 31: channel_organic_seo_content_strength**
```
IF: ContentCapabilityFact(capability=HIGH)
THEN:
  - Declare ChannelPriorityFact(channel="organic_seo", priority=2, budget_percent=20.0)
  - Declare ChannelReadinessFact(channel="organic_seo", readiness="ready")
```

**Rule 32: channel_organic_seo_budget_constrained**
```
IF: BudgetLevelFact(tier=MICRO) AND TimeHorizonFact(horizon=LONG)
THEN:
  - Declare ChannelPriorityFact(channel="organic_seo", priority=1, budget_percent=40.0)
```

#### Email Marketing Rules (3 rules)

**Rule 33: channel_email_retention**
```
IF: PrimaryGoalFact(goal=RETENTION)
THEN:
  - Declare ChannelPriorityFact(channel="email_marketing", priority=1, budget_percent=20.0)
```

**Rule 34: channel_email_nurture**
```
IF: SalesCycleFact(cycle="long") AND PrimaryGoalFact(goal=LEAD_GEN)
THEN:
  - Declare ChannelPriorityFact(channel="email_marketing", priority=2, budget_percent=15.0)
```

**Rule 35: channel_email_subscription**
```
IF: ProductFact(product_type=SUBSCRIPTION)
THEN:
  - Declare ChannelPriorityFact(channel="email_marketing", priority=1, budget_percent=25.0)
```

#### Content Marketing Rules (2 rules)

**Rule 36: channel_content_thought_leadership**
```
IF: ContentCapabilityFact(capability=HIGH)
    AND (ProductFact(product_type=B2B_SAAS) OR ProductFact(product_type=CONSULTING))
THEN:
  - Declare ChannelPriorityFact(channel="content_marketing", priority=1, budget_percent=30.0)
```

**Rule 37: channel_content_brand_building**
```
IF: PrimaryGoalFact(goal=AWARENESS) AND TimeHorizonFact(horizon=LONG)
THEN:
  - Declare ChannelPriorityFact(channel="content_marketing", priority=2, budget_percent=25.0)
```

#### Influencer Marketing Rules (1 rule)

**Rule 38: channel_influencer_b2c_youth**
```
IF: ProductFact(product_type=B2C_RETAIL)
    AND (TargetCustomerFact(customer=GEN_Z) OR TargetCustomerFact(customer=MILLENIAL))
    AND BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare ChannelPriorityFact(channel="influencer", priority=2, budget_percent=20.0)
```

#### Events & Webinars Rules (2 rules)

**Rule 39: channel_events_b2b_enterprise**
```
IF: (ProductFact(product_type=B2B_SAAS) OR ProductFact(product_type=CONSULTING))
    AND BudgetLevelFact(tier=LARGE)
THEN:
  - Declare ChannelPriorityFact(channel="events_webinars", priority=2, budget_percent=20.0)
```

**Rule 40: channel_events_complex_sales**
```
IF: CustomerAcquisitionComplexityFact(complexity="very_complex")
    AND SalesCycleFact(cycle="very_long")
THEN:
  - Declare ChannelPriorityFact(channel="events_webinars", priority=1, budget_percent=25.0)
```

#### Community Building Rules (2 rules)

**Rule 41: channel_community_technical**
```
IF: ProductFact(product_type=TECHNICAL_TOOLS) AND TargetCustomerFact(customer=NICHE)
THEN:
  - Declare ChannelPriorityFact(channel="community", priority=1, budget_percent=15.0)
```

**Rule 42: channel_community_local**
```
IF: ProductFact(product_type=LOCAL_SERVICE)
THEN:
  - Declare ChannelPriorityFact(channel="community", priority=2, budget_percent=10.0)
```

#### Local SEO Rules (2 rules)

**Rule 43: channel_local_seo_service**
```
IF: ProductFact(product_type=LOCAL_SERVICE) AND TargetCustomerFact(customer=LOCAL)
THEN:
  - Declare ChannelPriorityFact(channel="local_seo", priority=1, budget_percent=30.0)
```

**Rule 44: channel_local_seo_hospitality**
```
IF: ProductFact(product_type=HOSPITALITY)
THEN:
  - Declare ChannelPriorityFact(channel="local_seo", priority=1, budget_percent=25.0)
```

#### Retargeting Rules (2 rules)

**Rule 45: channel_retargeting_conversion**
```
IF: PriorityKPIFact(kpi=CR) AND BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare ChannelPriorityFact(channel="retargeting", priority=2, budget_percent=15.0)
```

**Rule 46: channel_retargeting_nurture**
```
IF: SalesCycleFact(cycle="medium")
THEN:
  - Declare ChannelPriorityFact(channel="retargeting", priority=3, budget_percent=10.0)
```

#### Referral Program Rules (2 rules)

**Rule 47: channel_referral_clv_focus**
```
IF: PriorityKPIFact(kpi=CLV) AND PrimaryGoalFact(goal=RETENTION)
THEN:
  - Declare ChannelPriorityFact(channel="referral", priority=2, budget_percent=10.0)
```

**Rule 48: channel_referral_subscription**
```
IF: ProductFact(product_type=SUBSCRIPTION)
THEN:
  - Declare ChannelPriorityFact(channel="referral", priority=2, budget_percent=12.0)
```

---

### LAYER 4: Content Strategy (8 Rules)

**Rule 49: content_thought_leadership_blog**
```
IF: ContentCapabilityFact(capability=HIGH)
    AND (ProductFact(product_type=B2B_SAAS) OR ProductFact(product_type=CONSULTING))
THEN:
  - Declare ContentTypePriorityFact(content_type="blog_articles", priority=1, frequency="3-4 per week")
```

**Rule 50: content_video_youth**
```
IF: (TargetCustomerFact(customer=GEN_Z) OR TargetCustomerFact(customer=MILLENIAL))
    AND ContentCapabilityFact(capability=MEDIUM)
THEN:
  - Declare ContentTypePriorityFact(content_type="video_content", priority=1, frequency="2-3 per week")
```

**Rule 51: content_case_studies_enterprise**
```
IF: ProductFact(product_type=B2B_SAAS) AND TargetCustomerFact(customer=B2B_LARGE)
THEN:
  - Declare ContentTypePriorityFact(content_type="case_studies", priority=1, frequency="2 per month")
```

**Rule 52: content_whitepapers_complex**
```
IF: CustomerAcquisitionComplexityFact(complexity="very_complex")
    AND ContentCapabilityFact(capability=HIGH)
THEN:
  - Declare ContentTypePriorityFact(content_type="whitepapers", priority=2, frequency="1 per month")
```

**Rule 53: content_webinars_nurture**
```
IF: SalesCycleFact(cycle="long") AND BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare ContentTypePriorityFact(content_type="webinars", priority=2, frequency="2 per month")
```

**Rule 54: content_social_posts_retail**
```
IF: ProductFact(product_type=B2C_RETAIL)
THEN:
  - Declare ContentTypePriorityFact(content_type="social_posts", priority=1, frequency="daily")
```

**Rule 55: content_newsletter_retention**
```
IF: PrimaryGoalFact(goal=RETENTION) AND ProductFact(product_type=SUBSCRIPTION)
THEN:
  - Declare ContentTypePriorityFact(content_type="email_newsletters", priority=1, frequency="weekly")
```

**Rule 56: content_ugc_budget**
```
IF: ProductFact(product_type=B2C_RETAIL) AND BudgetLevelFact(tier=MICRO)
THEN:
  - Declare ContentTypePriorityFact(content_type="user_generated", priority=1, frequency="ongoing")
```

---

### LAYER 5: Tactical Quick Wins (6 Rules)

**Rule 57: quickwin_gmb_optimization**
```
IF: ProductFact(product_type=LOCAL_SERVICE) AND BudgetLevelFact(tier=MICRO)
THEN:
  - Declare QuickWinFact(action="Optimize Google My Business listing", priority="Critical", effort="Low")
```

**Rule 58: quickwin_content_calendar**
```
IF: ContentCapabilityFact(capability=LOW) AND BudgetLevelFact(tier=MICRO)
THEN:
  - Declare QuickWinFact(action="Set up 30-day content calendar", priority="High", effort="Low")
```

**Rule 59: quickwin_email_automation**
```
IF: SalesStructureFact(structure=AUTOMATED)
THEN:
  - Declare QuickWinFact(action="Implement welcome email sequence", priority="High", effort="Medium")
```

**Rule 60: quickwin_cro_audit**
```
IF: PriorityKPIFact(kpi=CR) AND SalesStructureFact(structure=AUTOMATED)
THEN:
  - Declare QuickWinFact(action="Conduct conversion funnel audit", priority="Critical", effort="Medium")
```

**Rule 61: quickwin_linkedin_optimization**
```
IF: ProductFact(product_type=B2B_SAAS)
THEN:
  - Declare QuickWinFact(action="Optimize LinkedIn company page and start posting", priority="High", effort="Low")
```

**Rule 62: quickwin_competitor_analysis**
```
IF: BudgetLevelFact(tier=MICRO)
THEN:
  - Declare QuickWinFact(action="Complete competitor marketing analysis", priority="High", effort="Low")
```

---

### LAYER 6: KPI Recommendations (7 Rules)

**Rule 63: kpi_conversion_rate**
```
IF: PriorityKPIFact(kpi=CR)
THEN:
  - Declare KPIRecommendationFact(kpi="Website Conversion Rate", target="2-5% improvement per quarter", priority="primary")
  - Declare KPIRecommendationFact(kpi="Landing Page Conversion Rate", target="10-20% for cold traffic", priority="primary")
```

**Rule 64: kpi_customer_lifetime_value**
```
IF: PriorityKPIFact(kpi=CLV)
THEN:
  - Declare KPIRecommendationFact(kpi="Customer Lifetime Value", target="3x customer acquisition cost minimum", priority="primary")
  - Declare KPIRecommendationFact(kpi="Repeat Purchase Rate", target="25-40% depending on industry", priority="primary")
```

**Rule 65: kpi_organic_traffic**
```
IF: PriorityKPIFact(kpi=TRAFFIC)
THEN:
  - Declare KPIRecommendationFact(kpi="Organic Traffic Growth", target="15-30% monthly growth", priority="primary")
  - Declare KPIRecommendationFact(kpi="Domain Authority", target="+5 points per quarter", priority="secondary")
```

**Rule 66: kpi_cost_per_acquisition**
```
IF: PriorityKPIFact(kpi=CPA)
THEN:
  - Declare KPIRecommendationFact(kpi="Cost Per Acquisition", target="<33% of customer LTV", priority="primary")
  - Declare KPIRecommendationFact(kpi="Return on Ad Spend", target="3:1 minimum, 5:1 target", priority="primary")
```

**Rule 67: kpi_sales_qualified_leads**
```
IF: PriorityKPIFact(kpi=SQL)
THEN:
  - Declare KPIRecommendationFact(kpi="Sales Qualified Leads", target="20% MQL to SQL conversion", priority="primary")
  - Declare KPIRecommendationFact(kpi="SQL to Close Rate", target="25-40% depending on sales cycle", priority="primary")
```

**Rule 68: kpi_awareness_metrics**
```
IF: PrimaryGoalFact(goal=AWARENESS)
THEN:
  - Declare KPIRecommendationFact(kpi="Brand Awareness (Surveys)", target="15-25% increase quarterly", priority="secondary")
  - Declare KPIRecommendationFact(kpi="Social Media Reach", target="20% monthly growth", priority="secondary")
```

**Rule 69: kpi_saas_specific**
```
IF: ProductFact(product_type=B2B_SAAS)
THEN:
  - Declare KPIRecommendationFact(kpi="Monthly Recurring Revenue Growth", target="10-20% monthly", priority="secondary")
  - Declare KPIRecommendationFact(kpi="Churn Rate", target="<5% monthly", priority="secondary")
```

---

### LAYER 7: Risk Assessment (6 Rules)

**Rule 70: risk_limited_budget**
```
IF: BudgetLevelFact(tier=MICRO)
THEN:
  - Declare RiskIdentificationFact(risk="Limited budget may restrict channel diversification", severity="High", mitigation="Focus on 1-2 high-ROI channels, leverage organic and low-cost tactics")
```

**Rule 71: risk_high_competition**
```
IF: CompetitionLevelFact(level="very_high") AND BudgetLevelFact(tier=SMALL)
THEN:
  - Declare RiskIdentificationFact(risk="High competition may make paid channels expensive", severity="High", mitigation="Focus on long-tail keywords, niche positioning, and organic growth")
```

**Rule 72: risk_low_content_capability**
```
IF: ContentCapabilityFact(capability=LOW)
THEN:
  - Declare RiskIdentificationFact(risk="Low content capability limits content marketing effectiveness", severity="Medium", mitigation="Invest in content training, hire freelancers, or use AI tools")
```

**Rule 73: risk_sales_timeline_mismatch**
```
IF: SalesCycleFact(cycle="very_long") AND TimeHorizonFact(horizon=SHORT)
THEN:
  - Declare RiskIdentificationFact(risk="Short timeline incompatible with long sales cycle", severity="High", mitigation="Set realistic expectations, focus on pipeline building not closed deals")
```

**Rule 74: risk_owner_bottleneck**
```
IF: SalesStructureFact(structure=OWNER_DRIVEN)
THEN:
  - Declare RiskIdentificationFact(risk="Owner-driven sales may limit scalability", severity="Medium", mitigation="Implement marketing automation, nurture sequences, and self-service options")
```

**Rule 75: risk_cpa_volatility**
```
IF: ProductFact(product_type=B2C_RETAIL) AND PriorityKPIFact(kpi=CPA)
THEN:
  - Declare RiskIdentificationFact(risk="B2C ad costs can fluctuate seasonally", severity="Medium", mitigation="Diversify traffic sources, build organic channels, reserve budget for peak seasons")
```

---

### LAYER 8: Budget Allocation (9 Rules)

**Rule 76: budget_allocation_micro**
```
IF: BudgetLevelFact(tier=MICRO)
THEN:
  - Declare BudgetCategoryFact(category="Organic Marketing", percentage=60.0)
  - Declare BudgetCategoryFact(category="Paid Advertising", percentage=20.0)
  - Declare BudgetCategoryFact(category="Tools & Software", percentage=10.0)
  - Declare BudgetCategoryFact(category="Content Creation", percentage=10.0)
```

**Rule 77: budget_allocation_small**
```
IF: BudgetLevelFact(tier=SMALL)
THEN:
  - Declare BudgetCategoryFact(category="Paid Advertising", percentage=35.0)
  - Declare BudgetCategoryFact(category="Content Marketing", percentage=25.0)
  - Declare BudgetCategoryFact(category="Tools & Software", percentage=15.0)
  - Declare BudgetCategoryFact(category="SEO & Organic", percentage=15.0)
  - Declare BudgetCategoryFact(category="Marketing Operations", percentage=10.0)
```

**Rule 78: budget_allocation_medium**
```
IF: BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare BudgetCategoryFact(category="Paid Advertising", percentage=40.0)
  - Declare BudgetCategoryFact(category="Content & SEO", percentage=25.0)
  - Declare BudgetCategoryFact(category="Marketing Technology", percentage=15.0)
  - Declare BudgetCategoryFact(category="Events & Partnerships", percentage=10.0)
  - Declare BudgetCategoryFact(category="Team & Freelancers", percentage=10.0)
```

**Rule 79: budget_allocation_large**
```
IF: BudgetLevelFact(tier=LARGE)
THEN:
  - Declare BudgetCategoryFact(category="Paid Media Mix", percentage=45.0)
  - Declare BudgetCategoryFact(category="Brand & Content", percentage=20.0)
  - Declare BudgetCategoryFact(category="Marketing Team", percentage=15.0)
  - Declare BudgetCategoryFact(category="Technology Stack", percentage=10.0)
  - Declare BudgetCategoryFact(category="Events & PR", percentage=10.0)
```

**Rule 80: budget_allocation_enterprise**
```
IF: BudgetLevelFact(tier=ENTERPRISE)
THEN:
  - Declare BudgetCategoryFact(category="Multi-Channel Paid Media", percentage=40.0)
  - Declare BudgetCategoryFact(category="Brand & Demand Gen", percentage=20.0)
  - Declare BudgetCategoryFact(category="Marketing Organization", percentage=20.0)
  - Declare BudgetCategoryFact(category="MarTech & Analytics", percentage=10.0)
  - Declare BudgetCategoryFact(category="Strategic Partnerships", percentage=10.0)
```

**Rule 81: cost_optimization_micro**
```
IF: BudgetLevelFact(tier=MICRO)
THEN:
  - Declare CostOptimizationFact(tip="Use free tools: Google Analytics, Google Search Console, Mailchimp free tier")
  - Declare CostOptimizationFact(tip="Leverage organic social media before paid ads")
  - Declare CostOptimizationFact(tip="Create content in-house or use AI writing assistants")
```

**Rule 82: cost_optimization_performance**
```
IF: BudgetLevelFact(tier=SMALL) AND PriorityKPIFact(kpi=CPA)
THEN:
  - Declare CostOptimizationFact(tip="Start with long-tail keywords for lower CPCs")
  - Declare CostOptimizationFact(tip="Use retargeting to improve conversion efficiency")
  - Declare CostOptimizationFact(tip="A/B test ad creative weekly to improve CTR")
```

**Rule 83: cost_optimization_content**
```
IF: ContentCapabilityFact(capability=LOW)
THEN:
  - Declare CostOptimizationFact(tip="Repurpose content across multiple channels")
  - Declare CostOptimizationFact(tip="Use user-generated content and testimonials")
  - Declare CostOptimizationFact(tip="Curate industry content instead of always creating original")
```

---

### LAYER 9: Scaling Strategy (5 Rules)

**Rule 84: scaling_trigger_cpa**
```
IF: PriorityKPIFact(kpi=CPA)
THEN:
  - Declare ScalingTriggerFact(trigger="When CPA is below target for 2 consecutive weeks")
```

**Rule 85: scaling_trigger_traffic**
```
IF: PriorityKPIFact(kpi=TRAFFIC)
THEN:
  - Declare ScalingTriggerFact(trigger="When organic traffic grows 20% month-over-month")
```

**Rule 86: scaling_trigger_clv**
```
IF: PriorityKPIFact(kpi=CLV)
THEN:
  - Declare ScalingTriggerFact(trigger="When CLV:CAC ratio exceeds 3:1")
```

**Rule 87: scaling_action_aggressive**
```
IF: StrategicApproachFact(approach="aggressive_growth") AND BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare ScalingActionFact(action="Increase winning channel budgets by 50% when efficiency maintained")
  - Declare ScalingActionFact(action="Expand to 2-3 new channels after proving core channels")
```

**Rule 88: scaling_action_steady**
```
IF: StrategicApproachFact(approach="steady_growth")
THEN:
  - Declare ScalingActionFact(action="Increase budgets 20% monthly while maintaining target metrics")
  - Declare ScalingActionFact(action="Test one new channel per quarter")
```

---

### LAYER 10: Tools & Resources (15 Rules)

**Rule 89: tools_micro_budget**
```
IF: BudgetLevelFact(tier=MICRO)
THEN:
  - Declare ToolRecommendationFact(tool="Google Analytics (free)", category="analytics")
  - Declare ToolRecommendationFact(tool="Mailchimp Free Tier", category="email")
  - Declare ToolRecommendationFact(tool="Canva Free", category="design")
  - Declare ToolRecommendationFact(tool="Buffer Free", category="social_media")
```

**Rule 90: tools_small_budget**
```
IF: BudgetLevelFact(tier=SMALL)
THEN:
  - Declare ToolRecommendationFact(tool="Google Ads", category="paid_search")
  - Declare ToolRecommendationFact(tool="Mailchimp or ConvertKit", category="email")
  - Declare ToolRecommendationFact(tool="SEMrush or Ahrefs (basic)", category="seo")
  - Declare ToolRecommendationFact(tool="Hootsuite or Buffer", category="social_media")
```

**Rule 91: tools_medium_budget**
```
IF: BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare ToolRecommendationFact(tool="HubSpot or Marketo", category="marketing_automation")
  - Declare ToolRecommendationFact(tool="SEMrush Enterprise", category="seo")
  - Declare ToolRecommendationFact(tool="Google Analytics + Data Studio", category="analytics")
  - Declare ToolRecommendationFact(tool="Sprout Social", category="social_media")
```

**Rule 92: tools_b2b_saas**
```
IF: ProductFact(product_type=B2B_SAAS)
THEN:
  - Declare ToolRecommendationFact(tool="LinkedIn Sales Navigator", category="prospecting")
  - Declare ToolRecommendationFact(tool="Clearbit", category="data_enrichment")
  - Declare ToolRecommendationFact(tool="Intercom or Drift", category="conversational_marketing")
```

**Rule 93: tools_b2c_retail**
```
IF: ProductFact(product_type=B2C_RETAIL)
THEN:
  - Declare ToolRecommendationFact(tool="Facebook Ads Manager", category="paid_social")
  - Declare ToolRecommendationFact(tool="Klaviyo", category="email_ecommerce")
  - Declare ToolRecommendationFact(tool="Google Merchant Center", category="product_ads")
```

**Rule 94: tools_content_creation**
```
IF: ContentCapabilityFact(capability=HIGH)
THEN:
  - Declare ToolRecommendationFact(tool="BuzzSumo", category="content_research")
  - Declare ToolRecommendationFact(tool="Grammarly Premium", category="content_quality")
  - Declare ToolRecommendationFact(tool="Loom or Descript", category="video_content")
```

**Rule 95: capability_content_writing**
```
IF: ContentCapabilityFact(capability=LOW)
    AND (ProductFact(product_type=B2B_SAAS) OR ProductFact(product_type=CONSULTING))
THEN:
  - Declare CapabilityRequirementFact(capability="Content Writing & Thought Leadership", importance="Critical")
```

**Rule 96: capability_marketing_automation**
```
IF: SalesStructureFact(structure=AUTOMATED)
THEN:
  - Declare CapabilityRequirementFact(capability="Marketing Automation & Email Workflows", importance="High")
```

**Rule 97: capability_data_analysis**
```
IF: BudgetLevelFact(tier=MEDIUM)
THEN:
  - Declare CapabilityRequirementFact(capability="Data Analysis & Performance Optimization", importance="High")
```

**Rule 98: capability_social_media**
```
IF: TargetCustomerFact(customer=GEN_Z) OR TargetCustomerFact(customer=MILLENIAL)
THEN:
  - Declare CapabilityRequirementFact(capability="Social Media Management & Community Engagement", importance="High")
```

**Rule 99: capability_seo_technical**
```
IF: ProductFact(product_type=B2B_SAAS)
THEN:
  - Declare CapabilityRequirementFact(capability="Technical SEO & Content Optimization", importance="Medium")
```

**Rule 100: partner_content_agency**
```
IF: BudgetLevelFact(tier=MEDIUM) AND ContentCapabilityFact(capability=LOW)
THEN:
  - Declare PartnerRecommendationFact(partner_type="Content Marketing Agency or Freelance Writers")
```

**Rule 101: partner_paid_media_agency**
```
IF: BudgetLevelFact(tier=LARGE) AND CompetitionLevelFact(level="very_high")
THEN:
  - Declare PartnerRecommendationFact(partner_type="Specialized Paid Media Agency (Google Ads, Facebook Ads)")
```

**Rule 102: partner_influencer_platform**
```
IF: ProductFact(product_type=B2C_RETAIL)
THEN:
  - Declare PartnerRecommendationFact(partner_type="Influencer Marketing Platform or Agency")
```

**Rule 103: partner_pr_firm**
```
IF: ProductFact(product_type=B2B_SAAS) AND TargetCustomerFact(customer=B2B_LARGE)
THEN:
  - Declare PartnerRecommendationFact(partner_type="B2B PR Firm for Media Relations")
```

**Rule 104: partner_local_seo**
```
IF: ProductFact(product_type=LOCAL_SERVICE)
THEN:
  - Declare PartnerRecommendationFact(partner_type="Local SEO Specialist or Agency")
```

---

## 5. Output Structure

### Simplified Output Schema

```json
{
  "recommended_strategies": [
    "S1 - Search Engine Optimization (SEO)",
    "S2 - Pay-Per-Click (PPC) Advertising",
    "S5 - Content Marketing"
  ],

  "critical_insights": [
    "Insight 1: Strategic direction based on primary goal",
    "Insight 2: Budget-specific channel strategy",
    "Insight 3: Product-specific marketing approach",
    "Insight 4: Time horizon considerations (optional)",
    "Insight 5: Content capability leverage (optional)"
  ],

  "budget_allocation": [
    {
      "strategy_code": "S1 - Search Engine Optimization (SEO)",
      "percentage": 30.0,
      "monthly_amount": 500.00
    },
    {
      "strategy_code": "S2 - Pay-Per-Click (PPC) Advertising",
      "percentage": 40.0,
      "monthly_amount": 666.67
    },
    {
      "strategy_code": "S5 - Content Marketing",
      "percentage": 30.0,
      "monthly_amount": 500.00
    }
  ],

  "total_monthly_budget": 1666.67,

  "channel_tactics": [
    {
      "strategy_code": "S1 - Search Engine Optimization (SEO)",
      "tactic": "Optimize website for target keywords and create SEO-focused content pillars",
      "priority": "High",
      "expected_outcome": "Increase organic traffic by 30-50% over 3-6 months"
    },
    {
      "strategy_code": "S2 - Pay-Per-Click (PPC) Advertising",
      "tactic": "Launch targeted PPC campaigns on Google Ads with A/B tested ad copy",
      "priority": "High",
      "expected_outcome": "Generate qualified leads with target CPA below industry average"
    },
    {
      "strategy_code": "S5 - Content Marketing",
      "tactic": "Create value-driven content (blogs, videos, guides) addressing customer pain points",
      "priority": "Medium",
      "expected_outcome": "Establish thought leadership and generate inbound leads"
    }
  ]
}
```

### Strategy Code Mapping

| Code | Strategy Name | Channel Mapping |
|------|---------------|-----------------|
| **S1** | Search Engine Optimization (SEO) | organic_seo_content |
| **S2** | Pay-Per-Click (PPC) Advertising | paid_search_google_ads |
| **S3** | Social Media Marketing (SMM) | paid_social_facebook_instagram_linkedin |
| **S4** | Email Marketing/Newsletters | email_marketing |
| **S5** | Content Marketing | content_marketing_blog_video |
| **S6** | Local SEO (Google My Business) | local_seo_gmb |
| **S7** | Account-Based Marketing (ABM) | *Special: B2B_SAAS + B2B_LARGE + SALES_TEAM* |
| **S8** | Trade Shows/Conferences | events_and_webinars |
| **S9** | Influencer/Partnership Marketing | influencer_partnerships, strategic_partnerships |

---

## 6. Example Scenarios

### Example 1: Local Coffee Shop

#### Input
```json
{
  "product_type": "local_service",
  "target_customer": "local_community",
  "primary_goal": "brand_awareness",
  "time_horizon": "medium_term",
  "content_capability": "medium_capability",
  "sales_structure": "owner_driven",
  "priority_kpi": "organic_traffic_impressions",
  "raw_budget_amount": 2000.0
}
```

#### Rules Firing & Evaluation

**Layer 0: Budget Classification**
- Rule 1 fires: 2000 > 1000 AND ≤ 10000 → `BudgetLevelFact(tier=SMALL)`

**Layer 1: Market Context**
- Rule 4 fires: LOCAL_SERVICE → `MarketMaturityFact(level="mature")`, `CompetitionLevelFact(level="moderate")`
- Rule 15 fires: LOCAL customer → `CustomerAcquisitionComplexityFact(complexity="simple")`, `SalesCycleFact(cycle="short")`

**Layer 2: Strategic Direction**
- No exact match, but awareness + medium = partial match patterns considered

**Layer 3: Channel Suitability**
- Rule 43 fires: LOCAL_SERVICE + LOCAL → `ChannelPriorityFact(channel="local_seo", priority=1, budget_percent=30.0)`
- Rule 42 fires: LOCAL_SERVICE → `ChannelPriorityFact(channel="community", priority=2, budget_percent=10.0)`
- Rule 30 fires: TRAFFIC KPI → `ChannelPriorityFact(channel="organic_seo", priority=1, budget_percent=25.0)` *(Note: depends on time horizon=medium, may not fire)*
- Rule 31 fires: MEDIUM content → `ChannelPriorityFact(channel="organic_seo", priority=2, budget_percent=20.0)`

**Layer 4: Content Strategy**
- Rule 54 may fire partially based on social needs

**Layer 5: Quick Wins**
- Rule 57 fires: LOCAL_SERVICE + MICRO... wait, SMALL budget, doesn't fire
- Rule 62 fires: SMALL budget → `QuickWinFact(action="Complete competitor marketing analysis", ...)`

**Layer 6: KPI Recommendations**
- Rule 65 fires: TRAFFIC KPI → KPI facts for organic traffic growth, domain authority
- Rule 68 fires: AWARENESS goal → KPI facts for brand awareness surveys, social reach

**Layer 7: Risk Assessment**
- Rule 74 fires: OWNER_DRIVEN → `RiskIdentificationFact(risk="Owner-driven sales may limit scalability", ...)`

**Layer 8: Budget Allocation**
- Rule 77 fires: SMALL budget → Budget category facts (35% paid, 25% content, etc.)
- Rule 83 may fire: if LOW content (not in this case, MEDIUM)

**Layer 9 & 10: Scaling & Tools**
- Rule 85 fires: TRAFFIC KPI → Scaling trigger
- Rule 90 fires: SMALL budget → Tool recommendations (Google Ads, Mailchimp, SEMrush, Buffer)

#### Output
```json
{
  "recommended_strategies": [
    "S6 - Local SEO (Google My Business)",
    "S1 - Search Engine Optimization (SEO)",
    "S5 - Content Marketing"
  ],

  "critical_insights": [
    "Focus on brand visibility and reach - prioritize content distribution and thought leadership to build market presence",
    "With limited budget, concentrate on high-ROI organic channels (SEO, content) and test paid channels with small experiments",
    "Local dominance is key - prioritize Google My Business, local SEO, and community engagement to capture nearby customers"
  ],

  "budget_allocation": [
    {
      "strategy_code": "S6 - Local SEO (Google My Business)",
      "percentage": 40.0,
      "monthly_amount": 200.00
    },
    {
      "strategy_code": "S1 - Search Engine Optimization (SEO)",
      "percentage": 35.0,
      "monthly_amount": 175.00
    },
    {
      "strategy_code": "S5 - Content Marketing",
      "percentage": 25.0,
      "monthly_amount": 125.00
    }
  ],

  "total_monthly_budget": 500.00,

  "channel_tactics": [
    {
      "strategy_code": "S6 - Local SEO (Google My Business)",
      "tactic": "Optimize Google My Business profile and collect customer reviews",
      "priority": "High",
      "expected_outcome": "Rank in top 3 local map pack for primary keywords"
    },
    {
      "strategy_code": "S1 - Search Engine Optimization (SEO)",
      "tactic": "Optimize website for target keywords and create SEO-focused content pillars",
      "priority": "High",
      "expected_outcome": "Increase organic traffic by 30-50% over 3-6 months"
    },
    {
      "strategy_code": "S5 - Content Marketing",
      "tactic": "Create value-driven content (blogs, videos, guides) addressing customer pain points",
      "priority": "Medium",
      "expected_outcome": "Establish thought leadership and generate inbound leads"
    }
  ]
}
```

---

### Example 2: Enterprise B2B SaaS Company

#### Input
```json
{
  "product_type": "b2b_enterprise_saas",
  "target_customer": "large_enterprise",
  "primary_goal": "immediate_lead_generation",
  "time_horizon": "short_term",
  "content_capability": "high_capability",
  "sales_structure": "dedicated_sales_team",
  "priority_kpi": "sales_qualified_leads",
  "raw_budget_amount": 150000.0
}
```

#### Rules Firing & Evaluation

**Layer 0: Budget Classification**
- Rule 1 fires: 150000 > 100000 AND ≤ 1000000 → `BudgetLevelFact(tier=LARGE)`

**Layer 1: Market Context**
- Rule 2 fires: B2B_SAAS → `MarketMaturityFact(level="growth")`, `CompetitionLevelFact(level="high")`
- Rule 11 fires: B2B_LARGE → `CustomerAcquisitionComplexityFact(complexity="very_complex")`, `SalesCycleFact(cycle="very_long")`

**Layer 2: Strategic Direction**
- Rule 20 fires: LEAD_GEN + SHORT → `StrategicApproachFact(approach="aggressive_growth")`, `MarketingFocusFact(focus="acquisition")`

**Layer 3: Channel Suitability**
- Rule 39 fires: B2B_SAAS + LARGE budget → `ChannelPriorityFact(channel="events_webinars", priority=2, budget_percent=20.0)`
- Rule 40 fires: very_complex + very_long → `ChannelPriorityFact(channel="events_webinars", priority=1, budget_percent=25.0)` *(overrides priority)*
- Rule 36 fires: HIGH content + B2B_SAAS → `ChannelPriorityFact(channel="content_marketing", priority=1, budget_percent=30.0)`
- Rule 29 fires: AWARENESS... wait, goal is LEAD_GEN, doesn't fire
- Multiple other channel rules fire based on budget and product type

**Layer 4: Content Strategy**
- Rule 49 fires: HIGH content + B2B_SAAS → `ContentTypePriorityFact(content_type="blog_articles", priority=1, frequency="3-4 per week")`
- Rule 51 fires: B2B_SAAS + B2B_LARGE → `ContentTypePriorityFact(content_type="case_studies", priority=1, frequency="2 per month")`
- Rule 52 fires: very_complex + HIGH content → `ContentTypePriorityFact(content_type="whitepapers", priority=2, frequency="1 per month")`
- Rule 53 fires: long cycle + MEDIUM... wait, LARGE budget → `ContentTypePriorityFact(content_type="webinars", priority=2, frequency="2 per month")`

**Layer 5: Quick Wins**
- Rule 61 fires: B2B_SAAS → `QuickWinFact(action="Optimize LinkedIn company page and start posting", ...)`

**Layer 6: KPI Recommendations**
- Rule 67 fires: SQL KPI → KPI facts for SQL, MQL to SQL conversion, SQL to close rate
- Rule 69 fires: B2B_SAAS → KPI facts for MRR growth, churn rate

**Layer 7: Risk Assessment**
- Rule 73 fires: very_long cycle + SHORT horizon → `RiskIdentificationFact(risk="Short timeline incompatible with long sales cycle", severity="High", mitigation="Set realistic expectations, focus on pipeline building not closed deals")`

**Layer 8: Budget Allocation**
- Rule 79 fires: LARGE budget → Budget category facts (45% paid media, 20% brand/content, 15% team, etc.)

**Layer 9: Scaling Strategy**
- Rule 87 fires: aggressive_growth + MEDIUM... wait, LARGE budget (rule expects MEDIUM, may not fire exactly)
- Other scaling rules fire based on KPI

**Layer 10: Tools & Resources**
- Rule 91 fires: MEDIUM... wait, LARGE budget (uses medium tier tools)
- Rule 92 fires: B2B_SAAS → Tools like LinkedIn Sales Navigator, Clearbit, Intercom
- Rule 94 fires: HIGH content → BuzzSumo, Grammarly, Loom
- Rule 95 doesn't fire: Content is HIGH not LOW
- Rule 96 doesn't fire: Sales is SALES_TEAM not AUTOMATED
- Rule 99 fires: B2B_SAAS → Technical SEO capability needed
- Rule 103 fires: B2B_SAAS + B2B_LARGE → B2B PR Firm partner recommendation

#### Output
```json
{
  "recommended_strategies": [
    "S7 - Account-Based Marketing (ABM)",
    "S8 - Trade Shows/Conferences",
    "S5 - Content Marketing"
  ],

  "critical_insights": [
    "Optimize for conversion - implement targeted campaigns with clear CTAs and lead capture mechanisms",
    "Leverage multi-channel approach - diversify across paid and organic to maximize reach while maintaining efficiency",
    "B2B buyers need education and trust - create case studies, whitepapers, and demonstrate ROI through content",
    "Short timeline requires immediate action - prioritize paid channels and quick-win optimizations over long-term SEO",
    "Maximize your content strength - produce authoritative resources that attract organic traffic and establish industry credibility"
  ],

  "budget_allocation": [
    {
      "strategy_code": "S7 - Account-Based Marketing (ABM)",
      "percentage": 25.0,
      "monthly_amount": 4166.67
    },
    {
      "strategy_code": "S8 - Trade Shows/Conferences",
      "percentage": 40.0,
      "monthly_amount": 6666.67
    },
    {
      "strategy_code": "S5 - Content Marketing",
      "percentage": 35.0,
      "monthly_amount": 5833.33
    }
  ],

  "total_monthly_budget": 16666.67,

  "channel_tactics": [
    {
      "strategy_code": "S7 - Account-Based Marketing (ABM)",
      "tactic": "Identify top 20 target accounts and create personalized outreach campaigns",
      "priority": "High",
      "expected_outcome": "Increase enterprise deal closure rate by 40%"
    },
    {
      "strategy_code": "S8 - Trade Shows/Conferences",
      "tactic": "Attend industry conferences and host booth/speaking sessions",
      "priority": "High",
      "expected_outcome": "Generate 50-100 qualified leads per event"
    },
    {
      "strategy_code": "S5 - Content Marketing",
      "tactic": "Create value-driven content (blogs, videos, guides) addressing customer pain points",
      "priority": "High",
      "expected_outcome": "Establish thought leadership and generate inbound leads"
    }
  ]
}
```

---

## Summary

**Total Rules: 104 rules across 10 layers**
- Layer 0: 1 rule (Budget Classification)
- Layer 1: 18 rules (Market Context)
- Layer 2: 5 rules (Strategic Direction)
- Layer 3: 29 rules (Channel Suitability)
- Layer 4: 8 rules (Content Strategy)
- Layer 5: 6 rules (Quick Wins)
- Layer 6: 7 rules (KPIs)
- Layer 7: 6 rules (Risk Assessment)
- Layer 8: 9 rules (Budget Allocation)
- Layer 9: 5 rules (Scaling)
- Layer 10: 15 rules (Tools & Resources)

**Expert System Architecture:**
- **Input Facts**: 8 user-provided facts (F1-F8)
- **Intermediate Facts**: 16 fact types inferred through reasoning
- **Forward Chaining**: Layered execution ensures systematic inference
- **Output**: Simplified, actionable marketing recommendations (S1-S9 strategies)

---

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**System:** MARX (Marketing Analysis Recommendation eXpert System)
