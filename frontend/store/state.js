// /frontend/store/state.js

export const userInput = {
    budget: "",
    product_type: null,
    target_customer: null,
    primary_goal: null,
    time_horizon: 'medium_term', 
    content_capability: 'medium_capability',
    sales_structure: null,
    priority_kpi: null
};

export const sectionToStateMap = {
    'card-1': 'budget',
    'card-2': 'product_type',
    'card-3': 'target_customer',
    'card-4': 'primary_goal',
    'card-5': 'time_horizon',
    'card-6': 'content_capability',
    'card-7': 'sales_structure',
    'card-8': 'priority_kpi'
};

/**
 * Updates a specific key in the userInput state.
 * @param {string} key - The state key to update.
 * @param {any} value - The value to save.
 */
export const saveState = (key, value) => {
    userInput[key] = value;
    // DEBUG LOGGING: Shows the updated state in a readable table
    // console.log(`%c [STATE UPDATE] ${key.toUpperCase()}: ${value}`, "color: #ff00ff; font-weight: bold;");
    // console.table(userInput);
};

//Output model
export const analysisResult = {
    status: null,
    strategies: [], // Array of objects with { id, title, percentage, monthly_amount, tactic, priority, outcome }
    critical_insights: [],
    action_plan: [],
    resources: [],
    total_monthly_budget: 0
};

export const saveAnalysisResult = (apiResponse) => {
    const { data } = apiResponse;
    
    analysisResult.status = apiResponse.status;
    analysisResult.critical_insights = data.critical_insights || [];
    analysisResult.action_plan = data.action_plan || [];
    analysisResult.resources = data.resources || [];
    analysisResult.total_monthly_budget = data.total_monthly_budget || 0;

    // Combine strategies into one data point using the S# as internal ID
    analysisResult.strategies = data.recommended_strategies.map(fullCode => {
        // Splitting "S1 - Search Engine Optimization (SEO)" 
        // id: "S1", title: "Search Engine Optimization (SEO)"
        const [id, ...titleParts] = fullCode.split(' - ');
        const title = titleParts.join(' - ');

        const allocation = data.budget_allocation.find(a => a.strategy_code === fullCode) || {};
        const tactics = data.channel_tactics.find(t => t.strategy_code === fullCode) || {};

        return {
            id: id, 
            title: title, // This is the "Description" you want to display
            percentage: allocation.percentage || 0,
            monthly_amount: allocation.monthly_amount || 0,
            tactic: tactics.tactic || "",
            priority: tactics.priority || "Medium",
            expected_outcome: tactics.expected_outcome || ""
        };
    });

    console.log("[STATE UPDATE] Processed AI Analysis Result:", analysisResult);
};