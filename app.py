import os
import threading
import time
from flask import Flask, request, redirect, render_template, url_for
from producer import job_queue, consumer, result_list, stop_signal
from datetime import datetime

app = Flask(__name__, template_folder='web_dashboard/templates', static_folder='web_dashboard/static')

# keep track of job id
job_id = 1

@app.route("/")
def home():
    recent_jobs = list(result_list[-5:])

    jobs_folder = os.path.join(os.getcwd(),"jobs")
    scripts = sorted([
                    f"python jobs/{f}"
                    for f in os.listdir(jobs_folder)
                    if f.endswith(".py")
                     ])

    return render_template("home.html", recent_jobs=recent_jobs, script_options=scripts)

@app.route('/live_job')
def live_job():
    live_jobs = []

    temp_queue = list(job_queue.queue)
    for job in temp_queue:
        if job['status'] == "Queued":
            live_jobs.append(job)
    return render_template('live_job.html', live_jobs=live_jobs)

@app.route('/status')
def status():
    all_jobs = list(result_list)
    return render_template('status.html', all_jobs=all_jobs)


@app.route('/submit', methods=["POST"])
def submit():
    global job_id
    command = request.form.get('command')
    user_time = request.form.get('local_time') 

    if not command.strip():
        return redirect('/')
    else:
        submission = {
            "jobId": job_id,
            "command": command, 
            "submission_time": time.time(),
            "submitted_at": user_time,   
            "status": "Queued"
        }
        job_id += 1
        job_queue.put(submission)
        return redirect('/')

@app.route('/api/recent_jobs')
def api_recent_jobs():
    recent_jobs = list(result_list[-5:])  # or however many you want
    return render_template('recent_jobs_partial.html', recent_jobs=recent_jobs)

    

if __name__ == "__main__":
    t1 = threading.Thread(target=consumer)
    t1.daemon = True
    t1.start()
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True)