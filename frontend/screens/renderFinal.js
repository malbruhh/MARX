import { analysisResult, userInput } from '../store/state.js';

export function renderFinal() {
    // Show fact dropdown only on results
    const factDropdown = document.getElementById('fact-dropdown-container');
    if (factDropdown) factDropdown.classList.remove('hidden');
    console.log(analysisResult);
    const finalSection = document.getElementById('final-section');
    if (!finalSection || !analysisResult) return;

    // Calculate total months from overall budget
    const totalMonths = Math.round(Number(userInput.budget) / analysisResult.total_monthly_budget) || 0;

    finalSection.innerHTML = `
        <!-- Background Blobs -->
        <div class="spray-blob blob-md blob-1 opacity-30" style="top: -5%; left: -5%;"></div>
        <div class="spray-blob blob-md blob-2 opacity-30" style="bottom: -5%; right: -5%;"></div>
        <div class="spray-blob blob-sm blob-3 opacity-20" style="top: 15%; right: 5%;"></div>

        <div class="w-full max-w-6xl mx-auto py-24 px-8 relative z-10 animate-fadeIn">
            
            <div class="flex flex-col items-center mb-20 text-center">
                <h2 class="text-[10px] font-bold mb-4 text-blue-600 uppercase tracking-[0.6em] flex items-center gap-3">
                    <span class="w-8 h-[1px] bg-blue-600/30"></span>
                    Your Strategic Roadmap
                    <span class="w-8 h-[1px] bg-blue-600/30"></span>
                </h2>
                <h1 class="text-5xl md:text-7xl font-black text-white tracking-tighter uppercase leading-[0.9]">
                    Recommended<br><span class="text-transparent" style="-webkit-text-stroke: 1.5px rgba(255,255,255,0.8)">Strategies</span>
                </h1>
            </div>

            <!-- Critical Insights + Total Budget Row -->
            <div class="flex flex-col md:flex-row gap-6 mb-20 items-stretch">
                <!-- Critical Insights -->
                <div class="glass rounded-[2.5rem] p-10 flex-1 border border-white/20">
                    <h3 class="text-base font-bold text-blue-400 uppercase tracking-[0.4em] mb-6 decoration-blue-500/50 underline underline-offset-8">Critical Insights</h3>
                    <ul class="text-slate-900 space-y-4 text-base font-light">
                        ${analysisResult.critical_insights.map(insight => `
                            <li class="flex items-start gap-4">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-500 mt-2.5 shrink-0"></span>
                                <span>${insight}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                
                <!-- Total Budget (Refined) -->
                <div class="glass rounded-[2.5rem] p-6 w-full md:w-[240px] flex flex-col items-center justify-center text-center border border-white/20 hover:bg-white/5 transition-colors">
                    <div class="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center mb-5 border border-blue-500/30">
                        <i class="fas fa-wallet text-blue-400 text-xl"></i>
                    </div>
                    <h3 class="text-base font-bold text-slate-900 uppercase tracking-widest mb-1.5">Monthly Budget</h3>
                    <p class="text-3xl font-black text-white">$${analysisResult.total_monthly_budget}</p>
                    <div class="mt-5 px-3 py-1.5 bg-white/10 rounded-full border border-white/10">
                        <span class="text-blue-400 font-bold text-base">${totalMonths}</span>
                        <span class="text-slate-900 text-base font-bold uppercase tracking-widest ml-1">Months</span>
                    </div>
                </div>
            </div>

            <!-- Recommended Channels -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
                ${analysisResult.strategies.map((strat, index) => renderStrategyCard(strat, index)).join('')}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
                <!-- Action Plan -->
                <div class="glass rounded-[2.5rem] p-10 border border-white/20">
                    <h3 class="text-2xl font-black text-white mb-8 tracking-tight uppercase">Action Plan</h3>
                    <ul class="flex flex-col gap-3">
                        ${analysisResult.action_plan.map(item => renderActionPlanItem(item)).join('')}
                    </ul>
                </div>

                <!-- Resources -->
                <div class="glass rounded-[2.5rem] p-10 border border-white/20">
                    <h3 class="text-2xl font-black text-white mb-8 tracking-tight uppercase">Resources</h3>
                    <ul class="flex flex-col gap-3 text-slate-900">
                        ${analysisResult.resources.map(item => renderResourceItem(item)).join('')}
                    </ul>
                </div>
            </div>

        </div>
    `;
}

/**
 * Modernist Strategy Card
 */
function renderStrategyCard(strat, index) {
    const priorityConfigs = {
        'High': { 
            glow: '0 0 30px rgba(239, 68, 68, 0.25)', 
            border: 'border-red-500/30',
            inner: 'group-hover:text-red-400'
        },
        'Medium': { 
            glow: '0 0 30px rgba(245, 158, 11, 0.25)', 
            border: 'border-amber-500/30',
            inner: 'group-hover:text-amber-400'
        },
        'Low': { 
            glow: '0 0 30px rgba(59, 130, 246, 0.25)', 
            border: 'border-blue-500/30',
            inner: 'group-hover:text-blue-400'
        }
    };
    
    const config = priorityConfigs[strat.priority] || priorityConfigs['Low'];

    return `
        <div class="group relative flex flex-col h-full bg-white/[0.03] backdrop-blur-3xl rounded-[2rem] overflow-hidden border border-white/10 transition-all duration-500 hover:bg-white/[0.08] hover:${config.border} hover:-translate-y-2" style="box-shadow: ${config.glow}">
            <!-- Header with integrated Priority -->
            <div class="p-6 pb-4">
                <div class="flex justify-between items-start mb-5">
                    <span class="text-base font-black uppercase tracking-[0.2em] px-2.5 py-0.5 bg-white/10 rounded-full text-slate-900 border border-white/5">
                        ${strat.priority} Priority
                    </span>
                    <div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-slate-900">
                        <i class="fas fa-arrow-up-right-from-square text-[10px]"></i>
                    </div>
                </div>
                <h4 class="text-2xl font-black text-white leading-tight uppercase mb-3 ${config.inner} transition-colors break-words">
                    ${strat.title}
                </h4>
            </div>

            <!-- Tactic Content -->
            <div class="px-6 flex-1">
                <div class="h-[1px] w-full bg-gradient-to-right from-white/20 to-transparent mb-5"></div>
                <p class="text-slate-900 text-base font-light leading-relaxed mb-6 italic">
                    "${strat.tactic}"
                </p>
                <div class="flex items-center gap-2 mb-6 ${config.inner}">
                    <i class="fas fa-bullseye text-[10px]"></i>
                    <span class="text-base font-bold uppercase tracking-wider">${strat.expected_outcome}</span>
                </div>
            </div>

            <!-- Footer Stats -->
            <div class="p-6 pt-0 mt-auto">
                <div class="flex items-end justify-between bg-white/5 rounded-[1.5rem] p-5 border border-white/5 group-hover:bg-blue-600/10 group-hover:border-blue-500/20 transition-all">
                    <div>
                        <p class="text-base font-bold text-slate-900 uppercase tracking-widest mb-1">Allocation</p>
                        <p class="text-2xl font-black text-white leading-none">${strat.percentage}<span class="text-base opacity-40 ml-0.5">%</span></p>
                    </div>
                    <div class="text-right">
                        <p class="text-base font-bold text-slate-900 tracking-tight">$${strat.monthly_amount}<span class="text-base text-slate-900 ml-1">/mo</span></p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Icons with consistent mapping
 */
function renderActionPlanItem(item) {
    const iconMap = {
        'Quick Win': { icon: 'fa-bolt-lightning', color: 'text-amber-400', bg: 'bg-amber-400/10' },
        'KPI': { icon: 'fa-chart-column', color: 'text-blue-400', bg: 'bg-blue-400/10' },
        'Risk': { icon: 'fa-shield-halved', color: 'text-red-400', bg: 'bg-red-400/10' },
        'Scaling': { icon: 'fa-arrow-trend-up', color: 'text-green-400', bg: 'bg-green-400/10' }
    };

    const prefixMatch = item.match(/^\[(Quick Win(?:\s*-\s*\w+)?|KPI|Risk|Scaling|Priority \w+)\]\s*/i);
    let content = item;
    let iconData = { icon: 'fa-check', color: 'text-blue-400', bg: 'bg-blue-400/10' };

    if (prefixMatch) {
        const fullPrefix = prefixMatch[1];
        const basePrefix = fullPrefix.split('-')[0].trim();
        content = item.replace(prefixMatch[0], '');
        iconData = iconMap[basePrefix] || iconData;
    }

    return `
        <li class="flex items-center gap-4 p-3.5 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-colors">
            <div class="w-9 h-9 rounded-lg ${iconData.bg} flex items-center justify-center ${iconData.color} shrink-0">
                <i class="fas ${iconData.icon} text-sm"></i>
            </div>
            <span class="text-slate-900 font-light text-base tracking-wide leading-relaxed">${content}</span>
        </li>
    `;
}

function renderResourceItem(item) {
    const iconMap = {
        'Tool': { icon: 'fa-screwdriver-wrench', color: 'text-cyan-400', bg: 'bg-cyan-400/10' },
        'Capability': { icon: 'fa-brain', color: 'text-purple-400', bg: 'bg-purple-400/10' },
        'Partner': { icon: 'fa-handshake', color: 'text-pink-400', bg: 'bg-pink-400/10' },
        'Cost Tip': { icon: 'fa-piggy-bank', color: 'text-green-400', bg: 'bg-green-400/10' }
    };

    const prefixMatch = item.match(/^\[(Tool|Capability(?:\s*-\s*\w+)?|Partner|Cost Tip)\]\s*/i);
    let content = item;
    let iconData = { icon: 'fa-paperclip', color: 'text-blue-400', bg: 'bg-blue-400/10' };

    if (prefixMatch) {
        const fullPrefix = prefixMatch[1];
        const basePrefix = fullPrefix.split('-')[0].trim();
        content = item.replace(prefixMatch[0], '');
        iconData = iconMap[basePrefix] || iconData;
    }

    return `
        <li class="flex items-center gap-4 p-3.5 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-colors">
            <div class="w-9 h-9 rounded-lg ${iconData.bg} flex items-center justify-center ${iconData.color} shrink-0">
                <i class="fas ${iconData.icon} text-sm"></i>
            </div>
            <span class="text-slate-900 font-light text-base tracking-wide leading-relaxed">${content}</span>
        </li>
    `;
}

