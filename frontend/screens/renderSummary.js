// /frontend/screens/renderSummary.js
import { userInput } from '../store/state.js';
import { productData, targetCustomerData, primaryGoalData, timeHorizonData, capabilityData, salesStructureData, kpiData } from '../components/inputData.js';

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
        <div class="flex flex-col items-center w-full max-w-6xl px-10">
            <h2 class="text-6xl font-extrabold text-white mb-2 tracking-tighter">SUMMARY</h2>
            <p class="text-2xl text-pink-200 font-light mb-12 italic">Budget: $${userInput.budget || '0'}</p>

            <div class="flex flex-wrap justify-center gap-4 mb-6 w-full">
                ${['product_type', 'target_customer', 'primary_goal', 'time_horizon'].map(key => renderMiniCard(getSelectionData(key))).join('')}
            </div>

            <div class="flex flex-wrap justify-center gap-4 mb-16 w-full">
                ${['content_capability', 'sales_structure', 'priority_kpi'].map(key => renderMiniCard(getSelectionData(key))).join('')}
            </div>

            <div class="flex flex-col md:flex-row gap-6 items-center">
                <button id="back-to-edit" class="px-8 py-4 rounded-2xl border border-white/10 text-white/40 hover:text-white hover:bg-white/5 transition-all text-sm uppercase font-bold tracking-widest">
                    <i class="fas fa-pen-to-square mr-2"></i> Edit Selections
                </button>
                <button id="analyze-btn" class="px-16 py-5 rounded-full btn-glass text-xl font-bold tracking-[0.3em] uppercase">
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
}

function renderMiniCard(data) {
    if (!data) return '';
    return `
        <div class="glass rounded-2xl p-4 flex flex-col items-center justify-center w-36 h-36 transition-all hover:scale-105 border border-white/10">
            <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center mb-3">
                <i class="fas ${data.icon} text-white text-lg"></i>
            </div>
            <h4 class="text-[10px] font-bold text-white uppercase text-center leading-tight tracking-wider">${data.title}</h4>
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

