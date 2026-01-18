// /frontend/hooks/scrollStepListener.js

export const updateStepListener = () => {
    const cardIds = [
        'card-1', 'card-2', 'card-3', 'card-4', 
        'card-5', 'card-6', 'card-7', 'card-8', 
        'summary-section'
    ];

    window.addEventListener('scroll', () => {
        const windowHeight = window.innerHeight;
    
        cardIds.forEach((id, index) => {
            const card = document.getElementById(id);
            if (!card) return;

            const rect = card.getBoundingClientRect();
            const stepElement = document.getElementById(`step-${index + 1}`);
    
            if (stepElement) {
                if (rect.top < windowHeight * 0.5) {
                    stepElement.classList.add('active');
                } else {
                    stepElement.classList.remove('active');
                }
            }
            // If scroll toward the summary section
            if (id === 'summary-section' && rect.top < windowHeight * 0.8) {
                // Check if all data is present
                const isComplete = Object.values(sectionToStateMap).every(key => 
                    userInput[key] !== null && userInput[key] !== ""
                );

                if (isComplete) {
                    renderSummary();
                    card.style.opacity = '1';
                    card.style.pointerEvents = 'auto';
                }
            }
        });
    });
}