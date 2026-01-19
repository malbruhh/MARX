// /frontend/screens/renderFinal.js
import { analysisResult, userInput } from '../store/state.js';

export function renderFinal() {
    console.log(analysisResult);
    const finalSection = document.getElementById('final-section');
    if (!finalSection || !analysisResult) return;

    // Calculate total months from overall budget
    const totalMonths = Math.round(Number(userInput.budget) / analysisResult.total_monthly_budget) || 0;

    finalSection.innerHTML = `
        <div class="w-full max-w-6xl mx-auto py-20 px-6 animate-fadeIn">

            <!-- Title -->
            <h2 class="text-5xl md:text-6xl font-extrabold text-white text-center mb-12 tracking-tight">
                Our Recommended Strategies
            </h2>

            <!-- Critical Insights + Total Budget Row -->
            <div class="flex flex-col md:flex-row gap-6 mb-16 items-stretch">
                <!-- Critical Insights (Larger) -->
                <div class="glass rounded-[2rem] p-8 flex-1">
                    <h3 class="text-2xl font-bold text-white mb-5 text-center">Critical Insights</h3>
                    <ul class="text-white/90 space-y-2 text-base font-light list-disc list-inside">
                        ${analysisResult.critical_insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
                <!-- Total Budget (Smaller) -->
                <div class="glass rounded-[2rem] p-8 w-full md:w-[220px] flex flex-col items-center justify-center text-center">
                    <h3 class="text-xl font-bold text-white mb-3">Total Budget</h3>
                    <p class="text-3xl font-extrabold text-white">$${analysisResult.total_monthly_budget} USD/mo</p>
                    <p class="text-sm text-white/70 mt-2">${totalMonths} Months</p>
                </div>
            </div>

            <!-- Recommended Channels -->
            <h3 class="text-3xl md:text-4xl font-bold text-white text-center mb-10">Recommended Channels</h3>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-start mb-16">
                ${analysisResult.strategies.map((strat, index) => renderStrategyCard(strat, index)).join('')}
            </div>

            <!-- Action Plan Section -->
            <div class="glass rounded-[2rem] p-8 mb-8">
                <h3 class="text-2xl font-bold text-white mb-6 text-center">Action Plan</h3>
                <ul class="grid md:grid-cols-2 gap-3 text-white/90 text-base">
                    ${analysisResult.action_plan.map(item => renderActionPlanItem(item)).join('')}
                </ul>
            </div>

            <!-- Resources Section -->
            <div class="glass rounded-[2rem] p-8">
                <h3 class="text-2xl font-bold text-white mb-6 text-center">Resources</h3>
                <ul class="grid md:grid-cols-2 gap-3 text-white/90 text-base">
                    ${analysisResult.resources.map(item => renderResourceItem(item)).join('')}
                </ul>
            </div>

        </div>
    `;
}

/**
 * Renders a Strategy Card with priority-based colors
 */
function renderStrategyCard(strat, index) {
    const isMiddle = index === 1;

    // Priority-based glassmorphism colors
    const priorityStyles = {
        'High': {
            bg: 'bg-red-800/50 border-red-400/40',
            header: 'bg-red-900/60 border-red-400/30'
        },
        'Medium': {
            bg: 'bg-amber-700/50 border-amber-400/40',
            header: 'bg-amber-800/60 border-amber-400/30'
        },
        'Low': {
            bg: 'bg-slate-600/50 border-slate-400/40',
            header: 'bg-slate-700/60 border-slate-400/30'
        }
    };

    const style = priorityStyles[strat.priority] || priorityStyles['Medium'];
    const marginClass = isMiddle ? 'mt-0' : 'md:mt-14';

    return `
        <div class="flex flex-col gap-4 ${marginClass} transition-transform hover:scale-[1.02] duration-300">
            <!-- Strategy Title -->
            <div class="${style.header} backdrop-blur-md rounded-[1.5rem] p-5 text-center border">
                <h4 class="font-bold text-white text-base leading-tight uppercase tracking-wide">
                    ${strat.title}
                </h4>
            </div>

            <!-- Channel Tactics -->
            <div class="${style.bg} backdrop-blur-md rounded-[1.5rem] p-5 border">
                <h5 class="text-center font-bold text-white mb-4 text-base">Channel Tactics</h5>
                <ul class="text-sm text-white/90 space-y-2 list-disc list-inside font-light">
                    <li><strong class="text-white">Priority:</strong> ${strat.priority}</li>
                    <li><strong class="text-white">Tactic:</strong> ${strat.tactic}</li>
                    <li><strong class="text-white">Expected Outcome:</strong> ${strat.expected_outcome}</li>
                </ul>
            </div>

            <!-- Budget Allocation -->
            <div class="${style.bg} backdrop-blur-md rounded-[1.5rem] p-4 border">
                <h5 class="text-center font-bold text-white mb-3 text-base">Budget Allocation</h5>
                <div class="flex gap-3">
                    <div class="bg-black/30 backdrop-blur-sm rounded-xl flex-1 py-3 text-center">
                        <span class="block text-xl font-bold text-white">${strat.percentage}%</span>
                    </div>
                    <div class="bg-black/30 backdrop-blur-sm rounded-xl flex-[2] py-3 text-center">
                        <span class="block text-base font-bold text-white">$${strat.monthly_amount} / mo</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Renders an Action Plan item with appropriate icon based on prefix
 */
function renderActionPlanItem(item) {
    const iconMap = {
        'Quick Win': { icon: 'fa-bolt', color: 'text-yellow-400' },
        'KPI': { icon: 'fa-chart-line', color: 'text-blue-400' },
        'Risk': { icon: 'fa-triangle-exclamation', color: 'text-red-400' },
        'Scaling': { icon: 'fa-arrow-trend-up', color: 'text-green-400' }
    };

    // Parse prefix pattern: [Quick Win - High], [KPI], [Risk], [Scaling]
    const prefixMatch = item.match(/^\[(Quick Win(?:\s*-\s*\w+)?|KPI|Risk|Scaling)\]\s*/i);

    if (prefixMatch) {
        const fullPrefix = prefixMatch[1];
        const basePrefix = fullPrefix.split('-')[0].trim();
        const content = item.replace(prefixMatch[0], '');
        const iconData = iconMap[basePrefix] || { icon: 'fa-circle', color: 'text-white/60' };

        // For Quick Win, show priority color
        let finalColor = iconData.color;
        if (basePrefix === 'Quick Win') {
            const priorityMatch = fullPrefix.match(/High|Medium|Low/i);
            if (priorityMatch) {
                const priority = priorityMatch[0].toLowerCase();
                if (priority === 'high') finalColor = 'text-red-400';
                else if (priority === 'medium') finalColor = 'text-amber-400';
                else finalColor = 'text-slate-400';
            }
        }

        return `
            <li class="flex items-start gap-3 bg-white/5 rounded-xl p-3">
                <i class="fas ${iconData.icon} ${finalColor} mt-0.5"></i>
                <span class="font-light">${content}</span>
            </li>
        `;
    }

    // Fallback for items without recognized prefix
    return `
        <li class="flex items-start gap-3 bg-white/5 rounded-xl p-3">
            <i class="fas fa-circle-dot text-white/40 mt-0.5"></i>
            <span class="font-light">${item}</span>
        </li>
    `;
}

/**
 * Renders a Resource item with appropriate icon based on prefix
 */
function renderResourceItem(item) {
    const iconMap = {
        'Tool': { icon: 'fa-wrench', color: 'text-cyan-400' },
        'Capability': { icon: 'fa-gear', color: 'text-purple-400' },
        'Partner': { icon: 'fa-handshake', color: 'text-pink-400' },
        'Cost Tip': { icon: 'fa-dollar-sign', color: 'text-green-400' }
    };

    // Parse prefix pattern: [Tool], [Capability - Critical], [Partner], [Cost Tip]
    const prefixMatch = item.match(/^\[(Tool|Capability(?:\s*-\s*\w+)?|Partner|Cost Tip)\]\s*/i);

    if (prefixMatch) {
        const fullPrefix = prefixMatch[1];
        const basePrefix = fullPrefix.split('-')[0].trim();
        const content = item.replace(prefixMatch[0], '');
        const iconData = iconMap[basePrefix] || { icon: 'fa-circle', color: 'text-white/60' };

        // For Capability, could adjust based on importance
        let finalColor = iconData.color;
        if (basePrefix === 'Capability') {
            const importanceMatch = fullPrefix.match(/Critical|High|Medium|Low/i);
            if (importanceMatch) {
                const importance = importanceMatch[0].toLowerCase();
                if (importance === 'critical' || importance === 'high') finalColor = 'text-red-400';
                else if (importance === 'medium') finalColor = 'text-amber-400';
                else finalColor = 'text-slate-400';
            }
        }

        return `
            <li class="flex items-start gap-3 bg-white/5 rounded-xl p-3">
                <i class="fas ${iconData.icon} ${finalColor} mt-0.5"></i>
                <span class="font-light">${content}</span>
            </li>
        `;
    }

    // Fallback
    return `
        <li class="flex items-start gap-3 bg-white/5 rounded-xl p-3">
            <i class="fas fa-circle-dot text-white/40 mt-0.5"></i>
            <span class="font-light">${item}</span>
        </li>
    `;
}

