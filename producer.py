from job_queue import job_queue 
import subprocess
import threading
import time


def producer():
    while True:
        command = input("Enter your command/type \'exist\': ")
        if(command.lower() == "exist"):
            print("Existing the program.")
            global stop_signal
            stop_signal = True
            break
        else:
            job_queue.put(command)
            print(f"Job added successfully!")


def consumer():
    while True:
        if stop_signal == True:
            break

        if(job_queue.empty() != True):
          result = subprocess.run(job_queue.get(), shell=True, capture_output=True, text=True)
          result_list.append({"command": result.args, "result":result.returncode, "output": result.stdout, "error": result.stderr})
        else:
            time.sleep(1.0)
            

if __name__ == "__main__":
    result_list = []
    stop_signal = False
    t1 = threading.Thread(target= consumer)
    t1.start()
    producer()
    t1.join()
    for result in result_list:
        if result["result"] == 0:
            print(f"✅ Command: {result["command"]} | Status: Success | Output:{result["output"]}")
        else:
            print(f"❌ Command: {result["command"]} | Status: Failed | Output:{result["output"]} | Error: {result["error"]}")