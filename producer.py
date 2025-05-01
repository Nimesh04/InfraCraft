from job_queue import job_queue 
import subprocess
import threading
import time
from datetime import datetime
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
                    print("Exiting the program.")
                    stop_signal = True
                    break
            elif command.lower() == "chaos":
                print("🔥 Launching Mega Chaos Mode!")
                mega_chaos_submitter()  # (optional) pass job_id if you want chaos jobs to have unique IDs
                auto_mode = True
            else:
                now = datetime.now()
                readable_time = now.strftime("%I:%M%p")
                submission = {
                    "jobId": job_id,
                    "command": command, 
                    "submission_time": time.time(), 
                    "submitted_at": readable_time,
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
        if stop_signal:
            break
        try:
            if not job_queue.empty():
                job = job_queue.get()
                job["status"] = "Running"
                print(f"▶️ Job {job['jobId']} is now running...")

                try:
                    # Handle Python script execution specially to ensure proper termination
                    if job["command"].startswith("python ") or job["command"].endswith(".py"):
                        print(f"📝 Detected Python script execution: {job['command']}")
                        # On Windows, use the taskkill command to ensure we can kill the Python process and its children
                        
                        # Start the process
                        process = subprocess.Popen(
                            job["command"],
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0
                        )
                        
                        process_id = process.pid
                        print(f"🆔 Process started with PID: {process_id}")
                    else:
                        # For non-Python commands
                        process = subprocess.Popen(
                            job["command"],
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                    
                    # Set up a buffer for incremental output collection
                    stdout_buffer = []
                    stderr_buffer = []
                    
                    def read_output(process):
                        """Read output incrementally to avoid buffer issues"""
                        while process.poll() is None:
                            # Read output line by line if available
                            stdout_line = process.stdout.readline()
                            if stdout_line:
                                stdout_buffer.append(stdout_line)
                                print(f"📤 Job {job['jobId']} output: {stdout_line.strip()}")
                            
                            stderr_line = process.stderr.readline()
                            if stderr_line:
                                stderr_buffer.append(stderr_line)
                                print(f"⚠️ Job {job['jobId']} error: {stderr_line.strip()}")
                            
                            # Short sleep to prevent CPU hogging
                            time.sleep(0.1)
                    
                    # Start a thread to read output incrementally
                    output_thread = threading.Thread(target=read_output, args=(process,))
                    output_thread.daemon = True
                    output_thread.start()
                    
                    # Wait for the process to complete with timeout
                    try:
                        returncode = process.wait(timeout=5)
                        # Join the output thread with a timeout
                        output_thread.join(1.0)
                        
                        # Get any remaining output
                        remaining_stdout, remaining_stderr = process.communicate()
                        if remaining_stdout:
                            stdout_buffer.append(remaining_stdout)
                        if remaining_stderr:
                            stderr_buffer.append(remaining_stderr)
                        
                        stdout = "".join(stdout_buffer) 
                        stderr = "".join(stderr_buffer)
                        status = "Completed" if returncode == 0 else "Failed"
                        print(f"✅ Job {job['jobId']} finished with status: {status}")
                    except subprocess.TimeoutExpired:
                        print(f"⏱️ Job {job['jobId']} timed out after 10 seconds, terminating...")
                        
                        # Force kill the process - this is especially important for Windows
                        try:
                            if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') and job["command"].startswith("python "):
                                # Windows-specific handling for Python scripts
                                kill_cmd = f"taskkill /F /T /PID {process.pid}"
                                print(f"🔫 Executing: {kill_cmd}")
                                subprocess.run(kill_cmd, shell=True)
                            else:
                                # Standard kill for other platforms/processes
                                process.kill()
                            
                            # Collect any output that was generated before killing
                            try:
                                remaining_stdout, remaining_stderr = process.communicate(timeout=2)
                                if remaining_stdout:
                                    stdout_buffer.append(remaining_stdout)
                                if remaining_stderr:
                                    stderr_buffer.append(remaining_stderr)
                            except subprocess.TimeoutExpired:
                                # If communicate times out again, force terminate
                                process.terminate()
                                try:
                                    process.communicate(timeout=1)
                                except:
                                    pass
                            
                            stdout = "".join(stdout_buffer)
                            stderr = "".join(stderr_buffer)
                        except Exception as kill_error:
                            print(f"⚠️ Error killing process: {kill_error}")
                            stdout = "".join(stdout_buffer)
                            stderr = "".join(stderr_buffer) + f"\nError killing process: {kill_error}"
                        
                        returncode = 1
                        status = "Timeout"
                        print(f"⏱️ Job {job['jobId']} timed out and was killed.")
                        
                except Exception as e:
                    print(f"❌ Error executing job: {e}")
                    stdout = "".join(stdout_buffer) if 'stdout_buffer' in locals() else ""
                    stderr = "".join(stderr_buffer) if 'stderr_buffer' in locals() else f"Exception during execution: {e}"
                    returncode = 1
                    status = "Error"

                completed_jobs += 1
                completion_time = time.time() - job["submission_time"]

                result_list.append({
                    "jobID": job["jobId"],
                    "command": job["command"],
                    "Completion_time": round(completion_time, 2),
                    "submitted_at": job["submitted_at"],
                    "result": returncode,
                    "output": stdout,
                    "error": stderr,
                    "status": status
                })
            else:
                time.sleep(1.0)
        except Exception as e:
            print(f"❌ Error in consumer: {e}")



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