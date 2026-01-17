const sectionIds = [
    'home',
    'card-1', // Budget
    'card-2', // Product Type
    'card-3', // Target Customer
    'card-4', // Primary Goal
    'card-5', // time horizon
    'card-6', // capability
    'card-7', // sales structure
    'card-8', // kpi
    'summary-section'
];
export const nextSectionBtn = () => {
    const globalNextBtn = document.getElementById('global-next-btn');

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
            // Use centering logic for a professional scroll focus
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
}