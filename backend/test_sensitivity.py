import requests
import json

def test_sensitivity():
    url = "http://127.0.0.1:8000/api/analyze"
    
    # Common base configuration
    base_payload = {
        "product_type": "b2c_retail_goods",
        "raw_budget_amount": 50000,
        "primary_goal": "brand_awareness",
        "time_horizon": "long_term",
        "content_capability": "medium_capability",
        "sales_structure": "automated_ecommerce",
        "priority_kpi": "conversion_rate"
    }

    # Case 1: Gen Z
    payload_gen_z = base_payload.copy()
    payload_gen_z["target_customer"] = "gen_z"
    
    # Case 2: Senior
    payload_senior = base_payload.copy()
    payload_senior["target_customer"] = "senior"

    print("\n--- TESTING SENSITIVITY: Gen Z vs Senior ---")
    
    try:
        resp_gen_z = requests.post(url, json=payload_gen_z)
        resp_senior = requests.post(url, json=payload_senior)
        
        print(f"Gen Z Response Code: {resp_gen_z.status_code}")
        print(f"Senior Response Code: {resp_senior.status_code}")

        if resp_gen_z.status_code != 200:
            print(f"Gen Z Error: {resp_gen_z.text}")
            return
        if resp_senior.status_code != 200:
            print(f"Senior Error: {resp_senior.text}")
            return

        res_gen_z = resp_gen_z.json()["data"]
        res_senior = resp_senior.json()["data"]
        
        strategies_gen_z = res_gen_z["recommended_strategies"]
        strategies_senior = res_senior["recommended_strategies"]
        
        print(f"\nGen Z Strategies:    {strategies_gen_z}")
        print(f"Senior Strategies:   {strategies_senior}")
        
        if set(strategies_gen_z) != set(strategies_senior):
            print("\n✅ SUCCESS: Strategies are distinct!")
            
            # Find common and unique
            common = set(strategies_gen_z).intersection(set(strategies_senior))
            unique_gen_z = set(strategies_gen_z) - common
            unique_senior = set(strategies_senior) - common
            
            print(f"Shared: {list(common)}")
            print(f"Unique to Gen Z:  {list(unique_gen_z)}")
            print(f"Unique to Senior: {list(unique_senior)}")
        else:
            print("\n❌ FAILURE: Strategies are identical. Sensitivity issues remain.")

        # Test Case 3: Micro Budget + Gen Z (Should trigger high-dimensional combination)
        print("\n--- TESTING SENSITIVITY: Micro Budget + Gen Z ---")
        payload_micro = payload_gen_z.copy()
        payload_micro["raw_budget_amount"] = 500
        
        resp_micro = requests.post(url, json=payload_micro)
        res_micro = resp_micro.json()["data"]
        strategies_micro = res_micro["recommended_strategies"]
        
        print(f"Micro Budget Gen Z Strategies: {strategies_micro}")
        if set(strategies_micro) != set(strategies_gen_z):
            print("✅ SUCCESS: Budget change triggered distinct strategy shift!")
        else:
            print("❌ FAILURE: Budget change did not shift strategy.")

    except Exception as e:
        print(f"Error connecting to server: {e}")
        print("Make sure the FastAPI server is running (python backend/app.py)")

if __name__ == "__main__":
    test_sensitivity()
