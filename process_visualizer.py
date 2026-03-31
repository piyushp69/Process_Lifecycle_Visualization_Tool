import tkinter as tk
from tkinter import messagebox
import random

# Process model
class Process:
    def __init__(self, pid, burst):
        self.pid = pid
        self.burst = burst
        self.remaining = burst

# Main app
class ProcessVisualizer:

    def __init__(self, root):
        self.root = root
        self.root.title("Process Lifecycle Visualization Tool")
        self.root.geometry("1200x750")
        self.root.configure(bg="#111827") 

        # state data
        self.process_count = 0
        self.ready = []
        self.waiting = []
        self.terminated = []
        self.time_quantum = 2
        
        self.running_process = None 
        self.prev_process = None
        self.is_simulating = False

        self.create_ui()

    # UI setup
    def create_ui(self):
        header = tk.Frame(self.root, bg="#1F2937", pady=15)
        header.pack(fill="x")

        tk.Label(header, text="Process Lifecycle Visualization Tool",
                 font=("Segoe UI", 24, "bold"),
                 bg="#1F2937", fg="#F9FAFB").pack()

        tk.Label(header,
                 text=f"Round Robin | Time Quantum: {self.time_quantum}",
                 font=("Segoe UI", 12),
                 bg="#1F2937", fg="#9CA3AF").pack()

        control = tk.Frame(self.root, bg="#111827")
        control.pack(pady=20)

        tk.Label(control, text="Burst Time:",
                 bg="#111827", fg="white").grid(row=0, column=0)

        self.entry = tk.Entry(control, width=10)
        self.entry.grid(row=0, column=1, padx=10)

        tk.Button(control, text="+ Add", command=self.create_process)\
            .grid(row=0, column=2, padx=10)

        tk.Button(control, text="▶ Start", command=self.start_simulation)\
            .grid(row=0, column=3, padx=10)

        tk.Button(control, text="↺ Reset", command=self.reset_simulation)\
            .grid(row=0, column=4, padx=10)

        # context switch info
        self.context_label = tk.Label(self.root, text="",
                                     font=("Segoe UI", 12, "bold"),
                                     bg="#111827", fg="#F87171")
        self.context_label.pack()

        container = tk.Frame(self.root, bg="#111827")
        container.pack()

        self.ready_frame = self.create_box(container, "Ready", "#3B82F6")
        self.running_frame = self.create_box(container, "Running", "#F59E0B")
        self.waiting_frame = self.create_box(container, "Waiting", "#8B5CF6")
        self.terminated_frame = self.create_box(container, "Terminated", "#EF4444")

        self.cpu_status = tk.Label(self.root, text="CPU Idle",
                                  bg="#111827", fg="white")
        self.cpu_status.pack(pady=10)

    # state box
    def create_box(self, parent, title, color):
        frame = tk.Frame(parent, bg="#1F2937", width=200, height=200)
        frame.pack(side="left", padx=10)
        frame.pack_propagate(False)

        tk.Label(frame, text=title,
                 bg="#1F2937", fg=color,
                 font=("Segoe UI", 12, "bold")).pack()
        return frame

    # add process
    def create_process(self):
        try:
            burst = int(self.entry.get())
            if burst <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid burst time")
            return

        self.process_count += 1
        self.ready.append(Process(f"P{self.process_count}", burst))

        self.entry.delete(0, tk.END)
        self.update_ui()

    # refresh UI
    def update_ui(self):
        self.clear(self.ready_frame)
        self.clear(self.running_frame)
        self.clear(self.waiting_frame)
        self.clear(self.terminated_frame)

        for p in self.ready:
            tk.Label(self.ready_frame, text=p.pid,
                     bg="blue", fg="white").pack()

        if self.running_process:
            tk.Label(self.running_frame, text=self.running_process.pid,
                     bg="orange").pack()

        for p in self.waiting:
            tk.Label(self.waiting_frame, text=p.pid,
                     bg="purple", fg="white").pack()

        for p in self.terminated:
            tk.Label(self.terminated_frame, text=p.pid,
                     bg="red", fg="white").pack()

    # clear box
    def clear(self, frame):
        for w in frame.winfo_children()[1:]:
            w.destroy()

    # reset
    def reset_simulation(self):
        self.ready.clear()
        self.waiting.clear()
        self.terminated.clear()
        self.running_process = None
        self.prev_process = None
        self.is_simulating = False

        self.context_label.config(text="")
        self.cpu_status.config(text="CPU Idle")

        self.update_ui()

    # start
    def start_simulation(self):
        if not self.ready:
            messagebox.showerror("Error", "No process")
            return

        self.is_simulating = True
        self.simulate()

    # scheduling loop
    def simulate(self):
        if not self.is_simulating:
            return

        if self.waiting and random.random() < 0.5:
            self.ready.append(self.waiting.pop(0))

        if not self.ready:
            self.running_process = None
            self.update_ui()
            return

        self.running_process = self.ready.pop(0)

        if self.prev_process:
            self.context_label.config(
                text=f"Context Switch: {self.prev_process.pid} → {self.running_process.pid}"
            )

        self.prev_process = self.running_process

        self.cpu_status.config(text=f"Running: {self.running_process.pid}")
        self.update_ui()

        self.root.after(1000, self.execute)

    # execution step
    def execute(self):
        p = self.running_process
        exec_time = min(self.time_quantum, p.remaining)
        p.remaining -= exec_time

        if p.remaining > 0 and random.random() < 0.3:
            self.waiting.append(p)
        elif p.remaining > 0:
            self.ready.append(p)
        else:
            self.terminated.append(p)

        self.running_process = None
        self.update_ui()

        self.root.after(800, self.simulate)


# run app
if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessVisualizer(root)
    root.mainloop()
