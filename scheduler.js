class Process {
    constructor(pid, arrival, burst, priority) {
        this.pid = pid;
        this.arrivalTime = arrival;
        this.burstTime = burst;
        this.priority = priority;
        this.remainingTime = burst;
        this.startTime = null;
        this.completionTime = null;
    }
}

class CPUScheduler {
    constructor() {
        this.processes = [];
        this.history = [];
        this.time = 0;
    }

    addProcess(pid, arrival, burst, priority) {
        this.processes.push(new Process(pid, arrival, burst, priority));
    }

    clearProcesses() {
        this.processes = [];
        this.history = [];
        this.time = 0;
    }

    async runLifecycleSimulation(algo, quantum, onTick) {
        // Reset everything before start
        this.time = 0;
        this.history = [];
        this.processes.forEach(p => {
            p.remainingTime = p.burstTime;
            p.startTime = null;
            p.completionTime = null;
        });

        let unarrived = [...this.processes];
        let ready = [];
        let waiting = [];
        let terminated = [];
        let running = null;

        // Same loop as your second code
        while (unarrived.length > 0 || ready.length > 0 || waiting.length > 0 || running) {
            
            // 1. Check Arrivals (p.arrival <= self.time)
            let arrivedNow = unarrived.filter(p => p.arrivalTime <= this.time);
            arrivedNow.forEach(p => {
                ready.push(p);
                unarrived = unarrived.filter(up => up.pid !== p.pid);
            });

            // 2. 30% chance waiting process completes I/O (As per your 2nd code)
            if (waiting.length > 0 && Math.random() < 0.3) {
                ready.push(waiting.shift());
            }

            // 3. Pick process if CPU is idle
            if (!running && ready.length > 0) {
                if (algo === "SJF") {
                    ready.sort((a, b) => a.remainingTime - b.remainingTime);
                } else if (algo === "priority") {
                    ready.sort((a, b) => a.priority - b.priority);
                }
                running = ready.shift();
                
                if (running.startTime === null) running.startTime = this.time;
            }

            // UI Update (onTick)
            onTick({ time: this.time, ready, running, waiting, terminated });
            await new Promise(r => setTimeout(r, 600)); // Visualization delay

            // 4. Execution Step
            if (running) {
                let execTime = (algo === "rr") ? Math.min(quantum, running.remainingTime) : 1;
                
                // Add to Gantt History
                this.history.push({ 
                    pid: running.pid, 
                    startTime: this.time, 
                    endTime: this.time + execTime, 
                    isIdle: false 
                });

                running.remainingTime -= execTime;
                this.time += execTime;

                // Next State Decisions (From your code logic)
                if (running.remainingTime > 0) {
                    // 20% chance for I/O (Simulating OS behavior)
                    if (Math.random() < 0.2) {
                        waiting.push(running);
                        running = null;
                    } else if (algo === "rr") {
                        // RR logic: Quantum expired, back to ready
                        ready.push(running);
                        running = null;
                    }
                } else {
                    // Terminated
                    running.completionTime = this.time;
                    terminated.push(running);
                    running = null;
                }
            } else {
                // CPU is Idle
                this.history.push({ pid: 'Idle', startTime: this.time, endTime: this.time + 1, isIdle: true });
                this.time += 1;
            }
        }
        // Final UI refresh
        onTick({ time: this.time, ready, running, waiting, terminated });
    }

    getFinalMetrics() {
        const n = this.processes.length;
        let totalWT = 0, totalTAT = 0;
        this.processes.forEach(p => {
            const tat = p.completionTime - p.arrivalTime;
            const wt = Math.max(0, tat - p.burstTime);
            totalWT += wt;
            totalTAT += tat;
        });
        return {
            schedule: this.history,
            processes: this.processes,
            avgWT: n > 0 ? totalWT / n : 0,
            avgTAT: n > 0 ? totalTAT / n : 0
        };
    }
}
