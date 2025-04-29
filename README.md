InfraCraft 🚀

A lightweight Python-based job runner dashboard for developers.

🌟 Project Overview

InfraCraft is a developer-first tool that allows users to submit, run, and monitor Python scripts through a web dashboard. Built with Flask and Python threading, it simulates a simplified CI/CD system, making it perfect for understanding queue-based job handling, backend systems, and live dashboards.

🧰 Key Features

🔧 Submit Jobs: Choose scripts from a dynamic dropdown (auto-scanned from /jobs/).

⏳ Real-Time Queue: Monitor jobs in Queued, Running, Completed, or Failed states.

🔍 Live Logs: View each job's output or error with collapsible sections.

⏰ Timestamp & Duration: Track when jobs were submitted and how long they took.

🌐 Frontend Polished: Clean, custom UI with badges, icons, and dynamic job states.

🌐 Tech Stack

Backend: Python, Flask, threading, subprocess, queue.Queue

Frontend: HTML5, CSS3, Jinja2 Templates

📄 Getting Started

1. Clone the Repo

git clone https://github.com/your-username/infracraft.git
cd infracraft

2. Install Dependencies

pip install flask

3. Add Jobs

Create .py scripts inside the /jobs folder. Example:

# jobs/success_script.py
print("✅ Script ran successfully!")

4. Run the App

python dashboard.py

Visit: http://localhost:5000

📸 Screenshots




🌐 Deploy on Render

Push code to GitHub

Create a new Web Service at render.com

Set:

Environment: Python

Start command: python dashboard.py

Done! You now have a public InfraCraft dashboard.

🏆 What You'll Learn

Flask routing and full-stack templating

Job queuing with Python's queue.Queue

Thread-safe background processing

Dynamic UI rendering with Jinja2

Real-time job log capture and presentation