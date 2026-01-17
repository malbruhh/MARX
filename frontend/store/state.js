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