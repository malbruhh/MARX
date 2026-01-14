// /frontend/components/renderCarousel.js
export function initializeCarousel(data, containerId) {
    const carousel = document.getElementById(containerId);
    if (!carousel) return;

    data.forEach(item => {
        const card = document.createElement('div');
        // Combined your sizing fix (larger cards) with your glass classes
        card.className = 'fact-card glass rounded-[1.5rem] cursor-pointer p-6 flex items-center gap-5';
        card.dataset.id = item.id; // Store ID for potential JSON parsing

        card.innerHTML = `
            <div class="w-14 h-14 bg-white/90 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm">
                <i class="fas ${item.icon} fact-icon text-black text-xl"></i>
            </div>
            <div>
                <h3 class="font-bold text-white text-[15px] uppercase tracking-wider">${item.title}</h3>
                <p class="text-[11px] text-white/50 leading-tight">${item.desc}</p>
            </div>
        `;

        card.addEventListener('click', () => {
            document.querySelectorAll('.fact-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            // Log for your future HTTP POST
            console.log(`Product selected: ${item.id}`);
        });

        carousel.appendChild(card);
    });
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