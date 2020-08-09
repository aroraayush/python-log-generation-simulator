import sys
import logging
import logging.config
import random
import time
from concurrent.futures import ProcessPoolExecutor
from functools import wraps
from multiprocessing import cpu_count
from os import makedirs, path, mkdir
from pathlib import Path
from shutil import rmtree
from datetime import date, datetime, timedelta
from filelock import FileLock

# PYCACHE = Path('__pycache__')
OUTPUT = Path('logs')
LOCKS = OUTPUT / '.locks'

logger = logging.getLogger('locks')

def ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(start_ip)

    while temp != end:
        for i in (3, 2, 1):
            if temp[i] == 255:
                start[3] = -1
                temp[i] = 0
                temp[i-1] += 1
            start[3] += 1
            ip_range.append(".".join(map(str, temp)))

    return ip_range

def create_dir(parent_path, folder_name):
    child_dir_path = path.join(parent_path, folder_name)
    
    if path.isdir(child_dir_path):
        print(child_dir_path ,"exists")
        return child_dir_path
    else:
        print(child_dir_path ,"doesn't exist. Creating dir :",folder_name)
        try:
            mkdir(child_dir_path)
        except OSError:
            print ("Creation of the directory %s failed" % child_dir_path)
        else:
            print ("Successfully created the directory %s \n" % child_dir_path)
            return child_dir_path

def create_log_file(parent_dir, file_name):
    file_path = path.join(parent_dir, file_name + ".log")
    if path.isfile(file_path):
        print(file_path ,"exists")
    else:
        print(file_path ,"doesn't exist. Creating...\n")
        try:
            open(file_path, 'a').close()
        except:
            print("Error creating file :", file_path)

# ======================================================================================

def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception("Error writing logs...")
            raise
    return wrapper

@log_exceptions
def write_logs(server_ip, cpu_id, log_date, timestamps):
    
    logger.debug(f"Processing server_ip {server_ip}")
    for timestamp in timestamps:
        
        # Get the locks
        filename = f'{log_date}.log'
        lock = FileLock(LOCKS / f'{log_date}.lock')
        logger.debug(f"{server_ip}, {timestamp}: Aquiring lock {lock!r}...")

        with lock.exclusive() as exc_lock:
            logger.debug(f"{server_ip}, {timestamp}: Got lock {lock!r}!")

            # Open the output file for writing
            with open(OUTPUT / filename, 'a') as output:

                # Write all the things
                # time_stamp = "1"
                # usage = 10
                # format (time_stamp, server_ip, cpu_id, usage)
                output.write(f'{timestamp} {server_ip} {cpu_id} {int(random.uniform(0, 100))}\n')
                output.flush()
                # output.write(f'{server_ip}: Done!\n')
                output.flush()
            logger.debug(f"{server_ip}, {timestamp}: Releasing lock {lock!r}...")

if __name__ == '__main__':

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'multiprocess',
            },
        },
        'formatters': {
            'multiprocess': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(processName)-7s %(message)s',
            },
        },
        'loggers': {
            'locks': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        },
    })

    # logs_dir_path = create_dir(parent_path, "logs")
    # create_log_file(logs_dir_path, log_date)

    # Parent Folder Directory
    # parent_path = (sys.argv)[1]

    # Data for which logs have to generated
    log_date = sys.argv[1:][1] if (len(sys.argv[1:]) == 2) else date.today()

    # Starting time at 00:00:00
    date_time_str = f'{log_date} 00:00:00'
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    
    # Starting epoch time
    starting_ts = int(date_time_obj.strftime('%s'))
    # Ending epoch time
    ending_ts = int((date_time_obj + timedelta(1)).strftime('%s'))

    # Creating timestamps for 24 hour
    timestamps = []
    for ts in range(starting_ts, ending_ts, 60):
        timestamps.append(ts)

    # 2 CPUs per server
    cpu_id_0 = 0
    cpu_id_1 = 1

    # 1000 IPs generated
    servers = ip_range("192.168.0.0", "192.168.0.3")
    # servers = ip_range("192.168.0.0", "192.168.3.234")
    # print(len(servers))
    # servers = ["192.168.1.10"]

    # random.shuffle(servers)

    if not path.exists(OUTPUT):
        # # Recursive directory creation function
        makedirs(OUTPUT)
        makedirs(LOCKS)
    else:
        rmtree(OUTPUT)           # Recursively remove all the subdirectories!
        # rmtree(PYCACHE)
        makedirs(OUTPUT)
        makedirs(LOCKS)

    with ProcessPoolExecutor() as pool:
        for server in servers:
            pool.submit(write_logs, server, cpu_id_0, log_date, timestamps)
            pool.submit(write_logs, server, cpu_id_1, log_date, timestamps)
        logger.debug(f"Started generating the logs for {log_date}")
        pool.shutdown()
    logger.debug(f"Finished generating the logs for {log_date}")
    rmtree(LOCKS)