// ============================================
// MARX: Marketing Expert Analysis
// Vue.js Application
// ============================================

const { createApp } = Vue;

createApp({
    data() {
        return {
            // Current step for progress bar highlighting
            currentStep: 1,
            
            // Hero title scale (for shrinking animation)
            heroScale: 1,
            
            // Steps array for progress bar
            steps: [
                { id: 'budget', label: 'Budget' },
                { id: 'product', label: 'Product Type' },
                { id: 'customer', label: 'Target Customer' },
                { id: 'goal', label: 'Primary Goal' },
                { id: 'time', label: 'Time Horizon' },
                { id: 'content', label: 'Content Capability' },
                { id: 'sales', label: 'Sales Structure' },
                { id: 'kpi', label: 'Priority KPI' },
                { id: 'summary', label: 'Summary' }
            ],
            
            // Pagination for categories with 6+ items
            currentProductPage: 0,
            currentCustomerPage: 0,
            
            // Loading state for strategize button
            isLoading: false,
            
            // Show output section flag
            showOutput: false,
            
            // Form data - stores all user inputs
            formData: {
                budget: '',
                product: '',
                customer: '',
                goal: '',
                time: '',
                content: '',
                sales: '',
                kpi: ''
            },
            
            // Output data from backend API
            outputData: {
                recommended_strategies: [],
                critical_insights: [],
                budget_allocation: [],
                total_monthly_budget: 0,
                channel_tactics: []
            },
            
            // ============================================
            // PRODUCT TYPE OPTIONS
            // ============================================
            products: [
                { 
                    value: 'b2b_enterprise_saas', 
                    label: 'B2B Enterprise SaaS', 
                    icon: '💼', 
                    description: 'Enterprise software solutions for businesses' 
                },
                { 
                    value: 'b2c_retail_goods', 
                    label: 'B2C Retail Goods', 
                    icon: '🛍️', 
                    description: 'Consumer products and retail items' 
                },
                { 
                    value: 'local_service', 
                    label: 'Local Service', 
                    icon: '🏪', 
                    description: 'Community-based service businesses' 
                },
                { 
                    value: 'high_end_consulting', 
                    label: 'High-End Consulting', 
                    icon: '🎓', 
                    description: 'Premium consulting services' 
                },
                { 
                    value: 'digital_info_product', 
                    label: 'Digital Info Product', 
                    icon: '📱', 
                    description: 'Online courses and digital content' 
                },
                { 
                    value: 'fast_moving_consumer_goods', 
                    label: 'FMCG', 
                    icon: '🥤', 
                    description: 'Fast-moving consumer goods' 
                },
                { 
                    value: 'niche_technical_tools', 
                    label: 'Technical Tools', 
                    icon: '🔧', 
                    description: 'Specialized technical equipment' 
                },
                { 
                    value: 'hospitality', 
                    label: 'Hospitality', 
                    icon: '🏨', 
                    description: 'Hotels, restaurants, tourism' 
                },
                { 
                    value: 'subscription_recurring', 
                    label: 'Subscription Service', 
                    icon: '🔄', 
                    description: 'Recurring subscription models' 
                }
            ],
            
            // ============================================
            // TARGET CUSTOMER OPTIONS
            // ============================================
            customers: [
                { 
                    value: 'large_enterprise', 
                    label: 'Large Enterprise', 
                    icon: '🏢', 
                    description: 'Fortune 500 companies' 
                },
                { 
                    value: 'small_to_medium_enterprise', 
                    label: 'SME', 
                    icon: '🏪', 
                    description: 'Small to medium businesses' 
                },
                { 
                    value: 'gen_z', 
                    label: 'Gen Z', 
                    icon: '👾', 
                    description: 'Born 1997-2012, digital natives' 
                },
                { 
                    value: 'millenial', 
                    label: 'Millennial', 
                    icon: '💻', 
                    description: 'Born 1981-1996, tech-savvy' 
                },
                { 
                    value: 'senior', 
                    label: 'Senior', 
                    icon: '👴', 
                    description: 'Age 65+, experienced consumers' 
                },
                { 
                    value: 'local_community', 
                    label: 'Local Community', 
                    icon: '🏘️', 
                    description: 'Neighborhood-based customers' 
                },
                { 
                    value: 'niche_industry', 
                    label: 'Niche Industry', 
                    icon: '🎯', 
                    description: 'Specialized industry professionals' 
                },
                { 
                    value: 'budget_shopper', 
                    label: 'Budget Shopper', 
                    icon: '💰', 
                    description: 'Price-conscious consumers' 
                },
                { 
                    value: 'luxury', 
                    label: 'Luxury', 
                    icon: '💎', 
                    description: 'High-end, premium buyers' 
                }
            ],
            
            // ============================================
            // PRIMARY GOAL OPTIONS
            // ============================================
            goals: [
                { 
                    value: 'brand_awareness', 
                    label: 'Brand Awareness', 
                    icon: '📢', 
                    description: 'Build recognition and visibility' 
                },
                { 
                    value: 'immediate_lead_generation', 
                    label: 'Lead Generation', 
                    icon: '🎯', 
                    description: 'Generate qualified leads quickly' 
                },
                { 
                    value: 'customer_retention_loyalty', 
                    label: 'Customer Retention', 
                    icon: '❤️', 
                    description: 'Keep existing customers engaged' 
                }
            ],
            
            // ============================================
            // TIME HORIZON OPTIONS
            // ============================================
            timeHorizons: [
                { 
                    value: 'short_term', 
                    label: 'Short Term', 
                    icon: '⚡', 
                    description: '1-3 months campaign' 
                },
                { 
                    value: 'medium_term', 
                    label: 'Medium Term', 
                    icon: '📅', 
                    description: '3-6 months strategy' 
                },
                { 
                    value: 'long_term', 
                    label: 'Long Term', 
                    icon: '🎯', 
                    description: '6+ months investment' 
                }
            ],
            
            // ============================================
            // CONTENT CAPABILITY OPTIONS
            // ============================================
            contentCapabilities: [
                { 
                    value: 'high_capability', 
                    label: 'High Capability', 
                    icon: '🚀', 
                    description: 'Strong content production team' 
                },
                { 
                    value: 'medium_capability', 
                    label: 'Medium Capability', 
                    icon: '✅', 
                    description: 'Moderate content resources' 
                },
                { 
                    value: 'low_capability', 
                    label: 'Low Capability', 
                    icon: '📝', 
                    description: 'Limited content capacity' 
                }
            ],
            
            // ============================================
            // SALES STRUCTURE OPTIONS
            // ============================================
            salesStructures: [
                { 
                    value: 'automated_ecommerce', 
                    label: 'Automated E-commerce', 
                    icon: '🛒', 
                    description: 'Online automated sales' 
                },
                { 
                    value: 'dedicated_sales_team', 
                    label: 'Sales Team', 
                    icon: '👥', 
                    description: 'Dedicated sales professionals' 
                },
                { 
                    value: 'owner_driven', 
                    label: 'Owner Driven', 
                    icon: '👤', 
                    description: 'Owner handles sales directly' 
                }
            ],
            
            // ============================================
            // PRIORITY KPI OPTIONS
            // ============================================
            kpis: [
                { 
                    value: 'conversion_rate', 
                    label: 'Conversion Rate', 
                    icon: '📈', 
                    description: 'Optimize visitor-to-customer conversion' 
                },
                { 
                    value: 'customer_lifetime_value', 
                    label: 'Customer LTV', 
                    icon: '💰', 
                    description: 'Maximize long-term customer value' 
                },
                { 
                    value: 'organic_traffic_impressions', 
                    label: 'Organic Traffic', 
                    icon: '🌐', 
                    description: 'Grow organic reach and visibility' 
                },
                { 
                    value: 'cost_per_acquisition', 
                    label: 'Cost per Acquisition', 
                    icon: '💵', 
                    description: 'Minimize customer acquisition cost' 
                },
                { 
                    value: 'sales_qualified_leads', 
                    label: 'Sales Qualified Leads', 
                    icon: '🎯', 
                    description: 'Generate high-quality sales leads' 
                }
            ]
        };
    },
    
    // ============================================
    // COMPUTED PROPERTIES
    // ============================================
    computed: {
        // Split products into pages of 6 items each
        productPages() {
            const pages = [];
            for (let i = 0; i < this.products.length; i += 6) {
                pages.push(this.products.slice(i, i + 6));
            }
            return pages;
        },
        
        // Split customers into pages of 6 items each
        customerPages() {
            const pages = [];
            for (let i = 0; i < this.customers.length; i += 6) {
                pages.push(this.customers.slice(i, i + 6));
            }
            return pages;
        },
        
        // Format budget for display (remove non-numeric characters except decimal point)
        formattedBudget() {
            return this.formData.budget.replace(/[^0-9.]/g, '');
        },
        
        // Sort channels by priority (High, Medium, Low)
        sortedChannels() {
            const order = { 'High': 0, 'Medium': 1, 'Low': 2 };
            return [...this.outputData.channel_tactics].sort((a, b) => {
                return (order[a.priority] ?? 3) - (order[b.priority] ?? 3);
            });
        }
    },
    
    // ============================================
    // LIFECYCLE HOOKS
    // ============================================
    mounted() {
        // Set up scroll event listener for navbar and hero title animation
        window.addEventListener('scroll', this.handleScroll);
        
        // Set up Intersection Observer for progress bar highlighting
        this.setupCheckpointObserver();
    },
    
    beforeUnmount() {
        // Clean up event listener
        window.removeEventListener('scroll', this.handleScroll);
    },
    
    // ============================================
    // METHODS
    // ============================================
    methods: {
        /**
         * Handle scroll events
         * - Updates navbar appearance
         * - Shrinks hero MARX title as user scrolls
         */
        handleScroll() {
            const navbar = document.getElementById('navbar');
            const scrollY = window.scrollY;
            
            // Add 'scrolled' class to navbar after scrolling past 100px
            if (scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Shrink hero title as user scrolls
            const hero = document.querySelector('.hero-marx');
            if (hero) {
                // Calculate scale based on scroll position
                // Title shrinks from 1.0 to 0.3 as user scrolls from 0 to 600px
                const scale = Math.max(0.3, 1 - scrollY / 600);
                this.heroScale = scale;
            }
        },
        
        /**
         * Set up Intersection Observer to track which section is in view
         * Updates progress bar highlighting based on current section
         */
        setupCheckpointObserver() {
            const sections = document.querySelectorAll('section[id]');
            
            // Create a map of section IDs to step numbers
            const sectionMap = {};
            this.steps.forEach((step, index) => {
                sectionMap[step.id] = index + 1;
            });
            
            // Create Intersection Observer
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    // When section is 30% visible, update current step
                    if (entry.isIntersecting && entry.intersectionRatio > 0.3) {
                        const sectionId = entry.target.id;
                        if (sectionMap[sectionId]) {
                            this.currentStep = sectionMap[sectionId];
                        }
                    }
                });
            }, {
                threshold: [0.3],
                rootMargin: '-100px 0px -100px 0px'
            });
            
            // Observe all sections
            sections.forEach(section => observer.observe(section));
        },
        
        /**
         * Smooth scroll to a section by ID
         * @param {string} sectionId - The ID of the section to scroll to
         */
        scrollToSection(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
        },
        
        /**
         * Determine CSS class for progress bar checkpoint
         * @param {number} index - The step index (1-based)
         * @returns {string} CSS class name
         */
        checkpointClass(index) {
            if (index < this.currentStep) {
                return 'visited'; // Already visited (darker)
            } else if (index === this.currentStep) {
                return 'active'; // Current step (highlighted)
            } else {
                return 'upcoming'; // Not yet visited (brighter)
            }
        },
        
        /**
         * Get label for fact category based on count
         * @param {number} count - Number of facts in category
         * @returns {string} Label text
         */
        factCategoryLabel(count) {
            if (count >= 6) return '6+ Facts Category';
            if (count === 5) return '5 Facts Category';
            if (count === 3) return '3 Facts Category';
            return `${count} Facts`;
        },
        
        /**
         * Format budget input - only allow numbers and one decimal point
         * Automatically shows $ sign when user starts typing
         */
        formatBudget(event) {
            let value = event.target.value.replace(/[^0-9.]/g, '');
            
            // Ensure only one decimal point
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            
            this.formData.budget = value;
        },
        
        /**
         * Get grid class based on number of items
         * Used for responsive layout (3, 5, or 6+ items)
         * @param {number} count - Number of items
         * @returns {string} Tailwind CSS grid classes
         */
        getGridClass(count) {
            if (count === 3) {
                return 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';
            } else if (count === 5) {
                return 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';
            } else {
                // 6+ items: 2 columns on mobile, 3 on desktop
                return 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4';
            }
        },
        
        /**
         * Handle category option selection
         * @param {string} field - Form field name (product, customer, etc.)
         * @param {string} value - Selected option value
         */
        selectOption(field, value) {
            this.formData[field] = value;
            
            // Auto-scroll to next section after selection (with delay for smooth UX)
            setTimeout(() => {
                const sectionOrder = ['product', 'customer', 'goal', 'time', 'content', 'sales', 'kpi'];
                const currentIndex = sectionOrder.indexOf(field);
                
                if (currentIndex >= 0 && currentIndex < sectionOrder.length - 1) {
                    // Scroll to next section
                    const nextSection = sectionOrder[currentIndex + 1];
                    this.scrollToSection(nextSection);
                } else if (field === 'kpi') {
                    // If last section, scroll to summary
                    this.scrollToSection('summary');
                }
            }, 300);
        },
        
        /**
         * Get icon for selected option
         * @param {string} field - Form field name
         * @returns {string} Icon emoji or '❓' if not selected
         */
        getIconForSelection(field) {
            const value = this.formData[field];
            if (!value) return '❓';
            
            // Get the appropriate options array
            let options = [];
            switch(field) {
                case 'product': options = this.products; break;
                case 'customer': options = this.customers; break;
                case 'goal': options = this.goals; break;
                case 'time': options = this.timeHorizons; break;
                case 'content': options = this.contentCapabilities; break;
                case 'sales': options = this.salesStructures; break;
                case 'kpi': options = this.kpis; break;
            }
            
            // Find and return the icon
            const item = options.find(opt => opt.value === value);
            return item ? item.icon : '❓';
        },
        
        /**
         * Get label for selected option
         * @param {string} field - Form field name
         * @returns {string} Label text or 'Not selected'
         */
        getLabelForSelection(field) {
            const value = this.formData[field];
            if (!value) return 'Not selected';
            
            // Get the appropriate options array
            let options = [];
            switch(field) {
                case 'product': options = this.products; break;
                case 'customer': options = this.customers; break;
                case 'goal': options = this.goals; break;
                case 'time': options = this.timeHorizons; break;
                case 'content': options = this.contentCapabilities; break;
                case 'sales': options = this.salesStructures; break;
                case 'kpi': options = this.kpis; break;
            }
            
            // Find and return the label
            const item = options.find(opt => opt.value === value);
            return item ? item.label : 'Not selected';
        },
        
        /**
         * Get budget percentage for a strategy
         * @param {string} strategyCode - Strategy code
         * @returns {string} Percentage as string
         */
        getBudgetPercentage(strategyCode) {
            const allocation = this.outputData.budget_allocation.find(
                item => item.strategy_code === strategyCode
            );
            return allocation ? allocation.percentage.toFixed(0) : '0';
        },
        
        /**
         * Get budget amount for a strategy
         * @param {string} strategyCode - Strategy code
         * @returns {number} Monthly amount
         */
        getBudgetAmount(strategyCode) {
            const allocation = this.outputData.budget_allocation.find(
                item => item.strategy_code === strategyCode
            );
            return allocation ? allocation.monthly_amount : 0;
        },
        
        /**
         * Main function to send data to backend and get recommendations
         * Validates form, sends API request, displays results
         */
        async strategize() {
            // Validate all fields are filled
            if (!this.formData.budget || 
                !this.formData.product || 
                !this.formData.customer || 
                !this.formData.goal || 
                !this.formData.time || 
                !this.formData.content || 
                !this.formData.sales || 
                !this.formData.kpi) {
                alert('Please complete all fields before strategizing!');
                return;
            }
            
            // Set loading state
            this.isLoading = true;
            
            try {
                // Parse budget value
                const budgetValue = parseFloat(this.formData.budget.replace(/[^0-9.]/g, ''));
                
                // Determine budget level based on amount
                let budgetLevel = 'medium';
                if (budgetValue < 1000) budgetLevel = 'micro';
                else if (budgetValue < 10000) budgetLevel = 'low';
                else if (budgetValue < 100000) budgetLevel = 'medium';
                else if (budgetValue < 1000000) budgetLevel = 'high';
                else budgetLevel = 'enterprise';
                
                // Prepare payload for API request
                const payload = {
                    product_type: this.formData.product,
                    target_customer: this.formData.customer,
                    budget: budgetValue,
                    budget_level: budgetLevel,
                    primary_goal: this.formData.goal,
                    time_horizon: this.formData.time,
                    content_capability: this.formData.content,
                    sales_structure: this.formData.sales,
                    priority_kpi: this.formData.kpi
                };
                
                // ============================================
                // API REQUEST
                // Backend endpoint: http://localhost:8000/api/analyze
                // ============================================
                const apiUrl = 'http://localhost:8000/api/analyze';
                
                // Make API request
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                
                // Check if request was successful
                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }
                
                // Parse response
                const data = await response.json();
                
                // Store output data
                this.outputData = {
                    recommended_strategies: data.recommended_strategies || [],
                    critical_insights: data.critical_insights || [],
                    budget_allocation: data.budget_allocation || [],
                    total_monthly_budget: data.total_monthly_budget || 0,
                    channel_tactics: data.channel_tactics || []
                };
                
                // Show output section
                this.showOutput = true;
                
                // Scroll to output section after a short delay
                this.$nextTick(() => {
                    setTimeout(() => {
                        this.scrollToSection('output');
                    }, 300);
                });
                
            } catch (error) {
                console.error('Error strategizing:', error);
                
                // For development: Use mock data if API fails
                // Remove this in production!
                console.warn('API request failed, using mock data for demonstration');
                const budgetValue = parseFloat(this.formData.budget.replace(/[^0-9.]/g, ''));
                this.useMockData(budgetValue);
                this.showOutput = true;
                
                this.$nextTick(() => {
                    setTimeout(() => {
                        this.scrollToSection('output');
                    }, 300);
                });
            } finally {
                // Reset loading state
                this.isLoading = false;
            }
        },
        
        /**
         * Mock data function for development/testing
         * Remove this in production!
         * @param {number} budgetValue - Budget amount
         */
        useMockData(budgetValue) {
            this.outputData = {
                recommended_strategies: [
                    "S7 - Account-Based Marketing (ABM)",
                    "S8 - Trade Shows/Conferences",
                    "S5 - Content Marketing"
                ],
                critical_insights: [
                    "Optimize for conversion - implement targeted campaigns with clear CTAs and lead capture mechanisms",
                    "Leverage multi-channel approach - diversify across paid and organic to maximize reach while maintaining efficiency",
                    "B2B buyers need education and trust - create case studies, whitepapers, and demonstrate ROI through content",
                    "Short timeline requires immediate action - prioritize paid channels and quick-win optimizations over long-term SEO",
                    "Maximize your content strength - produce authoritative resources that attract organic traffic and establish industry credibility"
                ],
                budget_allocation: [
                    {
                        strategy_code: "S7 - Account-Based Marketing (ABM)",
                        percentage: 25.0,
                        monthly_amount: budgetValue * 0.25
                    },
                    {
                        strategy_code: "S8 - Trade Shows/Conferences",
                        percentage: 40.0,
                        monthly_amount: budgetValue * 0.40
                    },
                    {
                        strategy_code: "S5 - Content Marketing",
                        percentage: 35.0,
                        monthly_amount: budgetValue * 0.35
                    }
                ],
                total_monthly_budget: budgetValue,
                channel_tactics: [
                    {
                        strategy_code: "S7 - Account-Based Marketing (ABM)",
                        tactic: "Identify top 20 target accounts and create personalized outreach campaigns",
                        priority: "High",
                        expected_outcome: "Increase enterprise deal closure rate by 40%"
                    },
                    {
                        strategy_code: "S8 - Trade Shows/Conferences",
                        tactic: "Attend industry conferences and host booth/speaking sessions",
                        priority: "High",
                        expected_outcome: "Generate 50-100 qualified leads per event"
                    },
                    {
                        strategy_code: "S5 - Content Marketing",
                        tactic: "Create value-driven content (blogs, videos, guides) addressing customer pain points",
                        priority: "Medium",
                        expected_outcome: "Establish thought leadership and generate inbound leads"
                    }
                ]
            };
        }
    }
}).mount('#app');
