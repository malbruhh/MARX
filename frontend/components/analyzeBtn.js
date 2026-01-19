// /frontend/components/analyzeBtn.js
import { userInput, saveAnalysisResult } from '../store/state.js';

export const initializeAnalyzeBtn = (btnId) => {
    const btn = document.getElementById(btnId);
    if (!btn) return;

    btn.addEventListener('click', async () => {
        toggleLoading(btn, true);

        try {
            // Prepare the payload to match API expectations
            const payload = {
                ...userInput,
                raw_budget_amount: parseFloat(userInput.budget) || 0
            };
            // Remove the old 'budget' key if your API is strict
            delete payload.budget;
            console.log(payload);
            const response = await fetch('http://127.0.0.1:8000/api/analyze', {
                method: 'POST',
                headers: { 
                    'accept': 'application/json',
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const result = await response.json();
            saveAnalysisResult(result);

            // Transition logic
            const summary = document.getElementById('summary-section');
            const final = document.getElementById('final-section');
            if (summary && final) {
                summary.style.display = 'none';
                final.style.display = 'flex';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }

        } catch (error) {
            console.error("Analysis Error:", error);
            // Specific error message for debugging
            alert(`Backend Error: ${error.message}. Ensure FastAPI is running at port 8000.`);
            toggleLoading(btn, false);
        }
    });
};

function toggleLoading(btn, isLoading) {
    if (isLoading) {
        btn.disabled = true;
        btn.classList.add('opacity-50', 'cursor-not-allowed', 'scale-95');
        btn.innerHTML = `
            <div class="flex items-center gap-3">
                <i class="fas fa-circle-notch animate-spin text-2xl"></i>
                <span class="tracking-[0.2em] font-bold">Synthesizing Strategy...</span>
            </div>
        `;
    } else {
        btn.disabled = false;
        btn.classList.remove('opacity-50', 'cursor-not-allowed', 'scale-95');
        btn.innerHTML = `ANALYZE STRATEGY`;
    }
}