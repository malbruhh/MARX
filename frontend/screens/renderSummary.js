// /frontend/screens/renderSummary.js
import { userInput } from '../store/state.js';
import { productData, targetCustomerData, primaryGoalData, timeHorizonData, capabilityData, salesStructureData, kpiData } from '../components/inputData.js';
import { initializeAnalyzeBtn } from '../components/analyzeBtn.js';

const allData = [...productData, ...targetCustomerData, ...primaryGoalData, ...timeHorizonData, ...capabilityData, ...salesStructureData, ...kpiData];
let lastRenderedState = "";
export function renderSummary() {
    const container = document.getElementById('summary-section');
    if (!container) return;

    const currentStateString = JSON.stringify(userInput);
    if (currentStateString === lastRenderedState) return;
    
    // Filter used categories to find the labels/icons
    const getSelectionData = (key) => allData.find(item => item.id === userInput[key]);

    container.innerHTML = `
        <div class="flex flex-col items-center w-full max-w-3xl px-10">
            <h2 class="text-xs font-bold mb-4 text-blue-600 uppercase tracking-[0.4em] flex items-center gap-3">
                <span class="w-8 h-[2px] bg-blue-600"></span>
                Review Your Choices
                <span class="w-8 h-[2px] bg-blue-600"></span>
            </h2>
            <h2 class="text-7xl font-extrabold text-blue-900 my-2 tracking-tighter">SUMMARY</h2>
            <p class="text-2xl text-blue-500 font-light mb-8 italic">Plan Budget: <span class="font-bold">$${userInput.budget || '0'}</span></p>

            <!-- High-Contrast Centered Grid -->
            <div class="flex flex-wrap justify-center gap-4 md:gap-6 mb-4 w-full">
                ${['product_type', 'target_customer', 'primary_goal', 'time_horizon'].map(key => renderMiniCard(getSelectionData(key))).join('')}
            </div>

            <div class="flex flex-wrap justify-center gap-4 md:gap-6 mb-16 w-full">
                ${['content_capability', 'sales_structure', 'priority_kpi'].map(key => renderMiniCard(getSelectionData(key))).join('')}
            </div>

            <div class="flex flex-col md:flex-row gap-8 items-center">
                <button id="back-to-edit" class="glass px-10 py-5 rounded-full border-2 border-blue-200 text-blue-600 hover:bg-blue-50 transition-all text-sm uppercase font-bold tracking-widest flex items-center gap-3">
                    <i class="fas fa-pen-to-square"></i> Edit Selection
                </button>
                <button id="analyze-btn" class="px-10 py-5 rounded-[2.2rem] btn-primary text-lg font-bold tracking-[0.2em] uppercase shadow-2xl hover:shadow-blue-500/40 transform hover:-translate-y-1 active:scale-95 transition-all">
                    Analyze Strategy
                </button>
            </div>
        </div>
    `;
    document.getElementById('back-to-edit').addEventListener('click', () => {
        // 1. Restore the layout immediately
        document.getElementById('analysis-section').style.display = 'flex';
        document.getElementById('home').style.display = 'flex';
        const mainSection = document.querySelector('main');
        if (mainSection) mainSection.style.display = 'block';

        // 2. Hide the summary and bring back the navigation button
        container.classList.add('hidden');
        container.style.display = 'none';
        
        const nextBtn = document.getElementById('global-next-btn');
        if (nextBtn) {
            nextBtn.style.display = 'flex';
            // Force reset visibility properties so it doesn't flicker on home
            nextBtn.style.opacity = '1';
            nextBtn.style.pointerEvents = 'auto';
            nextBtn.style.transform = 'translateY(0)';
        }

        // 3. Scroll to Card 1 (or wherever you want them to start editing)
        // Using a slight timeout ensures the browser has finished the 'display: block' layout
        setTimeout(() => {
            scrollToSection('card-1'); 
        }, 50);
    });
    lastRenderedState = currentStateString;
    console.log("[UI] Summary dynamically updated via scroll.");
    console.log(userInput);


    initializeAnalyzeBtn('analyze-btn');
}

function renderMiniCard(data) {
    if (!data) return '';
    return `
        <div class="glass rounded-[2rem] p-4 flex flex-col items-center justify-center w-36 h-40 transition-all hover:-translate-y-1 border border-white/60 shadow-lg shadow-blue-900/5">
            <div class="w-12 h-12 bg-blue-50 border border-blue-100 rounded-full flex items-center justify-center mb-3 shadow-inner">
                <i class="fas ${data.icon} text-blue-600 text-lg"></i>
            </div>
            <h4 class="text-[10px] font-bold text-blue-900 uppercase text-center leading-tight tracking-widest">
                ${data.title}
            </h4>
        </div>
    `;
}

function scrollToSection(id) {
    const target = document.getElementById(id);
    if (!target) return;
    const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - (window.innerHeight / 2) + (target.offsetHeight / 2);

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

