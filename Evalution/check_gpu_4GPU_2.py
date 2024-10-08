import subprocess
import time
import numpy as np
import subprocess
import numpy as np

def check_gpu_idle(gpu_ids):
    """
    Check if specific GPUs are idle by querying their utilization.
    
    Args:
        gpu_ids (list): List of GPU IDs to check.

    Returns:
        bool: True if all specified GPUs are idle, False otherwise.
    """
    try:
        # Utilizing multiple GPUs requires separate checks for each GPU
        gpu_usages = []
        for gpu_id in gpu_ids:
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--id=' + str(gpu_id), '--format=csv,noheader,nounits'], capture_output=True, text=True)
            if "Failed" in result.stdout or "Error" in result.stdout:
                print("Error fetching GPU data for GPU ID " + str(gpu_id) + ":", result.stdout)
                return False  # Assume not idle if there's an error
            usage = int(result.stdout.strip().split()[-1])
            gpu_usages.append(usage)
        
        print("Parsed GPU Usages:", gpu_usages)
        return np.all(np.array(gpu_usages) == 0)
    except Exception as e:
        print("An error occurred while checking GPU idle status:", str(e))
        return False


def run_script(script_name, check_interval, gpu_ids):
    """
    Run a script when specified GPUs are idle.
    
    Args:
        script_name (str): The name of the script to run.
        check_interval (int): Time in seconds between checks.
        gpu_ids (list): List of GPU IDs to monitor.
    """
    while True:
        if check_gpu_idle(gpu_ids):
            print(f"All specified GPUs are idle, running the script {script_name}...")
            time.sleep(1)  # Short delay to ensure GPUs remain idle
            if check_gpu_idle(gpu_ids):
                subprocess.run(['bash', script_name])
                break
        else:
            print(f"Specified GPUs are busy, checking again after {check_interval} seconds...")
            time.sleep(check_interval)
def main():
    script_to_run_1 = "run_long.sh"
    script_to_run_2 = "run_long_2.sh"
    script_to_run_3 = "run_long_3.sh"
    # script_to_run_1 = "run.sh"
    # script_to_run_2 = "run_2.sh"
    # script_to_run_3 = "run_3.sh"
    # script_to_run_3 = "run_4.sh"
    check_interval = 30
    gpu_ids = [0,1,2,3,4,5,6,7]  # Specify which GPUs to monitor
    
    # Sequentially run the scripts on specified GPUs
    run_script(script_to_run_1, check_interval, gpu_ids)
    #run_script(script_to_run_4, check_interval, gpu_ids)
if __name__ == "__main__":
    main()
