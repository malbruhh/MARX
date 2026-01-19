import { saveState } from "../store/state.js";

export function initializeSlider(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // We use a relative container to house the track and the nodes
    container.innerHTML = `
        <div class="w-full max-w-5xl mx-auto px-4 py-16">
            <div class="relative flex items-center justify-between">
                
                <div class="absolute top-1/2 left-0 w-full h-1.5 bg-gray-200/50 rounded-full -translate-y-1/2 glass"></div>
                
                <div id="slider-progress-${containerId}" 
                     class="absolute top-1/2 left-0 h-1.5 bg-blue-600 rounded-full -translate-y-1/2 transition-all duration-500 shadow-[0_0_15px_rgba(37,99,235,0.3)]" 
                     style="width: 0%;"></div>

                ${data.map((item, index) => `
                    <div class="relative z-10 flex flex-col items-center group cursor-pointer slider-node" data-index="${index}">
                        <div class="node-circle w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 
                                     bg-white/60 glass border border-gray-100 
                                     group-hover:shadow-[0_0_20px_rgba(30,58,138,0.1)] group-hover:scale-110">
                            <i class="fas ${item.icon} node-icon text-gray-400 transition-all duration-500 text-lg"></i>
                        </div>
                        
                        <div class="absolute top-16 w-40 text-center transition-all duration-500 node-label opacity-40 scale-95">
                            <h4 class="text-blue-900 font-extrabold text-lg uppercase tracking-tighter leading-tight">${item.title}</h4>
                            <p class="text-[11px] text-gray-500 italic font-light">${item.desc}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    const nodes = container.querySelectorAll('.slider-node');
    const progress = container.querySelector(`#slider-progress-${containerId}`);

    const updateUI = (activeIndex) => {
        // 1. Update Progress Bar Width
        const percentage = (activeIndex / (data.length - 1)) * 100;
        progress.style.width = `${percentage}%`;

        // 2. Update Node States
        nodes.forEach((node, i) => {
            const circle = node.querySelector('.node-circle');
            const icon = node.querySelector('.node-icon');
            const label = node.querySelector('.node-label');

            if (parseInt(i) === parseInt(activeIndex)) {
                // Active State: Solid Blue, Flipped Icon, Scaled Up
                circle.classList.remove('bg-white/60', 'text-gray-400');
                circle.classList.add('bg-blue-600', 'scale-150', 'shadow-[0_0_25px_rgba(37,99,235,0.3)]');
                
                icon.classList.remove('text-gray-400');
                icon.classList.add('text-white', 'scale-110'); // Icon scale included
                
                label.classList.remove('opacity-40', 'scale-95');
                label.classList.add('opacity-100', 'scale-100', 'translate-y-2');
            } else {
                // Inactive State: Glassy, Semi-transparent
                circle.classList.add('bg-white/60');
                circle.classList.remove('bg-blue-600', 'scale-150', 'shadow-[0_0_25px_rgba(37,99,235,0.3)]');
                
                icon.classList.add('text-gray-400');
                icon.classList.remove('text-white', 'scale-110');
                
                label.classList.add('opacity-40', 'scale-95');
                label.classList.remove('opacity-100', 'scale-100', 'translate-y-2');
            }
        });

        // 3. Save State and Log
        const stateKey = containerId.includes('time') ? 'time_horizon' : 'content_capability';
        saveState(stateKey, data[activeIndex].id);
        
        const categoryLabel = containerId.replace('-container', '').replace('-', ' ').toUpperCase();
        console.log(`[STATE UPDATE] ${categoryLabel}:`, data[activeIndex].id);
    };

    // Add Click Listeners to Nodes
    nodes.forEach((node) => {
        node.addEventListener('click', () => {
            const index = node.getAttribute('data-index');
            updateUI(index);
        });
    });

    // Initialize with default value (index 1 for Medium as per your original logic)
    updateUI(1);
}