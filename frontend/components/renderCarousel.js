// /frontend/components/renderCarousel.js
export function initializeCarousel(data, containerId) {
    const carousel = document.getElementById(containerId);
    if (!carousel) return;

    carousel.innerHTML = '';
    
    // Reset Grid: Removes 'grid-flow-col' for fixed layouts
    carousel.className = 'grid gap-8 w-full transition-all duration-500';

    if (data.length === 3) {
        carousel.classList.add('grid-cols-3', 'md:grid-cols-2', 'justify-items-center', 'gap-x-2', 'ml-4');
    } else if (data.length === 4) {
        carousel.classList.add('md:grid-cols-2', 'justify-items-center', 'gap-x-1', 'ml-4');
    } else if (data.length === 5) {
        carousel.classList.add('grid-cols-2', 'justify-items-center', 'gap-4', 'ml-4');
    } else {
        carousel.classList.add('grid-flow-col', 'grid-rows-3', 'gap-5');
    }

    data.forEach((item, index) => {
        const card = document.createElement('div');
        
        let cardClasses = 'fact-card glass rounded-[1.5rem] cursor-pointer flex transition-all duration-300';
        if (data.length === 3 || data.length === 4) {
            cardClasses += ' flex-col items-center text-center p-4 justify-center';
            if (data.length === 3) {
            cardClasses += ' w-full md:w-[240px]';
        } else {
            card.style.width = '240px';
        }
        card.style.height = '250px';
    } else if (data.length === 5) {
            cardClasses += ' items-center gap-5 p-6';
            card.style.width = '280px';
            card.style.height = '140px';
    } else {
            // Original horizontal look
            cardClasses += ' items-center gap-5 p-6';
        }

        if (data.length === 3 && index === 2) {
        cardClasses += ' md:col-span-2';
    }

        if (data.length === 5 && index === 4) {
            cardClasses += ' col-span-2 justify-self-center';
        }

        if (data.length === 4) {
            if (index === 0 || index === 2) {
                cardClasses += ' md:-translate-y-10'; 
            }
        }

        card.className = cardClasses;
        card.dataset.id = item.id;

        card.innerHTML = `
            <div class="w-14 h-14 bg-white/90 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm ${data.length <= 4 ? 'mb-2' : ''}">
                <i class="fas ${item.icon} fact-icon"></i>
            </div>
            <div>
                <h3 class="font-bold text-white text-[15px] uppercase tracking-wider">${item.title}</h3>
                <p class="text-[11px] text-white/50 leading-tight">${item.desc}</p>
            </div>
        `;

        card.addEventListener('click', () => {
            carousel.querySelectorAll('.fact-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });

        carousel.appendChild(card);
    });

    // Cleanup: Remove masks/drag cues for fixed small layouts
    const wrapper = carousel.parentElement;
    if (data.length <= 5) {
        wrapper.style.maskImage = 'none';
        wrapper.style.webkitMaskImage = 'none';
        wrapper.classList.remove('cursor-grab', 'active:cursor-grabbing');
        wrapper.style.overflow = 'visible'; 
    }
}
// Function to enable dragging on any element
export function enableDrag(containerId) {
    const slider = document.getElementById(containerId);
    let isDown = false;
    let startX;
    let scrollLeft;

    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        slider.classList.add('active');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });

    slider.addEventListener('mouseleave', () => { 
        isDown = false; 
        slider.classList.remove('active');
    });
    
    slider.addEventListener('mouseup', () => { 
        isDown = false; 
        slider.classList.remove('active');
    });

    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; 
        slider.scrollLeft = scrollLeft - walk;
    });
}