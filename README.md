🖥️ Process Lifecycle Visualization Pro
A high-fidelity, interactive web application designed to visualize CPU Scheduling Algorithms and the Process Lifecycle. This tool simulates how an Operating System manages processes through various states: Ready, Running, I/O Wait, and Terminated.

🚀 Features
Real-Time Lifecycle Simulation: Watch processes move dynamically between states based on real OS behavior.

Multiple Scheduling Algorithms:

FCFS (First Come First Served)

SJF (Shortest Job First - Non-preemptive)

Round Robin (with customizable Time Quantum)

Priority Scheduling (Non-preemptive)

Dynamic I/O Simulation: Randomly simulates processes entering an I/O Wait state and returning to the Ready Queue, mimicking real-world system interruptions.

Detailed Analytics:

Interactive Gantt Chart: A visual timeline of CPU execution and idle periods.

Process Metrics Table: Detailed breakdown of Arrival, Burst, Exit, Turnaround (TAT), and Waiting Times (WT).

Performance Summary: Automated calculation of Average Waiting and Turnaround times.

Responsive UI/UX: Modern dark-themed interface built with a focus on scannability and professional aesthetics.

🛠️ Built With
HTML5/CSS3: Custom layouts using CSS Grid and Flexbox for a responsive experience.

JavaScript (ES6+): Custom-built scheduler engine using asynchronous logic for smooth animations.

FontAwesome: For professional iconography.

Google Fonts: Utilizing 'Inter' and 'JetBrains Mono' for high readability.

📂 Project Structure
Plaintext
├── index.html      # The main UI structure
├── styles.css      # Custom styling and animations
├── app.js          # UI Logic, Event Listeners, and Live UI updates
├── scheduler.js    # Core Scheduling Algorithms and State Management
└── README.md       # Project documentation
📖 How to Use
Add Processes: Enter a Process ID, Arrival Time, and Burst Time in the input panel.

Select Algorithm: Choose a scheduling method from the control grid.

Note: If you select Round Robin, you can specify the Time Quantum.

Run Simulation: Click "Run Simulation" to watch the process lifecycle in real-time.

Analyze Results: Once finished, scroll down to view the Gantt chart and statistical performance metrics.

🏁 Installation & Deployment
Since this is a static web application, no complex installation is required.

Clone the Repository:

Bash
git clone https://github.com/piyushp69/process-visualizer.git
Open the Project: Open index.html in any modern web browser.

Deploy: Easily deployable via GitHub Pages, Vercel, or Netlify.
