import { productData, targetCustomerData } from './components/inputData.js';
import { initializeCarousel, enableDrag} from './components/renderCarousel.js';



// Grab necessary elements
const mainTitle = document.getElementById('main-title');
const heroWrapper = document.getElementById('hero-wrapper');
const navLogo = document.getElementById('nav-logo');
const body = document.body;
const startBtn = document.getElementById('scroll-trigger');

// Grab Input and Progress elements
const budgetInput = document.getElementById('budget-input');
const currencySign = document.getElementById('currency-sign');
const steps = document.querySelectorAll('.step-circle');
const cards = [
    document.getElementById('card-1'),
    document.getElementById('card-2'),
    document.getElementById('card-3'),
    document.getElementById('card-4'),
    document.getElementById('card-5')
    ];

// Scroll event listener
window.addEventListener('scroll', () => {
    const scrollVal = window.scrollY;
    const windowHeight = window.innerHeight;
    const totalHeight = document.documentElement.scrollHeight;

    // --- 1. Title Shrinking Logic ---
    let scaleFactor = 1 - (scrollVal / 600);
    if (scaleFactor < 0.1) scaleFactor = 0.1;

    let opacityFactor = 1 - (scrollVal / 500);
    if (opacityFactor < 0) opacityFactor = 0;

    mainTitle.style.transform = `scale(${scaleFactor})`;
    heroWrapper.style.opacity = opacityFactor;

    // --- 2. Navbar Logo Toggle ---
    if (scrollVal > 400) {
        navLogo.style.opacity = '1';
    } else {
        navLogo.style.opacity = '0';
    }

    // --- 3. THE REVERSE GRADIENT LOGIC ---
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

// Smooth Scroll to Next Section
startBtn.addEventListener('click', () => {
    const target = document.getElementById('analysis-section');
    
    // Get the distance from the top of the document to the target element
    const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
    
    // Calculate the middle: Element Position - (Half of Window Height) + (Half of Element Height)
    // If the section is very tall (like 400vh), we usually want to scroll to the middle 
    // of the FIRST card, not the middle of the entire 400vh section.
    
    // To scroll to the middle of the first card (card-1):
    const firstCard = document.getElementById('card-1');
    const cardPosition = firstCard.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = cardPosition - (window.innerHeight / 2) + (firstCard.offsetHeight / 2);

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
});

// --- 1. Budget Input Logic ---
budgetInput.addEventListener('input', (e) => {
    // Only allow numbers and decimal point
    let value = e.target.value.replace(/[^0-9.]/g, '');
    
    // Prevent multiple decimals
    const parts = value.split('.');
    if (parts.length > 2) value = parts[0] + '.' + parts.slice(1).join('');
    
    e.target.value = value;

    // Toggle $ sign visibility and adjust text alignment
    if (value.length > 0) {
        currencySign.style.opacity = '1';
        budgetInput.style.paddingLeft = '4rem';
        budgetInput.style.textAlign = 'left';
    } else {
        currencySign.style.opacity = '0';
        budgetInput.style.paddingLeft = '3rem';
        budgetInput.style.textAlign = 'center';
    }
});

// --- 2. Progress Bar Tracking Logic ---
window.addEventListener('scroll', () => {
    const scrollVal = window.scrollY;
    const windowHeight = window.innerHeight;

    // Check which "card" is currently in the middle of the screen
    cards.forEach((card, index) => {
        if (!card) return;
        const rect = card.getBoundingClientRect();
        const stepElement = document.getElementById(`step-${index + 1}`);

        // If the card top has entered the upper half of the viewport
        if (rect.top < windowHeight * 0.5) {
            stepElement.classList.add('active');
        } else {
            stepElement.classList.remove('active');
        }
    });
});

initializeCarousel(productData, 'product-carousel');
initializeCarousel(targetCustomerData, 'customer-carousel');
enableDrag('drag-product');
enableDrag('drag-customer');
// Data for Product Type
// const productData = [
//     { id: 'b2b_saas', title: 'Business-to-Business SaaS', desc: 'Enterprise software solutions.', icon: 'fa-server' },
//     { id: 'b2c_retail', title: 'Business-to-Consumer Retail', desc: 'Direct consumer goods.', icon: 'fa-bag-shopping' },
//     { id: 'local_service', title: 'Local Service', desc: 'Regional physical services.', icon: 'fa-location-dot' },
//     { id: 'consulting', title: 'Consulting', desc: 'Expert professional advice.', icon: 'fa-user-tie' },
//     { id: 'digital_product', title: 'Digital Product', desc: 'Online courses and assets.', icon: 'fa-file-code' },
//     { id: 'fmcg', title: 'Fast-Moving Consumer Goods', desc: 'everyday, non-durable goods sold quickly at low prices for consumers ', icon: 'fa-cart-flatbed' },
//     // Draggable Items
//     { id: 'technical_tools', title: 'Technical Tools', desc: 'Niche hardware/software.', icon: 'fa-screwdriver-wrench' },
//     { id: 'hospitality', title: 'Hospitality', desc: 'Tourism and travel.', icon: 'fa-bed' },
//     { id: 'subscription', title: 'Subscription', desc: 'Recurring revenue models.', icon: 'fa-arrows-rotate' }
// ];
// const carousel = document.getElementById('product-carousel');
// const dragContainer = document.getElementById('drag-container');

// // Render the 9 Cards
// productData.forEach(item => {
//     const card = document.createElement('div');
//     card.className = 'fact-card glass rounded-[1.5rem] cursor-pointer';
//     card.innerHTML = `
//         <div class="w-14 h-14 bg-white/90 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm">
//             <i class="fas ${item.icon} fact-icon"></i>
//         </div>
//         <div>
//             <h3 class="font-bold text-white text-[15px] uppercase tracking-wider">${item.title}</h3>
//             <p class="text-[11px] text-white/50 leading-tight">${item.desc}</p>
//         </div>
//     `;

//     card.addEventListener('click', () => {
//         document.querySelectorAll('.fact-card').forEach(c => c.classList.remove('selected'));
//         card.classList.add('selected');
//     });

//     carousel.appendChild(card);
// });

// // Dragging Logic
// let isDown = false;
// let startX;
// let scrollLeft;

// dragContainer.addEventListener('mousedown', (e) => {
//     isDown = true;
//     dragContainer.classList.add('active');
//     startX = e.pageX - dragContainer.offsetLeft;
//     scrollLeft = dragContainer.scrollLeft;
// });

// dragContainer.addEventListener('mouseleave', () => { isDown = false; });
// dragContainer.addEventListener('mouseup', () => { isDown = false; });

// dragContainer.addEventListener('mousemove', (e) => {
//     if (!isDown) return;
//     e.preventDefault();
//     const x = e.pageX - dragContainer.offsetLeft;
//     const walk = (x - startX) * 2; 
//     dragContainer.scrollLeft = scrollLeft - walk;
// }); 



// Put this at lowest
const globalNextBtn = document.getElementById('global-next-btn');

// Array of section IDs in order of progress
const sectionIds = [
    'home',
    'card-1', // Budget
    'card-2', // Product Type
    'card-3', // Target Customer
    'card-4', // Primary Goal
    'summary-section'
];

globalNextBtn.addEventListener('click', () => {
    const scrollVal = window.scrollY + (window.innerHeight / 2); // Center-based detection
    let nextTarget = sectionIds[sectionIds.length - 1]; // Default to summary

    // Loop through sections to find where we currently are
    for (let i = 0; i < sectionIds.length - 1; i++) {
        const element = document.getElementById(sectionIds[i]);
        if (element) {
            const rect = element.getBoundingClientRect();
            const elementTop = rect.top + window.pageYOffset;
            
            // If we are currently "in" this section, the next target is i+1
            if (scrollVal < elementTop + element.offsetHeight) {
                nextTarget = sectionIds[i + 1];
                break;
            }
        }
    }

    const targetElement = document.getElementById(nextTarget);
    if (targetElement) {
        // Use our centering logic for a professional scroll focus
        const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - (window.innerHeight / 2) + (targetElement.offsetHeight / 2);

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
});

// Hide the button when on  Home and the Summary Page
window.addEventListener('scroll', () => {
    const firstCard = document.getElementById('card-1');
    const summarySection = document.getElementById('summary-section');
    const nextBtn = document.getElementById('global-next-btn');
    
    if (!firstCard || !summarySection || !nextBtn) return;

    const firstCardRect = firstCard.getBoundingClientRect();
    const summaryRect = summarySection.getBoundingClientRect();

    // Logic: 
    // 1. Show if the top of the Budget card is near the middle of the screen
    // 2. Hide if the Summary section has reached the screen
    const isInsideForm = firstCardRect.top < (window.innerHeight * 0.7);
    const hasReachedEnd = summaryRect.top < (window.innerHeight * 0.9);

    if (isInsideForm && !hasReachedEnd) {
        nextBtn.style.opacity = '1';
        nextBtn.style.pointerEvents = 'auto';
        nextBtn.style.transform = 'translateY(0)';
    } else {
        nextBtn.style.opacity = '0';
        nextBtn.style.pointerEvents = 'none';
        nextBtn.style.transform = 'translateY(20px)';
    }
});