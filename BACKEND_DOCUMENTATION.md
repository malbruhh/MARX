# MARX Backend Technical Documentation

This documentation provides a deep dive into the MARX Expert System's architecture, reasoning logic, and data structures.

---

## 1. System Architecture & Flow

The MARX backend is built using a **Layered Pipe-and-Filter** pattern integrated with a **Forward Chaining Knowledge Engine**.

### The Execution Flow:
1.  **API Gateway (FastAPI)**: Receives a `MarketingAnalysisRequest` with user selections.
2.  **Controller Layer**: Validates input and passes it to the asynchronous service.
3.  **Service Layer**: Instantiates the `ComprehensiveMarketingEngine` and injects **Input Facts**.
4.  **Inference Engine (Experta)**: Executes 12 layers of rules (Forward Chaining) to derive strategy.
5.  **Aggregation Logic**: Collects hundreds of inferred facts and deduplicates them using **Layer-First Overrides**.
6.  **Response**: Returns the refined `MarketingRecommendation`.

### Forward Chaining Method:
The system uses the Rete algorithm-based `experta` engine. Rules fire when their conditions are met, which in turn "declares" new facts. These new facts trigger further rules (e.g., `ProductType` $\rightarrow$ `MarketMaturity` $\rightarrow$ `StrategicApproach` $\rightarrow$ `ChannelPriority`).

---

## 2. Fact Categories & Data

### A. Input Facts (The Seeding Phase)
These are directly declared from the user's initial choices:
- `ProductFact`: The industry (B2B SaaS, Retail, etc.)
- `TargetCustomerFact`: The demographic or persona.
- `RawBudget`: The total USD amount.
- `PrimaryGoalFact`: Growth, Awareness, or Retention.
- `TimeHorizonFact`: Short, Medium, or Long term.
- `ContentCapabilityFact`: Organizational ability to produce media.
- `SalesStructureFact`: Automated vs. Sales Team led.
- `PriorityKPIFact`: The metric that matters most.

### B. Intermediate Facts (The Reasoning Phase)
Created during layers 1–10 to bridge the gap between "Input" and "Recommendation":
- `MarketMaturityFact`: Inferred level of saturation (e.g., Growth, Mature).
- `CompetitionLevelFact`: Inferred difficulty (Low to Very High).
- `CustomerAcquisitionComplexityFact`: Based on B2B/B2C and Ticket Size.
- `SalesCycleFact`: Inferred time to close (Immediate to Very Long).
- `StrategicApproachFact`: High-level mode (e.g., Niche Domination).
- `MessagingAngleFact`: The "Hook" (ROI, Innovation, Reliability).

---

## 3. The 12-Layer Override System

To ensure sensitivity, the engine uses a **Layered Override Architecture**:

| Layer | Name | Role | Baseline Priority |
| :--- | :--- | :--- | :--- |
| **0** | Budget Class | Converts raw money to tiers (Micro to Enterprise). | N/A |
| **1-2** | Context Analysis | Infers Market and Strategy facts. | N/A |
| **3C** | **Base Rules** | Sets standard industry defaults. | **Priority 6-8 (Neutral)** |
| **3D-3E** | **Audience/Combo** | Promotes/Inhibits based on specific segments. | **Priority 2-4 (High)** |
| **4-10** | Content & Tactics | Generates specific "how-to" recommendations. | N/A |
| **11** | **Universal Constraints** | Hard overrides for Time Horizon & Budget limits. | **Override Layer 5+** |
| **12** | **High-Dimensional Jitter** | Complex rule triplets for precise "micro-shifts". | **Override Layer 10** |

**The Override Logic**: If two rules recommend the same channel (e.g., SEO), the aggregator chooses the one from the **highest layer**. If layers are equal, it chooses the **lowest priority number**.

---

## 4. Possible Outputs

The result is a `MarketingRecommendation` object containing:
1.  **Recommended Strategies**: List of codes (S1–S9) like `S1 - SEO`, `S2 - PPC`, etc.
2.  **Critical Insights**: 2-5 high-level strategic takeaways.
3.  **Budget Allocation**: Percentage and Dollar breakdown per strategy.
4.  **Channel Tactics**: Actionable tasks with expected outcomes.
5.  **Action Plan**: Combined list of Quick Wins, KPIs, and Risks.
6.  **Resources**: Recommended Tools, Capabilities, and Partners.

---

## 5. Reasoning Examples

### Example 1: The Modernist Persona
- **Input**: B2C Retail + Gen Z + $50,000 Budget + Awareness Goal.
- **Reasoning**:
    - Layer 3C suggests PPC and SEO.
    - Layer 3D (Gen Z) promotes **Influencer Marketing** and **Social SMM** to Priority 2 (Layer 2).
    - Layer 3E (Gen Z + Retail) boosts **Content Marketing** (S5).
- **Output**: `['S3 - SMM', 'S9 - Influencers', 'S5 - Content']`

### Example 2: The Traditionalist Persona
- **Input**: B2C Retail + **Senior Audience** + $50,000 Budget + Awareness Goal.
- **Reasoning**:
    - Layer 3D (Senior) **inhibits** Social SMM to Priority 9 (Layer 2).
    - Layer 3D promotes **Email Marketing** (S4) and **Search SEO** (S1) to Priority 2.
    - Layer 11 (Long Horizon) confirms SEO as viable.
- **Output**: `['S1 - SEO', 'S4 - Email', 'S2 - PPC']`
