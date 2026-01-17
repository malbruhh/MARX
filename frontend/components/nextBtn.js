// /frontend/components/nextBtn.js
import { userInput, sectionToStateMap } from '../store/state.js';
import { renderSummary } from '../screens/renderSummary.js';

const sectionIds = [
    'home',
    'card-1', // Budget
    'card-2', // Product Type
    'card-3', // Target Customer
    'card-4', // Primary Goal
    'card-5', // Time Horizon
    'card-6', // Content Capability
    'card-7', // Sales Structure
    'card-8', // Priority KPI
    'summary-section'
];

export const nextSectionBtn = () => {
    const globalNextBtn = document.getElementById('global-next-btn');

    globalNextBtn.addEventListener('click', () => {
        const scrollVal = window.scrollY + (window.innerHeight / 2);
        let nextTarget = sectionIds[sectionIds.length - 1];

        // Find the current active section to determine the next one
        for (let i = 0; i < sectionIds.length - 1; i++) {
            const element = document.getElementById(sectionIds[i]);
            if (element && scrollVal < (element.getBoundingClientRect().top + window.pageYOffset + element.offsetHeight)) {
                nextTarget = sectionIds[i + 1];
                break;
            }
        }
        if (!nextTarget) nextTarget = 'summary-section';
        // Logic to the Summary Section
        if (nextTarget === 'summary-section') {
            const missing = Object.entries(sectionToStateMap).find(([id, key]) => !userInput[key]);
            if (missing) {
            const missingCardId = missing[0];
            const sectionName = missing[1].replace('_', ' ').toUpperCase();
            alert(`Please complete the ${sectionName} section.`);
            scrollToSection(missingCardId);
            return; // Prevent scrolling to the summary
            }
            renderSummary();
            const summary = document.getElementById('summary-section');
            summary.style.opacity = '1';
            summary.style.pointerEvents = 'auto';
        }

        const target = document.getElementById(nextTarget);
        window.scrollTo({
            top: target.getBoundingClientRect().top + window.pageYOffset - (window.innerHeight / 2) + (target.offsetHeight / 2),
            behavior: 'smooth'
        });

        // scrollToSection(nextTarget);
    });

    // Button Visibility Logic
    window.addEventListener('scroll', () => {
        const firstCard = document.getElementById('card-1');
        const summarySection = document.getElementById('summary-section');
        if (!firstCard || !summarySection || !globalNextBtn) return;

        const firstCardRect = firstCard.getBoundingClientRect();
        const summaryRect = summarySection.getBoundingClientRect();

        const isInsideForm = firstCardRect.top < (window.innerHeight * 0.7);
        const hasReachedEnd = summaryRect.top < (window.innerHeight * 0.5);

        if (isInsideForm && !hasReachedEnd) {
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
    const targetElement = document.getElementById(id);
    if (targetElement) {
        const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - (window.innerHeight / 2) + (targetElement.offsetHeight / 2);

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}