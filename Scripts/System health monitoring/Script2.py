import os
import subprocess
import logging
from datetime import datetime


logging.basicConfig(filename='system_health.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

def check_cpu_usage():
    cpu_usage = float(os.popen("grep 'cpu ' /proc/stat").read().split()[1:5])
    total = sum(cpu_usage)
    idle = cpu_usage[3]
    usage = (1 - (idle / total)) * 100
    if usage > CPU_THRESHOLD:
        alert_message = f"High CPU usage detected: {usage:.2f}%"
        print(alert_message)
        logging.warning(alert_message)
    return usage

def check_memory_usage():
    with open('/proc/meminfo', 'r') as mem:
        lines = mem.readlines()
        total_memory = float(lines[0].split()[1])
        free_memory = float(lines[1].split()[1])
        available_memory = float(lines[2].split()[1])
        used_memory = total_memory - free_memory
        usage = (used_memory / total_memory) * 100
        if usage > MEMORY_THRESHOLD:
            alert_message = f"High memory usage detected: {usage:.2f}%"
            print(alert_message)
            logging.warning(alert_message)
    return usage

def check_disk_usage():
    disk_usage = subprocess.check_output(['df', '/']).decode('utf-8').split('\n')[1].split()[4]
    usage = float(disk_usage[:-1])
    if usage > DISK_THRESHOLD:
        alert_message = f"High disk usage detected: {usage:.2f}%"
        print(alert_message)
        logging.warning(alert_message)
    return usage

def check_running_processes():
    process_count = int(subprocess.check_output(['ps', '-e', '--no-headers']).decode('utf-8').count('\n'))
    return process_count

def monitor_system():
    cpu_usage = check_cpu_usage()
    memory_usage = check_memory_usage()
    disk_usage = check_disk_usage()
    process_count = check_running_processes()

    # Log the system health summary
    logging.info(f"CPU usage: {cpu_usage:.2f}%, Memory usage: {memory_usage:.2f}%, "
                 f"Disk usage: {disk_usage:.2f}%, Running processes: {process_count}")

if __name__ == "__main__":
    monitor_system()
