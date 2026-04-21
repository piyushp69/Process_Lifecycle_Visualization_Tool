class SchedulerApp {
    constructor() {
        this.scheduler = new CPUScheduler();
        this.selectedAlgorithm = null;
        this.isSimulating = false;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Form submission logic
        document.getElementById('processForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addProcess();
        });

        // Clear button logic
        document.getElementById('clearAll').addEventListener('click', () => this.clearAll());

        // Algorithm card selection
        document.querySelectorAll('.algorithm-card').forEach(card => {
            card.addEventListener('click', () => this.selectAlgorithm(card.dataset.algo));
        });

        // Run Simulation button
        document.getElementById('simulate').addEventListener('click', () => this.runSimulation());
    }

    addProcess() {
        const pid = document.getElementById('pid').value || `P${this.scheduler.processes.length + 1}`;
        const arrival = parseInt(document.getElementById('arrivalTime').value);
        const burst = parseInt(document.getElementById('burstTime').value);
        const priority = parseInt(document.getElementById('priority').value) || 0;

        // Validation check
        if (isNaN(arrival) || isNaN(burst)) return;

        this.scheduler.addProcess(pid, arrival, burst, priority);
        this.updateProcessList();
        document.getElementById('processForm').reset();
        
        // Reset defaults for easier input
        document.getElementById('arrivalTime').value = 0;
        document.getElementById('burstTime').value = 5;
        document.getElementById('priority').value = 0;
        
        this.updateSimulateButton();
    }

    updateProcessList() {
        const list = document.getElementById('processList');
        if (this.scheduler.processes.length === 0) {
            list.innerHTML = '<div class="empty-state"><p>No processes added yet.</p></div>';
            return;
        }
        list.innerHTML = this.scheduler.processes.map(p => `
            <div class="process-item mini">
                <strong>${p.pid}</strong> 
                <span>Arrival: ${p.arrivalTime}</span> 
                <span>Burst: ${p.burstTime}</span>
                <span>Priority: ${p.priority}</span>
            </div>
        `).join('');
    }

    selectAlgorithm(algo) {
        document.querySelectorAll('.algorithm-card').forEach(c => c.classList.remove('selected'));
        const selectedCard = document.querySelector(`[data-algo="${algo}"]`);
        if (selectedCard) selectedCard.classList.add('selected');
        
        this.selectedAlgorithm = algo;
        document.getElementById('quantumInput').style.display = algo === 'rr' ? 'flex' : 'none';
        this.updateSimulateButton();
    }

    updateSimulateButton() {
        const btn = document.getElementById('simulate');
        const canRun = this.scheduler.processes.length > 0 && this.selectedAlgorithm;
        btn.disabled = !canRun;
    }

    async runSimulation() {
        if (this.isSimulating) return;
        
        this.isSimulating = true;
        document.getElementById('resultsSection').style.display = 'none'; // Hide old results
        
        const visualSection = document.getElementById('liveVisualization');
        visualSection.style.display = 'block';
        visualSection.scrollIntoView({ behavior: 'smooth' });

        const quantum = parseInt(document.getElementById('timeQuantum').value) || 2;
        
        // Start the lifecycle logic from scheduler.js
        await this.scheduler.runLifecycleSimulation(this.selectedAlgorithm, quantum, (state) => {
            this.updateLiveUI(state);
        });

        this.isSimulating = false;
        this.displayFinalResults();
    }

    updateLiveUI(state) {
        document.getElementById('globalTimeBadge').innerText = `Global Time: ${state.time}s`;
        
        const updateBox = (id, list) => {
            const container = document.querySelector(`#${id} .queue`);
            if (!container) return;
            container.innerHTML = list.map(p => `
                <div class="process-card-mini animate-pop">
                    ${p.pid} (${p.remainingTime}s left)
                </div>
            `).join('');
        };

        updateBox('box-ready', state.ready);
        updateBox('box-running', state.running ? [state.running] : []);
        updateBox('box-waiting', state.waiting);
        updateBox('box-terminated', state.terminated);
    }

    displayFinalResults() {
        const results = this.scheduler.getFinalMetrics();
        document.getElementById('resultsSection').style.display = 'block';
        
        // 1. Render Gantt Chart
        const gantt = document.getElementById('ganttChart');
        gantt.innerHTML = results.schedule.map(block => `
            <div class="gantt-block ${block.isIdle ? 'idle' : 'process-color-1'}" 
                 style="flex-grow: ${block.endTime - block.startTime}; min-width: 40px;">
                <strong>${block.pid}</strong>
                <small>${block.startTime}-${block.endTime}</small>
            </div>
        `).join('');

        // 2. Render Metrics Table
        const tableDiv = document.getElementById('metricsTable');
        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Arrival</th>
                        <th>Burst</th>
                        <th>Exit</th>
                        <th>TAT</th>
                        <th>WT</th>
                    </tr>
                </thead>
                <tbody>
        `;

        results.processes.forEach(p => {
            const tat = p.completionTime - p.arrivalTime;
            const wt = Math.max(0, tat - p.burstTime);
            tableHTML += `
                <tr>
                    <td><strong>${p.pid}</strong></td>
                    <td>${p.arrivalTime}</td>
                    <td>${p.burstTime}</td>
                    <td>${p.completionTime}</td>
                    <td>${tat}</td>
                    <td>${wt}</td>
                </tr>
            `;
        });

        tableHTML += `</tbody></table>`;
        tableDiv.innerHTML = tableHTML;

        // 3. Render Performance Summary
        document.getElementById('performanceSummary').innerHTML = `
            <div class="metric-card">
                <div class="metric-value">${results.avgWT.toFixed(2)}s</div>
                <div class="metric-label">Avg Waiting Time</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${results.avgTAT.toFixed(2)}s</div>
                <div class="metric-label">Avg Turnaround Time</div>
            </div>
        `;

        // Final scroll to results
        setTimeout(() => {
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        }, 500);
    }

    clearAll() {
        this.scheduler.clearProcesses();
        this.updateProcessList();
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('liveVisualization').style.display = 'none';
        this.updateSimulateButton();
        this.isSimulating = false;
    }
}

// Initialize App
window.app = new SchedulerApp();
