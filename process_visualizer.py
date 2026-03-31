import tkinter as tk
from tkinter import messagebox
import random

# Process Class
class Process:
    def __init__(self, pid, burst, arrival):
        self.pid = pid
        self.burst = burst
        self.remaining = burst
        self.arrival = arrival
        self.start_time = None
        self.completion_time = None

# Main Application
class ProcessVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Lifecycle Visualization Tool")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0F172A") # Deeper Dark Blue Theme

        # Core Variables
        self.process_count = 0
        self.ready = []
        self.waiting = []
        self.terminated = []
        self.unarrived = [] # Track processes that haven't arrived yet

        self.time = 0
        self.idle_time = 0
        self.time_quantum = 2

        self.running_process = None
        self.prev_process = None
        self.is_simulating = False
        self.is_paused = False

        self.algorithm = tk.StringVar(value="RR")

        self.create_ui()

    # --- UI Setup ---
    def create_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1E293B", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Process Scheduling Visualizer", font=("Segoe UI", 24, "bold"), bg="#1E293B", fg="#38BDF8").pack()

        # Control Panel
        control = tk.Frame(self.root, bg="#0F172A")
        control.pack(pady=20)

        # Inputs
        tk.Label(control, text="Burst Time:", bg="#0F172A", fg="#94A3B8", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5)
        self.burst_entry = tk.Entry(control, width=8, font=("Segoe UI", 11), bg="#334155", fg="white", relief="flat", insertbackground="white")
        self.burst_entry.grid(row=0, column=1, padx=5)

        tk.Label(control, text="Arrival Time:", bg="#0F172A", fg="#94A3B8", font=("Segoe UI", 11)).grid(row=0, column=2, padx=5)
        self.arrival_entry = tk.Entry(control, width=8, font=("Segoe UI", 11), bg="#334155", fg="white", relief="flat", insertbackground="white")
        self.arrival_entry.grid(row=0, column=3, padx=5)

        tk.Label(control, text="Algorithm:", bg="#0F172A", fg="#94A3B8", font=("Segoe UI", 11)).grid(row=0, column=4, padx=5)
        algo_menu = tk.OptionMenu(control, self.algorithm, "FCFS", "SJF", "RR")
        algo_menu.config(bg="#334155", fg="white", activebackground="#475569", relief="flat", font=("Segoe UI", 10))
        algo_menu.grid(row=0, column=5, padx=10)

        # Buttons
        btn_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white", "relief": "flat", "padx": 10, "pady": 4, "cursor": "hand2"}
        tk.Button(control, text="+ Add Process", bg="#10B981", activebackground="#059669", command=self.create_process, **btn_style).grid(row=0, column=6, padx=5)
        tk.Button(control, text="▶ Start", bg="#3B82F6", activebackground="#2563EB", command=self.start_simulation, **btn_style).grid(row=0, column=7, padx=5)
        tk.Button(control, text="⏸ Pause", bg="#F59E0B", activebackground="#D97706", command=self.pause, **btn_style).grid(row=0, column=8, padx=5)
        tk.Button(control, text="▶ Resume", bg="#8B5CF6", activebackground="#7C3AED", command=self.resume, **btn_style).grid(row=0, column=9, padx=5)
        tk.Button(control, text="↺ Reset", bg="#EF4444", activebackground="#DC2626", command=self.reset_simulation, **btn_style).grid(row=0, column=10, padx=5)

        # Status Bar (Time & Context)
        status_frame = tk.Frame(self.root, bg="#0F172A")
        status_frame.pack(fill="x", pady=10)
        
        self.time_label = tk.Label(status_frame, text="Global Time: 0s", font=("Consolas", 14, "bold"), bg="#0F172A", fg="#E2E8F0")
        self.time_label.pack(side="left", padx=50)
        
        self.cpu_status = tk.Label(status_frame, text="CPU is Idle", font=("Consolas", 14, "bold"), bg="#0F172A", fg="#FBBF24")
        self.cpu_status.pack(side="right", padx=50)

        # Visualization Containers
        container = tk.Frame(self.root, bg="#0F172A")
        container.pack(pady=10)

        self.ready_frame = self.create_box(container, "Ready Queue", "#3B82F6", "#EFF6FF")
        self.running_frame = self.create_box(container, "Running (CPU)", "#F59E0B", "#FEF3C7")
        self.waiting_frame = self.create_box(container, "I/O Waiting", "#8B5CF6", "#F5F3FF")
        self.terminated_frame = self.create_box(container, "Terminated", "#EF4444", "#FEF2F2")

        # Metrics
        self.metrics_label = tk.Label(self.root, text="", font=("Segoe UI", 12), bg="#0F172A", fg="#34D399")
        self.metrics_label.pack(pady=20)

    def create_box(self, parent, title, bg_color, fg_color):
        frame = tk.Frame(parent, bg="#1E293B", width=250, height=350, highlightbackground=bg_color, highlightthickness=2)
        frame.pack(side="left", padx=15)
        frame.pack_propagate(False) # Keep fixed size
        tk.Label(frame, text=title, bg=bg_color, fg=fg_color, font=("Segoe UI", 12, "bold"), pady=8).pack(fill="x")
        return frame

    # --- Core Logic ---
    def create_process(self):
        try:
            burst = int(self.burst_entry.get())
            arrival = int(self.arrival_entry.get())
            if burst <= 0 or arrival < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive integers for Burst and Arrival.")
            return

        self.process_count += 1
        new_process = Process(f"P{self.process_count}", burst, arrival)
        self.unarrived.append(new_process)

        self.burst_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"{new_process.pid} added! (Arrival: {arrival}, Burst: {burst})")

    def create_process_card(self, frame, process, bg_color):
        # Creates a nice visual card for the process
        card_text = f"{process.pid} ({process.remaining}s left)"
        if process.remaining == 0:
            card_text = f"{process.pid} (Done)"
            
        lbl = tk.Label(frame, text=card_text, bg=bg_color, fg="white", font=("Consolas", 11, "bold"), pady=5, padx=10, relief="flat")
        lbl.pack(pady=5, padx=10, fill="x")

    def update_ui(self):
        # Clear existing visual blocks
        for f in [self.ready_frame, self.running_frame, self.waiting_frame, self.terminated_frame]:
            for w in f.winfo_children()[1:]: # Skip the title label
                w.destroy()

        self.time_label.config(text=f"Global Time: {self.time}s")

        # Re-draw process cards
        for p in self.ready:
            self.create_process_card(self.ready_frame, p, "#2563EB") # Blue

        if self.running_process:
            self.create_process_card(self.running_frame, self.running_process, "#D97706") # Orange

        for p in self.waiting:
            self.create_process_card(self.waiting_frame, p, "#7C3AED") # Purple

        for p in self.terminated:
            self.create_process_card(self.terminated_frame, p, "#DC2626") # Red

    def pause(self):
        self.is_paused = True

    def resume(self):
        if self.is_simulating and self.is_paused:
            self.is_paused = False
            self.simulate()

    def reset_simulation(self):
        self.ready.clear()
        self.waiting.clear()
        self.terminated.clear()
        self.unarrived.clear()

        self.process_count = 0
        self.time = 0
        self.idle_time = 0

        self.running_process = None
        self.prev_process = None
        self.is_simulating = False
        self.is_paused = False

        self.cpu_status.config(text="CPU is Idle", fg="#FBBF24")
        self.metrics_label.config(text="")
        self.update_ui()

    def start_simulation(self):
        if not self.unarrived and not self.ready and not self.waiting:
            messagebox.showerror("Error", "No processes added to simulate!")
            return

        self.is_simulating = True
        self.is_paused = False
        self.metrics_label.config(text="")
        self.simulate()

    def pick_process(self):
        if self.algorithm.get() == "SJF":
            self.ready.sort(key=lambda x: x.remaining)
        return self.ready.pop(0)

    def simulate(self):
        if not self.is_simulating or self.is_paused:
            return

        # Check for new arrivals (Fixed logic to <= to catch skipped times)
        arrived_now = [p for p in self.unarrived if p.arrival <= self.time]
        for p in arrived_now:
            self.ready.append(p)
            self.unarrived.remove(p)

        # 30% chance a waiting process completes I/O
        if self.waiting and random.random() < 0.3:
            self.ready.append(self.waiting.pop(0))

        if not self.ready and not self.running_process:
            if not self.unarrived and not self.waiting:
                self.show_metrics()
                self.is_simulating = False
                return
            
            # CPU is idle waiting for processes
            self.cpu_status.config(text="Idle...", fg="#94A3B8")
            self.idle_time += 1
            self.time += 1
            self.update_ui()
            self.root.after(800, self.simulate)
            return

        # Load process to CPU
        if not self.running_process and self.ready:
            self.running_process = self.pick_process()
            
            if self.running_process.start_time is None:
                self.running_process.start_time = self.time

            self.cpu_status.config(text=f"Executing {self.running_process.pid}", fg="#34D399")
            self.update_ui()
            self.root.after(800, self.execute)
        else:
            # If a process is running, just execute it
            self.execute()

    def execute(self):
        if self.is_paused:
            return

        p = self.running_process
        if not p:
            self.simulate()
            return

        # Determine execution time slice
        if self.algorithm.get() == "RR":
            exec_time = min(self.time_quantum, p.remaining)
        else:
            exec_time = 1 # Step by 1 for FCFS/SJF visualization smoothness

        p.remaining -= exec_time
        self.time += exec_time

        # Update UI to show decreased time
        self.update_ui()

        # Decide next state
        if p.remaining > 0:
            # 20% chance to go for I/O waiting (Simulating real OS behavior)
            if random.random() < 0.2:
                self.waiting.append(p)
                self.running_process = None
            elif self.algorithm.get() == "RR" and exec_time == self.time_quantum:
                # Time quantum expired, back to ready queue
                self.ready.append(p)
                self.running_process = None
            else:
                # Keep running
                pass 
        else:
            # Process Finished
            p.completion_time = self.time
            self.terminated.append(p)
            self.running_process = None

        self.root.after(800, self.simulate)

    def show_metrics(self):
        total_wt = 0
        total_tat = 0
        n = len(self.terminated)

        if n == 0: return

        for p in self.terminated:
            tat = p.completion_time - p.arrival
            wt = tat - p.burst
            total_wt += wt
            total_tat += tat

        avg_wt = total_wt / n
        avg_tat = total_tat / n
        cpu_util = ((self.time - self.idle_time) / self.time) * 100 if self.time > 0 else 0

        self.metrics_label.config(
            text=f"📊 Simulation Complete | Avg Wait Time: {avg_wt:.2f}s | Avg Turnaround Time: {avg_tat:.2f}s | CPU Utilization: {cpu_util:.2f}%"
        )
        self.cpu_status.config(text="Simulation Finished", fg="#38BDF8")
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessVisualizer(root)
    root.mainloop()
