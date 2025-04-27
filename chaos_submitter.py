# chaos_submitter.py
import time
from job_queue import job_queue 

def mega_chaos_submitter():
    jobs_to_submit = [
        "python jobs/long_running_job.py",
        "python jobs/random_script.py",
        "python jobs/output_flood.py",
        "python jobs/unicode_bomb.py",
        "python jobs/crash_script.py",
        "python jobs/random_script.py",
        "python jobs/long_running_job.py",
        "python jobs/output_flood.py",
        "python jobs/unicode_bomb.py",
        "python jobs/crash_script.py"
    ]

    job_id = 1000  # start at 1000 so you can tell chaos jobs apart

    for command in jobs_to_submit:
        submission = {
            "jobId": job_id,
            "job": command,
            "submission_time": time.time()
        }
        job_queue.put(submission)
        print(f"🚀 Submitted chaotic job #{job_id}: {command}")
        job_id += 1
        time.sleep(0.5)  # tiny delay between submits for realism

