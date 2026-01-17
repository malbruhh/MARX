const cards = [
    document.getElementById('card-1'),
    document.getElementById('card-2'),
    document.getElementById('card-3'),
    document.getElementById('card-4'),
    document.getElementById('card-5'),
    document.getElementById('card-6'),
    document.getElementById('card-7'),
    document.getElementById('card-8'),
    document.getElementById('summary-section'),
];

export const updateStepListener = () => {
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
}