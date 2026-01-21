import httpx
import asyncio
import json
import time

# Sample requests for different budget tiers
MICRO_BUDGET_REQUEST = {
    "product_type": "local_service",
    "raw_budget_amount": 500,
    "target_customer": "local_community",
    "primary_goal": "immediate_lead_generation",
    "time_horizon": "short_term",
    "content_capability": "low_capability",
    "sales_structure": "owner_driven",
    "priority_kpi": "conversion_rate"
}

ENTERPRISE_BUDGET_REQUEST = {
    "product_type": "b2b_enterprise_saas",
    "raw_budget_amount": 1500000,
    "target_customer": "large_enterprise",
    "primary_goal": "brand_awareness",
    "time_horizon": "long_term",
    "content_capability": "high_capability",
    "sales_structure": "dedicated_sales_team",
    "priority_kpi": "sales_qualified_leads"
}

BASE_URL = "http://127.0.0.1:8000"

async def test_endpoint(payload, description):
    print(f"\n--- Testing Scenario: {description} ---")
    async with httpx.AsyncClient() as client:
        try:
            start_time = time.time()
            response = await client.post(f"{BASE_URL}/api/analyze", json=payload, timeout=30.0)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"Status: Success (Take {duration:.2f}s)")
                print(f"Recommended Strategies: {data['data']['recommended_strategies']}")
                print(f"Critical Insights: {len(data['data']['critical_insights'])} items")
                print(f"Total Monthly Budget: ${data['data']['total_monthly_budget']:,}")
            else:
                print(f"Status: FAILED ({response.status_code})")
                print(response.text)
        except Exception as e:
            print(f"Error connecting to server: {e}")

async def main():
    print("Starting KBS Logic Verification...")
    # These tests assume the server is already running
    await test_endpoint(MICRO_BUDGET_REQUEST, "Micro Budget - Local Service")
    await test_endpoint(ENTERPRISE_BUDGET_REQUEST, "Enterprise Budget - B2B SaaS")

if __name__ == "__main__":
    asyncio.run(main())
