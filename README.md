# InfraCraft 🔧

InfraCraft is a lightweight, modular, and expandable **distributed job runner** built from scratch. 

Think of it as your personal mini-infrastructure system: it queues tasks, distributes them to background workers, executes them, captures the results, and gives you a sweet battle report at the end.

Built in pure Python with real-world engineering principles. 
InfraCraft v0.2 is our next evolution: better reliability, better reporting, future-ready for scaling.

---

# 🔄 Why InfraCraft?

Big companies (Tesla, Google, etc.) have huge internal systems to build, test, and deploy code fast. 
InfraCraft is a scrappy, hacker-friendly simulation of those systems that you can actually understand, extend, and show off.

---

# 📉 Current Features (v0.1)

- Multithreaded Producer/Consumer model using Python `threading`
- CLI-based shell command and script runner
- Captures success, failure, output, and error logs
- Graceful shutdown with user-triggered exit
- Simple in-memory queue (Python `queue.Queue`)
- No external dependencies (pure Python)

---

# 🎉 What's Coming (v0.2)

- Drain the job queue completely before shutting down
- Timestamp jobs for accurate tracking
- Improve output reporting (success/failure clearly formatted)
- Catch subprocess crashes gracefully (with try/except)
- Add a professional shutdown summary report
- Introduce Job IDs for better result tracking

---

# 🌐 Future Roadmap (v0.3+)

- Build a Flask-based web dashboard to submit/view jobs
- Integrate Redis for multi-machine distributed queuing
- Enable remote job submissions via API
- Dockerize InfraCraft for easy deployment

This ain't just another CLI toy. It's your launchpad to real-world dev infrastructure. 

---

# 📅 Project Timeline

| Version | Goals |
|---------|------|
| v0.1    | Basic CLI-based task runner (Completed) |
| v0.2    | Stability, polish, graceful UX improvements |
| v0.3    | Web dashboard + distributed scaling features |

---

# 🔧 How It Works (Bird's Eye)

1. **Producer** - Takes user input for jobs (shell commands)
2. **Consumer** - Background worker that continuously pulls and runs jobs
3. **Result Storage** - Records command, output, error, timestamp, and status
4. **Graceful Exit** - Ensures all jobs are completed before system shuts down
5. **Result Reporting** - Clean job execution report after exit

---

# 🚀 Setup Instructions

1. Clone the repo
2. Make sure you have Python 3.10+
3. Run the main script:

```bash
python infracraft.py
```

4. Enter jobs like:

```bash
python jobs/success_script.py
python jobs/crash_script.py
```

5. Type `exist` to exit and see the full result report

---

# 🎉 Wanna Help?

- Fork it, tweak it, break it, improve it.
- Open PRs for better result handling, dashboard features, Redis integration.
- InfraCraft is meant to grow and evolve with contributors.

Let's build real-world systems together.

---

# 🔗 License

Hack it, build it, ship it.

---

# 🌟 Credits

Built from scratch, fueled by caffeine, ambition, and the stubborn belief that dev infrastructure should be fun to learn.

---

InfraCraft is just getting started. Let's make it legendary.

