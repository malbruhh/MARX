// /frontend/components/nextBtn.js
import { userInput, sectionToStateMap } from '../store/state.js';
import { renderSummary } from '../screens/renderSummary.js';

const sectionIds = [
    'home', 'card-1', 'card-2', 'card-3', 
    'card-4', 'card-5', 'card-6', 'card-7', 'card-8'
];

export const nextSectionBtn = () => {
    const globalNextBtn = document.getElementById('global-next-btn');
    const btnText = document.getElementById('btn-text');

    globalNextBtn.addEventListener('click', () => {
        const kpiCard = document.getElementById('card-8');

        if (btnText.innerText === "SUMMARIZE") {
            // ONLY validate when the user clicks "Summarize" at the end
            const missing = Object.entries(sectionToStateMap).find(([id, key]) => !userInput[key]);
            if (missing) {
                const sectionName = missing[1].replace('_', ' ').toUpperCase();
                alert(`Please complete the ${sectionName} section before summarizing.`);
                scrollToSection(missing[0]);
                return; // Stop and don't generate the summary
            }

            // SUCCESS: All data present, lock and summarize
            generateLockedSummary();
            return;
        }

        // REGULAR NAVIGATION (No alerts here)
        const scrollVal = window.scrollY + (window.innerHeight / 2);
        let nextTarget = sectionIds[sectionIds.length - 1];

        for (let i = 0; i < sectionIds.length - 1; i++) {
            const element = document.getElementById(sectionIds[i]);
            if (element && scrollVal < (element.getBoundingClientRect().top + window.pageYOffset + element.offsetHeight)) {
                nextTarget = sectionIds[i + 1];
                break;
            }
        }
        scrollToSection(nextTarget);
    });

    // 2. TEXT UPDATE LOGIC (Moved outside click listener)
    window.addEventListener('scroll', () => {
        const kpiCard = document.getElementById('card-8');
        if (!kpiCard || !btnText) return;

        const rect = kpiCard.getBoundingClientRect();
        // If KPI card is mostly in view, switch to Summarize
        if (rect.top < window.innerHeight * 0.4) {
            btnText.innerText = "Summarize";
        } else {
            btnText.innerText = "Next Section";
        }
    });

    // 3. VISIBILITY LOGIC (Updated to remove summary-section dependency)
    window.addEventListener('scroll', () => {
        const firstCard = document.getElementById('card-1');
        if (!firstCard || !globalNextBtn) return;

        const firstCardRect = firstCard.getBoundingClientRect();
        
        // Show button once the user reaches the first input card
        const isInsideForm = firstCardRect.top < (window.innerHeight * 0.7);

        if (isInsideForm) {
            globalNextBtn.style.opacity = '1';
            globalNextBtn.style.pointerEvents = 'auto';
            globalNextBtn.style.transform = 'translateY(0)';
        } else {
            globalNextBtn.style.opacity = '0';
            globalNextBtn.style.pointerEvents = 'none';
            globalNextBtn.style.transform = 'translateY(20px)';
        }
    });
};

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

function generateLockedSummary() {
    renderSummary();
    const summary = document.getElementById('summary-section');
    
    // Remove hidden class and ensure it's visible
    summary.classList.remove('hidden');
    summary.style.display = 'flex'; 
    summary.style.opacity = '1';

    // Hide everything else
    document.getElementById('analysis-section').style.display = 'none';
    document.getElementById('home').style.display = 'none';
    const mainAbout = document.querySelector('main');
    if(mainAbout) mainAbout.style.display = 'none';
    
    // Reset scroll to top of the now-only-existing summary page
    window.scrollTo({ top: 0, behavior: 'instant' });

    // Kill the button
    const btn = document.getElementById('global-next-btn');
    btn.style.display = 'none';
}