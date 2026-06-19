let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById('recordBtn');
const submitTextBtn = document.getElementById('submitTextBtn');
const textDumpInput = document.getElementById('textDumpInput');
const statusPulse = document.getElementById('statusPulse');
const summaryCard = document.getElementById('summaryCard');
const summaryText = document.getElementById('summaryText');

// --- Modality 1: Voice Recording Processing Loops ---
recordBtn.addEventListener('click', async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        return;
    }

    audioChunks = [];
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        
        mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) audioChunks.push(e.data); };

        mediaRecorder.onstart = () => {
            recordBtn.innerHTML = `<span class="icon">⏹️</span> Stop & Process`;
            recordBtn.classList.add('recording');
            statusPulse.innerText = "Listening to your thoughts...";
            statusPulse.classList.remove('hidden');
        };

        mediaRecorder.onstop = async () => {
            recordBtn.innerHTML = `<span class="icon">🎙️</span> Start Recording`;
            recordBtn.classList.remove('recording');
            statusPulse.innerText = "Transcribing voice via Whisper and parsing tracking contracts...";
            
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('file', audioBlob, 'braindump.webm');

            try {
                const response = await fetch('/api/process-voice', { method: 'POST', body: formData });
                if (!response.ok) throw new Error('Audio pipeline execution failure.');
                
                const data = await response.json();
                renderStructuredDashboard(data);
            } catch (err) {
                showError("Error processing voice metrics.");
            }
        };

        mediaRecorder.start();
    } catch (err) {
        alert("Microphone capture access rejected.");
    }
});

// --- Modality 2: Plain Text Fallback Entry Point ---
submitTextBtn.addEventListener('click', async () => {
    const rawText = textDumpInput.value.trim();
    if (!rawText) {
        alert("Please dump some thoughts into the input box before parsing!");
        return;
    }

    statusPulse.innerText = "Processing structured note schemas...";
    statusPulse.classList.remove('hidden');

    try {
        const response = await fetch('/api/process-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: rawText })
        });

        if (!response.ok) throw new Error('Text processing response fault.');

        const data = await response.json();
        textDumpInput.value = ''; 
        renderStructuredDashboard(data);
    } catch (err) {
        showError("Error parsing text metrics.");
    }
});

// --- Unified Frontend Layout Renderer ---
function renderStructuredDashboard(data) {
    statusPulse.classList.add('hidden');

    if(data.contextual_summary) {
        summaryCard.classList.remove('hidden');
        summaryText.innerText = data.contextual_summary;
    }

    const taskList = document.getElementById('taskList');
    taskList.innerHTML = data.tasks.length ? '' : `<li class="empty-msg">No structural tasks detected.</li>`;
    data.tasks.forEach(t => {
        taskList.innerHTML += `<li><span><strong>${t.title}</strong></span> <span style="color: var(--text-muted); font-size: 0.85rem;">[${t.priority}] · ${t.estimated_minutes}m</span></li>`;
    });

    const habitList = document.getElementById('habitList');
    habitList.innerHTML = data.habits.length ? '' : `<li class="empty-msg">No routine structural loops detected.</li>`;
    data.habits.forEach(h => {
        habitList.innerHTML += `<li><span>${h.habit_name}</span> <span style="color: var(--text-muted); font-size: 0.85rem;">${h.frequency}</span></li>`;
    });

    const shoppingList = document.getElementById('shoppingList');
    shoppingList.innerHTML = data.shopping_cart.length ? '' : `<li class="empty-msg">No clear logistics items isolated.</li>`;
    data.shopping_cart.forEach(i => {
        shoppingList.innerHTML += `<li><span>${i.item_name}</span> <span style="color: var(--accent); font-size: 0.8rem; font-weight: bold;">${i.category}</span></li>`;
    });
}

function showError(msg) {
    statusPulse.innerText = msg;
    statusPulse.style.color = "var(--priority-high)";
}