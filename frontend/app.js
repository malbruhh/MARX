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
    const navbar = document.getElementById('navbar');

    // --- Title Shrinking Logic ---
    let scaleFactor = 1 - (scrollVal / 600);
    if (scaleFactor < 0.5) scaleFactor = 0.5; // Don't shrink too much for the new long headline

    let opacityFactor = 1 - (scrollVal / 500);
    if (opacityFactor < 0) opacityFactor = 0;

    // --- Background Darkening Shift ---
    if (scrollVal > 600) {
        body.classList.add('dark-shift');
    } else {
        body.classList.remove('dark-shift');
    }

    mainTitle.style.transform = `scale(${scaleFactor})`;
    heroWrapper.style.opacity = opacityFactor;

    // --- Navbar Effects ---
    if (scrollVal > 50) {
        navbar.classList.add('shadow-md');
        navbar.style.padding = '0.75rem 2.5rem';
    } else {
        navbar.classList.remove('shadow-md');
        navbar.style.padding = '1rem 2.5rem';
    }

    if (scrollVal > 300) {
        navLogo.style.opacity = '1';
    } else {
        navLogo.style.opacity = '0';
    }
});

// Smooth Scroll to analysis Section
const heroClickIcon = document.getElementById('hero-click-icon');

const scrollToAnalysis = () => {
    const firstCard = document.getElementById('card-1');
    if (!firstCard) return;
    
    const cardPosition = firstCard.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = cardPosition - (window.innerHeight / 2) + (firstCard.offsetHeight / 2);

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
};

if (startBtn) startBtn.addEventListener('click', scrollToAnalysis);
if (heroClickIcon) heroClickIcon.addEventListener('click', scrollToAnalysis);

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
        budgetInput.style.textAlign = 'center';
    } else {
        currencySign.style.opacity = '0';
        budgetInput.style.paddingLeft = '3rem';
        budgetInput.style.textAlign = 'center';
    }

    clearTimeout(budgetTimeout); // Reset the timer on every keystroke
    budgetTimeout = setTimeout(() => {
        if (value.length > 0 && !isNaN(value)) {
            const formattedValue = parseFloat(value).toFixed(2);
            e.target.value = formattedValue;
            // Save the formatted value to the central state
            saveState('budget', formattedValue);
            console.log(`[STATE UPDATE] BUDGET:`, formattedValue);
        }
    }, 800); //800ms delay
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
