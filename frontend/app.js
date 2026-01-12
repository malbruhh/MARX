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