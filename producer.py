from job_queue import job_queue 
import subprocess
import threading
import time
from chaos_submitter import mega_chaos_submitter

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
                submission = {"jobId": job_id, "job": command, "submission_time": time.time()}
                job_queue.put(submission)
                print(f"✅ Job added successfully!")
                job_id += 1
        except Exception as e:
            print( f"Error: {e}")
            continue


def consumer():
    while True:
        if stop_signal == True:
            break
        try:
            if(job_queue.empty() != True):
                job = job_queue.get()
                result = subprocess.run(job["job"], shell=True, capture_output=True, text=True)
                completion_time = time.time() - job["submission_time"]
                result_list.append({"jobID": job["jobId"],"command": result.args, "Completion_time": round(completion_time, 2) ,"result":result.returncode, "output": result.stdout, "error": result.stderr})
            else:
                time.sleep(1.0)
        except Exception as e:
            print( f"Error: {e}")



if __name__ == "__main__":
    result_list = []
    stop_signal = False
    t1 = threading.Thread(target= consumer)
    t1.start()
    producer()
    t1.join()

    job_submission = 0
    successful_job = 0
    failed_job = 0

    for result in result_list:
        job_submission += 1
        if result["result"] == 0:
            successful_job += 1
            print(f"✅ Job ID: {result['jobID']} | Completion Time: {result['Completion_time']} | Command: {result['command']} | Status: Success | Output: {result['output']}")

        else:
            failed_job += 1
            print(f"❌ Job ID: {result['jobID']} | Completion Time: {result['Completion_time']} | Command: {result['command']} | Status: Failed | Output:{result['output']} | Error: {result['error']}")

    print("\n \n ")
    print("🚀 InfraCraft Run Summary ")
    print(f"Total Jobs Submitted: {job_submission} \nTotal Jobs Completed: {job_submission} \nSuccessful: {successful_job} \nFailed: {failed_job}")
    print("See detailed results above. \nThank you for using InfraCraft!")