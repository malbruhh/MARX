
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
        labels.forEach((label, i) => {
            const icon = label.querySelector('.glass-icon');
            const iconImg = label.querySelector('i');
            
            if (i == val) {
                label.classList.add('opacity-100', 'scale-110');
                label.classList.remove('opacity-50');
                icon.classList.add('bg-white');
                iconImg.classList.replace('text-white/50', 'text-black');
            } else {
                label.classList.add('opacity-50');
                label.classList.remove('opacity-100', 'scale-110');
                icon.classList.remove('bg-white');
                iconImg.classList.replace('text-black', 'text-white/50');
            }
        });

        // This value is what you will send to your Python Enum
        console.log("Selected Time Horizon ID:", data[val].id);
    };

    labels.forEach((label) => {
        label.style.cursor = 'pointer';
        
        label.addEventListener('click', () => {
            const index = label.getAttribute('data-index');
            slider.value = index;
            updateUI(index);
            slider.dispatchEvent(new Event('input'));
        });
    });

    slider.addEventListener('input', (e) => updateUI(e.target.value));
    updateUI(slider.value);
    slider.addEventListener('input', (e) => updateUI(e.target.value));
    
    updateUI(slider.value);
}