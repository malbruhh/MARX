import { saveState } from "../store/state.js";

export function initializeSlider(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="w-full min-w-[60vh] mx-auto px-4 py-12">
            <div class="relative h-2 bg-white/20 rounded-full mb-8 glass">
                <input type="range" id="time-slider" 
                    min="0" max="${data.length - 1}" step="1" value="1"
                    class="absolute w-full h-3 bg-transparent appearance-none cursor-pointer z-10">
                
                <div id="slider-progress" class="absolute h-full bg-white rounded-full transition-all duration-300" style="width: 50%;"></div>
            </div>

            <div class="flex justify-between items-start">
                ${data.map((item, index) => `
                    <div class="flex flex-col items-center text-center transition-all duration-300 slider-label whitespace-nowrap" style="width: 0; overflow: visible;" data-index="${index}">
                        <div class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center mb-2 glass-icon transition-colors">
                            <i class="fas ${item.icon} text-white/50"></i>
                        </div>
                        <h4 class="text-white font-bold text-sm uppercase tracking-tighter">${item.title}</h4>
                        <p class="text-[10px] text-white/40 italic">${item.desc}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    const slider = container.querySelector('#time-slider');
    const progress = container.querySelector('#slider-progress');
    const labels = container.querySelectorAll('.slider-label');

    const updateUI = (val) => {
        // Update Progress Bar width
        const percent = (val / (data.length - 1)) * 100;
        progress.style.width = `${percent}%`;

        // Update Labels (Highlighting)
        labels.forEach((label) => {
            label.style.cursor = 'pointer';
            label.addEventListener('click', () => {
                const index = label.getAttribute('data-index');
                slider.value = index;
                // Dispatching 'input' is enough; the listener below will catch it and run updateUI once.
                slider.dispatchEvent(new Event('input')); 
            });
        //save state
        const stateKey = containerId.includes('time') ? 'time_horizon' : 'content_capability';
        saveState(stateKey, data[val].id);
        });
        const categoryLabel = containerId.replace('-container', '').replace('-', ' ').toUpperCase();
        console.log(`[STATE UPDATE] ${categoryLabel}:`, data[val].id);
    };
    
    slider.addEventListener('input', (e) => updateUI(e.target.value));
    updateUI(slider.value);
}