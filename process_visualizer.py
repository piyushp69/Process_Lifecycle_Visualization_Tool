import tkinter as tk
from tkinter import messagebox

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
        self.root.geometry("1100x700")
        self.root.configure(bg="#111827")

        self.process_count = 0
        self.ready = []
        self.terminated = []
        self.gantt = []
        self.time_quantum = 2

        self.running_process = None
        self.is_simulating = False

        self.create_ui()

    # UI setup
    def create_ui(self):
        header_frame = tk.Frame(self.root, bg="#1F2937", pady=15)
        header_frame.pack(fill="x", side="top")

        tk.Label(header_frame,
                 text="Process Lifecycle Visualization Tool",
                 font=("Segoe UI", 24, "bold"),
                 bg="#1F2937",
                 fg="#F9FAFB").pack()

        tk.Label(header_frame,
                 text=f"Round Robin Scheduling | Time Quantum: {self.time_quantum}",
                 font=("Segoe UI", 12),
                 bg="#1F2937",
                 fg="#9CA3AF").pack()

        control_frame = tk.Frame(self.root, bg="#111827")
        control_frame.pack(pady=25)

        tk.Label(control_frame,
                 text="Burst Time:",
                 font=("Segoe UI", 12, "bold"),
                 bg="#111827",
                 fg="#E5E7EB").grid(row=0, column=0, padx=(0, 10))

        self.entry = tk.Entry(control_frame,
                              font=("Segoe UI", 14),
                              width=8,
                              justify="center",
                              bg="#374151",
                              fg="white",
                              insertbackground="white",
                              relief="flat")
        self.entry.grid(row=0, column=1, padx=10, ipady=5)

        self.create_btn = tk.Button(control_frame,
                               text="+ Add Process",
                               font=("Segoe UI", 11, "bold"),
                               bg="#10B981",
                               fg="white",
                               relief="flat",
                               width=15,
                               command=self.create_process)
        self.create_btn.grid(row=0, column=2, padx=10, ipady=3)

        self.start_btn = tk.Button(control_frame,
                              text="▶ Start Simulation",
                              font=("Segoe UI", 11, "bold"),
                              bg="#3B82F6",
                              fg="white",
                              relief="flat",
                              width=15,
                              command=self.start_simulation)
        self.start_btn.grid(row=0, column=3, padx=10, ipady=3)

        self.reset_btn = tk.Button(control_frame,
                              text="↺ Reset",
                              font=("Segoe UI", 11, "bold"),
                              bg="#6B7280",
                              fg="white",
                              relief="flat",
                              width=10,
                              command=self.reset_simulation)
        self.reset_btn.grid(row=0, column=4, padx=10, ipady=3)

        state_container = tk.Frame(self.root, bg="#111827")
        state_container.pack(pady=10)

        self.ready_frame = self.create_state_box(state_container, "Ready Queue", "#3B82F6")
        self.running_frame = self.create_state_box(state_container, "Running", "#F59E0B")
        self.terminated_frame = self.create_state_box(state_container, "Terminated", "#EF4444")

        self.cpu_status = tk.Label(self.root,
                                   text="CPU Status: Idle",
                                   font=("Segoe UI", 14, "bold"),
                                   bg="#111827",
                                   fg="#9CA3AF")
        self.cpu_status.pack(pady=(20, 5))

        gantt_container = tk.Frame(self.root, bg="#1F2937")
        gantt_container.pack(pady=10, fill="x", padx=50)

        tk.Label(gantt_container,
                 text="Gantt Chart Flow",
                 font=("Segoe UI", 14, "bold"),
                 bg="#1F2937",
                 fg="#E5E7EB").pack(pady=(10, 5))

        self.gantt_frame = tk.Frame(gantt_container, bg="#1F2937")
        self.gantt_frame.pack(pady=(0, 15))

    # Create state box
    def create_state_box(self, parent, title, color):
        frame = tk.Frame(parent, bg="#1F2937", bd=2, relief="groove", width=280, height=250)
        frame.pack(side="left", padx=15)
        frame.pack_propagate(False)

        tk.Label(frame,
                 text=title,
                 font=("Segoe UI", 14, "bold"),
                 bg="#1F2937",
                 fg=color).pack(pady=10)

        return frame

    # Add process
    def create_process(self):
        try:
            burst = int(self.entry.get())
            if burst <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid burst time")
            return

        self.process_count += 1
        self.ready.append(Process(f"P{self.process_count}", burst))

        self.entry.delete(0, tk.END)
        self.update_ui()

    # Update UI
    def update_ui(self):
        self.clear_box(self.ready_frame)
        self.clear_box(self.running_frame)
        self.clear_box(self.terminated_frame)

        for widget in self.gantt_frame.winfo_children():
            widget.destroy()

        for p in self.ready:
            tk.Label(self.ready_frame,
                     text=f"{p.pid} ({p.remaining})",
                     bg="#2563EB",
                     fg="white").pack(pady=4)

        if self.running_process:
            tk.Label(self.running_frame,
                     text=f"{self.running_process.pid} ({self.running_process.remaining})",
                     bg="#F59E0B").pack(pady=40)

        for p in self.terminated:
            tk.Label(self.terminated_frame,
                     text=p.pid,
                     bg="#DC2626",
                     fg="white").pack(pady=4)

        for i, pid in enumerate(self.gantt):
            if i > 0:
                tk.Label(self.gantt_frame, text="➔", bg="#1F2937").pack(side="left", padx=5)

            tk.Label(self.gantt_frame,
                     text=pid,
                     bg="#8B5CF6",
                     fg="white",
                     width=5).pack(side="left", padx=2)

    # Clear UI box
    def clear_box(self, frame):
        for widget in frame.winfo_children()[1:]:
            widget.destroy()

    # Reset simulation
    def reset_simulation(self):
        self.is_simulating = False
        self.process_count = 0
        self.ready.clear()
        self.terminated.clear()
        self.gantt.clear()
        self.running_process = None

        self.cpu_status.config(text="CPU Status: Idle")
        self.entry.delete(0, tk.END)

        self.create_btn.config(state="normal")
        self.start_btn.config(state="normal")

        self.update_ui()

    # Start simulation
    def start_simulation(self):
        if not self.ready:
            messagebox.showerror("Error", "No processes")
            return

        self.is_simulating = True
        self.create_btn.config(state="disabled")
        self.start_btn.config(state="disabled")

        self.simulate_step()

    # Execute one step
    def simulate_step(self):
        if not self.is_simulating:
            return

        if not self.ready:
            self.running_process = None
            self.cpu_status.config(text="CPU Status: Idle")
            self.update_ui()
            self.is_simulating = False
            self.create_btn.config(state="normal")
            self.start_btn.config(state="normal")
            messagebox.showinfo("Done", "All processes finished")
            return

        self.running_process = self.ready.pop(0)
        self.cpu_status.config(text=f"Running: {self.running_process.pid}")
        self.update_ui()

        self.root.after(1000, self.finish_step)

    # Finish execution step
    def finish_step(self):
        if not self.is_simulating:
            return

        p = self.running_process
        exec_time = min(self.time_quantum, p.remaining)

        self.gantt.append(p.pid)
        p.remaining -= exec_time

        if p.remaining > 0:
            self.ready.append(p)
        else:
            self.terminated.append(p)

        self.running_process = None
        self.update_ui()

        self.root.after(500, self.simulate_step)

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessVisualizer(root)
    root.mainloop()
