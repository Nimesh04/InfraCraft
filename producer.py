from job_queue import job_queue 
import subprocess
import threading
import time
from chaos_submitter import mega_chaos_submitter

result_list = []
stop_signal = False
completed_jobs  = 0
job_submission = 0
successful_job = 0
failed_job = 0

def producer():
    global stop_signal
    job_id = 1
    auto_mode = False
    while True:
        try:
            if auto_mode:
                if(job_queue.empty()):
                    stop_signal = True
                    break
                else:
                    time.sleep(1)
                    continue
            command = input("Enter your command/type \'exist\': ")
            if(command.lower() == "exist"):
                if(job_queue.empty() == True):
                    print("Existing the program.")
                    stop_signal = True
                    break
            elif command.lower() == "chaos":
                print("🔥 Launching Mega Chaos Mode!")
                mega_chaos_submitter()  # (optional) pass job_id if you want chaos jobs to have unique IDs
                auto_mode = True
            else:
                submission = {
                    "jobId": job_id,
                    "command": command, 
                    "submission_time": time.time(), 
                    "status": "Queued"
                    }
                
                job_queue.put(submission)
                print(f"✅ Job added successfully!")
                job_id += 1
        except Exception as e:
            print( f"Error: {e}")
            continue


def consumer():
    global completed_jobs
    while True:
        if stop_signal == True:
            break
        try:
            if(job_queue.empty() != True):
                job = job_queue.get()
                job["status"] = "Running"
                print(f"\nJob {job['jobId']} is now {job['status']}")
                result = subprocess.run(job["command"], shell=True, capture_output=True, text=True)
                if(result.returncode == 0):
                    job["status"] = "Completed"
                else:
                    job["status"] = "Failed"
                completed_jobs += 1
                completion_time = time.time() - job["submission_time"]
                result_list.append({"jobID": job["jobId"],
                                    "command": result.args, 
                                    "Completion_time": round(completion_time, 2) ,
                                    "submitted_at": job["submitted_at"],
                                    "result":result.returncode, 
                                    "output": result.stdout, 
                                    "error": result.stderr,
                                    "status": job["status"]
                                    })
            else:
                time.sleep(1.0)
        except Exception as e:
            print( f"Error: {e}")



if __name__ == "__main__":
    t1 = threading.Thread(target= consumer)
    t1.start()
    producer()
    t1.join()

    for result in result_list:
        job_submission += 1
        if result["result"] == 0:
            successful_job += 1
            print(f"✅ Job ID: {result['jobID']} | Completion Time: {result['Completion_time']} | Command: {result['command']} | Status: {result['status']} | Output: {result['output']}")

        else:
            failed_job += 1
            print(f"❌ Job ID: {result['jobID']} | Completion Time: {result['Completion_time']} | Command: {result['command']} | Status: {result['status']} | Output:{result['output']} | Error: {result['error']}")

    print("\n \n ")
    print("🚀 InfraCraft Run Summary ")
    print(f"Total Jobs Submitted: {job_submission} \nTotal Jobs Completed: {completed_jobs} \nSuccessful: {successful_job} \nFailed: {failed_job}")
    print("See detailed results above. \nThank you for using InfraCraft!")