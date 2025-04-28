from flask import Flask, request, redirect, render_template, url_for
from producer import job_queue, consumer, result_list, stop_signal
import threading
import time

app = Flask(__name__, template_folder='web_dashboard/templates', static_folder='web_dashboard/static')

# keep track of job id
job_id = 1

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/live_job')
def live_job():
    return render_template('live_job.html')

@app.route('/status')
def status():
    return render_template('status.html')


@app.route('/submit', methods=["POST"])
def submit():
    global job_id
    command = request.form.get('command')
    if not command.strip():
        return redirect('/')
    else:
        submission = {
                        "jobId": job_id,
                        "job": command, 
                        "submission_time": time.time(), 
                        "status": "Queued"
                        }
        job_queue.put(submission)
        job_id += 1
        return redirect('/')
    

if __name__ == "__main__":
    t1 = threading.Thread(target=consumer)
    t1.daemon = True
    t1.start()
    app.run(debug=True)