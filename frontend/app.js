const { createApp, ref, onMounted, computed } = Vue;

createApp({
    setup() {
        const currentSection = ref(1);
        const loading = ref(false);
        const output = ref(null);

        const formData = ref({
            budget: null,
            productType: '',
            targetCustomer: '',
            primaryGoal: '',
            timeHorizon: '',
            contentCapability: '',
            salesStructure: '',
            priorityKPI: ''
        });

        const reviews = [
            { stars: 5 }, { stars: 5 }, { stars: 4 }
        ];

        const categories = ref([
            {
                title: 'Product Category',
                key: 'productType',
                description: 'Define the core nature of your offering to determine market fit.',
                page: 0,
                options: [
                    { label: 'B2B Enterprise SaaS', value: 'b2b_enterprise_saas', icon: 'layers', desc: 'Software for large organizations' },
                    { label: 'B2C Retail Goods', value: 'b2c_retail_goods', icon: 'shopping-bag', desc: 'Physical consumer products' },
                    { label: 'Local Service', value: 'local_service', icon: 'map-pin', desc: 'Geography-specific services' },
                    { label: 'High-end Consulting', value: 'high_end_consulting', icon: 'briefcase', desc: 'Professional expert services' },
                    { label: 'Digital Info Product', value: 'digital_info_product', icon: 'book-open', desc: 'Courses and digital media' },
                    { label: 'FMCG', value: 'fast_moving_consumer_goods', icon: 'zap', desc: 'Rapidly consumed goods' },
                    { label: 'Niche Tech Tools', value: 'niche_technical_tools', icon: 'cpu', desc: 'Specialized hardware or software' },
                    { label: 'Hospitality', value: 'hospitality', icon: 'coffee', desc: 'Food, drink, and lodging' }
                ]
            },
            {
                title: 'Target Audience',
                key: 'targetCustomer',
                description: 'Who are we aiming for? Messaging varies wildly by demographic.',
                page: 0,
                options: [
                    { label: 'Large Enterprise', value: 'large_enterprise', icon: 'building', desc: 'Fortune 500 level' },
                    { label: 'Gen Z', value: 'gen_z', icon: 'smartphone', desc: 'Digital natives' },
                    { label: 'Luxury Buyers', value: 'luxury', icon: 'gem', desc: 'High net worth individuals' },
                    { label: 'SMEs', value: 'small_to_medium_enterprise', icon: 'users', desc: 'Small business owners' },
                    { label: 'Local Community', value: 'local_community', icon: 'home', desc: 'Neighborhood focused' }
                ]
            },
            {
                title: 'Primary Goal',
                key: 'primaryGoal',
                description: 'Are we building a brand or hunting for immediate sales?',
                page: 0,
                options: [
                    { label: 'Brand Awareness', value: 'brand_awareness', icon: 'eye', desc: 'Get people to know you' },
                    { label: 'Lead Generation', value: 'immediate_lead_generation', icon: 'target', desc: 'Focus on direct inquiries' },
                    { label: 'Retention', value: 'customer_retention_loyalty', icon: 'heart', desc: 'Focus on existing clients' }
                ]
            }
        ]);

        const visibleOptions = (cat) => {
            if (cat.options.length <= 6) return cat.options;
            const start = cat.page * 6;
            return cat.options.slice(start, start + 6);
        };

        const selectOption = (key, val) => {
            formData.value[key] = val;
        };

        const strategize = async () => {
            loading.value = true;
            // Simulate API Call
            setTimeout(() => {
                output.value = {
                    "recommended_strategies": ["S7 - Account-Based Marketing", "S8 - Trade Shows", "S5 - Content Marketing"],
                    "critical_insights": [
                        "Optimize for conversion - implement targeted campaigns with clear CTAs.",
                        "Leverage multi-channel approach - diversify across paid and organic.",
                        "B2B buyers need education - create case studies and whitepapers.",
                        "Short timeline requires immediate action - prioritize paid channels.",
                        "Maximize content strength - produce authoritative resources."
                    ],
                    "budget_allocation": [
                        { "strategy_code": "S7 - Account-Based Marketing", "percentage": 25.0, "monthly_amount": 4166.67 },
                        { "strategy_code": "S8 - Trade Shows", "percentage": 40.0, "monthly_amount": 6666.67 },
                        { "strategy_code": "S5 - Content Marketing", "percentage": 35.0, "monthly_amount": 5833.33 }
                    ],
                    "total_monthly_budget": 16666.67,
                    "channel_tactics": [
                        { "strategy_code": "S7 - Account-Based Marketing", "tactic": "Identify top 20 accounts", "priority": "High", "expected_outcome": "40% Increase in deals" },
                        { "strategy_code": "S8 - Trade Shows", "tactic": "Host booth at Industry X", "priority": "Medium", "expected_outcome": "100 Leads" },
                        { "strategy_code": "S5 - Content Marketing", "tactic": "Create ROI guides", "priority": "Low", "expected_outcome": "Inbound growth" }
                    ]
                };
                loading.value = false;
                
                // Scroll to output after a tick
                setTimeout(() => {
                    document.getElementById('output').scrollIntoView({ behavior: 'smooth' });
                }, 100);
            }, 2000);
        };

        const getPriorityClass = (p) => {
            if (p === 'High') return 'border-red-400/50';
            if (p === 'Medium') return 'border-yellow-400/50';
            return 'border-blue-400/50';
        };

        const getPriorityBg = (p) => {
            if (p === 'High') return 'bg-red-500/60';
            if (p === 'Medium') return 'bg-yellow-500/60';
            return 'bg-blue-500/60';
        };

        const getBudgetPerc = (code) => output.value.budget_allocation.find(b => b.strategy_code === code)?.percentage;
        const getBudgetAmt = (code) => output.value.budget_allocation.find(b => b.strategy_code === code)?.monthly_amount.toLocaleString();

        onMounted(() => {
            lucide.createIcons();
            
            // GSAP Scroll Animations
            gsap.registerPlugin(ScrollTrigger);

            // Title Shrinking Animation
            gsap.to("#main-title", {
                scrollTrigger: {
                    trigger: "#home",
                    start: "top top",
                    end: "500px",
                    scrub: true,
                },
                scale: 0.2,
                opacity: 0,
                y: -100
            });

            // Navbar Logo Reveal
            gsap.to("#nav-logo", {
                scrollTrigger: {
                    trigger: "#home",
                    start: "300px top",
                    scrub: true,
                },
                opacity: 1
            });

            // Section Checkpoint Logic
            const sections = document.querySelectorAll("section");
            window.addEventListener("scroll", () => {
                let current = "";
                sections.forEach((section, index) => {
                    const sectionTop = section.offsetTop;
                    if (pageYOffset >= sectionTop - 200) {
                        currentSection.value = index + 1;
                    }
                });
            });
        });

        return {
            formData, reviews, categories, visibleOptions, selectOption,
            currentSection, loading, strategize, output,
            getPriorityClass, getPriorityBg, getBudgetPerc, getBudgetAmt
        };
    }
}).mount('#app');