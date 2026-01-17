import { productData, targetCustomerData, primaryGoalData, timeHorizonData, capabilityData, salesStructureData, kpiData } from './components/inputData.js';
import { initializeCarousel, enableDrag} from './components/renderCarousel.js';
import { initializeSlider } from './components/renderSlider.js';
import { updateStepListener } from './hooks/scrollStepListener.js';
import { nextSectionBtn } from './components/nextBtn.js';
import { saveState } from './store/state.js';

nextSectionBtn();
updateStepListener();

const mainTitle = document.getElementById('main-title');
const heroWrapper = document.getElementById('hero-wrapper');
const navLogo = document.getElementById('nav-logo');
const body = document.body;
const startBtn = document.getElementById('scroll-trigger');

const budgetInput = document.getElementById('budget-input');
const currencySign = document.getElementById('currency-sign');

// Scroll event listener
window.addEventListener('scroll', () => {
    const scrollVal = window.scrollY;
    const windowHeight = window.innerHeight;
    const totalHeight = document.documentElement.scrollHeight;

    // --- Title Shrinking Logic ---
    let scaleFactor = 1 - (scrollVal / 600);
    if (scaleFactor < 0.1) scaleFactor = 0.1;

    let opacityFactor = 1 - (scrollVal / 500);
    if (opacityFactor < 0) opacityFactor = 0;

    mainTitle.style.transform = `scale(${scaleFactor})`;
    heroWrapper.style.opacity = opacityFactor;

    if (scrollVal > 400) {
        navLogo.style.opacity = '1';
    } else {
        navLogo.style.opacity = '0';
    }

    // We want the light to move to the bottom as we reach the "Next Section"
    // Trigger the inversion when the user is 60% down the page
    const reverseThreshold = totalHeight * 0.6;

    if (scrollVal > reverseThreshold) {
        body.classList.add('inverted');
    } else {
        // This ensures that when you scroll back UP, it goes back to the top-light
        body.classList.remove('inverted');
    }
});

// Smooth Scroll to analysis Section
startBtn.addEventListener('click', () => {
    const target = document.getElementById('analysis-section');
    
    // Get the distance from the top of the document to the target element
    const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
    
    const firstCard = document.getElementById('card-1');
    const cardPosition = firstCard.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = cardPosition - (window.innerHeight / 2) + (firstCard.offsetHeight / 2);

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
});

// --- Budget Input Logic ---
let budgetTimeout; // Variable to hold the timer

budgetInput.addEventListener('input', (e) => {
    // Filter: Numbers and decimal only (No '-' or letters)
    let value = e.target.value.replace(/[^0-9.]/g, '');
    
    // Prevent multiple decimals
    const parts = value.split('.');
    if (parts.length > 2) value = parts[0] + '.' + parts.slice(1).join('');
    
    e.target.value = value;

    if (value.length > 0) {
        currencySign.style.opacity = '1';
        budgetInput.style.paddingLeft = '4rem';
        budgetInput.style.textAlign = 'left';
    } else {
        currencySign.style.opacity = '0';
        budgetInput.style.paddingLeft = '3rem';
        budgetInput.style.textAlign = 'center';
    }

    // 3. Debounced State Saving and Logging
    clearTimeout(budgetTimeout); // Reset the timer on every keystroke
    budgetTimeout = setTimeout(() => {
        saveState('budget', value);
        console.log(`[STATE UPDATE] BUDGET:`, value);
    }, 600); // Waits for 600ms of "silence" before saving
});



initializeCarousel(productData, 'product-carousel');
initializeCarousel(targetCustomerData, 'customer-carousel');
initializeCarousel(primaryGoalData, 'goal-carousel');
initializeCarousel(salesStructureData, 'sales-carousel');
initializeCarousel(kpiData, 'kpi-carousel');
enableDrag('drag-product');
enableDrag('drag-customer');

initializeSlider(timeHorizonData, 'time-horizon-container');
initializeSlider(capabilityData, 'capability-container');
