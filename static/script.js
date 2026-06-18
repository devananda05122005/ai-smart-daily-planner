let tasks = [];

function addTask() {
    const taskName = document.getElementById("taskName").value;
    const deadline = document.getElementById("deadline").value;
    const duration = document.getElementById("duration").value;
    const priority = document.getElementById("priority").value;

    if (!taskName || !deadline || !duration || !priority) {
        alert("Please fill all fields.");
        return;
    }

    const task = {
        name: taskName,
        deadline: deadline,
        duration: duration,
        priority: priority,
        energy_required: priority === "High" ? "High" : "Medium"
    };

    tasks.push(task);

    const li = document.createElement("li");
    li.innerHTML = `
        <strong>${task.name}</strong> | 
        Deadline: ${task.deadline} | 
        Duration: ${task.duration} | 
        Priority: ${task.priority}
    `;
    document.getElementById("taskList").appendChild(li);

    // Reset input fields cleanly
    document.getElementById("taskName").value = "";
    document.getElementById("deadline").value = "";
    document.getElementById("duration").value = "";
}

async function optimizeTasks() {
    const freeTimeInput = document.getElementById("freeTime").value;

    if (!freeTimeInput) {
        alert("Please enter your available free time slots.");
        return;
    }

    const freeTime = freeTimeInput.split(",").map(slot => slot.trim()).filter(slot => slot.length > 0);
    const peakHours = freeTime.length > 0 ? [freeTime[0]] : [];

    try {
        const response = await fetch("/optimize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tasks: tasks,
                free_time: freeTime,
                peak_hours: peakHours,
                fixed_tasks: []
            })
        });

        const resBody = await response.json();

        // Secure handling of the error containment envelope 
        if (!resBody.success) {
            document.getElementById("result").innerHTML = `
                <div class="status-box" style="border-left: 5px solid #d9534f; background: #fdf7f7;">
                    <strong>Optimization Failed:</strong> ${resBody.error || "Unknown server event processing problem."}
                </div>`;
            return;
        }

        displayResult(resBody.data);

    } catch (error) {
        document.getElementById("result").innerHTML = `
            <div class="status-box" style="border-left: 5px solid #d9534f;">
                <strong>Network/Client Exception:</strong> ${error.message}
            </div>`;
    }
}

function displayResult(result) {
    let output = "";

    // 1. Optimized Schedule Block
    output += "<h2>Optimized Schedule</h2>";
    if (result.optimized_schedule && result.optimized_schedule.length > 0) {
        result.optimized_schedule.forEach(task => {
            output += `
                <div class="task-card">
                    <h3>${task.name || "Untitled Task"}</h3>
                    <p><strong>Deadline:</strong> ${task.deadline || "N/A"}</p>
                    <p><strong>Duration:</strong> ${task.duration || "N/A"}</p>
                    <p><strong>Time Slot:</strong> ${task.start_time || "N/A"} - ${task.end_time || "N/A"}</p>
                </div>`;
        });
    } else {
        output += "<p>No tasks scheduled.</p>";
    }

    // 2. Break Management Block
    output += "<h2>Break Suggestions</h2>";
    if (result.break_suggestions && result.break_suggestions.length > 0) {
        result.break_suggestions.forEach(item => {
            output += `
                <div class="task-card" style="border-left-color: #2196F3;">
                    <p><strong>Timing:</strong> ${item.start_time || "N/A"} - ${item.end_time || "N/A"}</p>
                    <p><strong>Reason:</strong> ${item.reason || "Recovery window"}</p>
                </div>`;
        });
    }

    // 3. Priority Order Sequence List
    output += "<h2>Priority Sequencing</h2><ul>";
    (result.priority_order || []).forEach(taskName => {
        output += `<li>${taskName}</li>`;
    });
    output += "</ul>";

    // 4. Focus Block Segments
    output += "<h2>Focus Blocks</h2>";
    (result.focus_blocks || []).forEach(block => {
        output += `
            <div class="task-card" style="border-left-color: #673AB7;">
                <h3>${block.name || "Deep Work Segment"}</h3>
                <p><strong>Duration:</strong> ${block.start_time || "N/A"} - ${block.end_time || "N/A"}</p>
            </div>`;
    });

    // 5. Overflow Management State
    const overloadText = result.overload_detected ? "Yes - Task load exceeds available slots" : "No";
    output += `
        <h2>Overload Status</h2>
        <div class="status-box">${overloadText}</div>`;

    if (result.postponed_tasks && result.postponed_tasks.length > 0) {
        output += "<h3>Postponed Tasks</h3><ul>";
        result.postponed_tasks.forEach(task => { output += `<li>${task}</li>`; });
        output += "</ul>";
    }

    // 6. Analytics Scores
    output += `
        <h2>Focus Score Prediction</h2>
        <div class="score-box">${result.focus_score_prediction || "N/A"}</div>
        <h2>Productivity Score</h2>
        <div class="score-box">${result.productivity_score || "N/A"}</div>`;

    // 7. Planner Decision Logic Logs
    output += "<h2>AI Strategy Logic</h2><ul>";
    (result.reasoning || []).forEach(reason => {
        output += `<li>${reason}</li>`;
    });
    output += "</ul>";

    document.getElementById("result").innerHTML = output;
}