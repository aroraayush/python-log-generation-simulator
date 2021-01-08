
- ## Log generating simulator
    A python based simulator that generates nearly 172 million logs (per minute) for a single day for 1000 servers with 2 CPUs each

    - Logs will be generated using python's multiprocessing module.
    - A pool for workers will create logs by locking a single file for writing.

    #### log format
    > <EPOCH_TIMESTAMP_FOR_DATE> <SERVER_IP> <CPU_ID> <USAGE_PERCENT>
    #### example log
    > 1596870180 192.168.0.2 0 71

---
## Log Parsing, using trie, to query logs (WIP)
Parses the logs and creates a trie to query within a second

---

# Usage

#### Log generation (if date not specified, logs for current day will be generated)
> ./generate.sh <DATA_PATH> [date]
- A folder with name `logs` will be generated in the `DATA_PATH`
- Logs and locks will be generated inside the `logs` directory and locks will the removed once logs created

#### Logs Parsing and Querying
> ./query.sh <LOGS_PARENT_DIR>
```
========================================================
Please wait !!! Parsing logs...

# A few seconds/minutes
Logs parsed successfully. You can query the logs


Usage : QUERY <IP_ADDRESS> <CPU_ID> <DATE(YYYY-MM-DD)> <TIME_START> <TIME_END> OR EXIT to exit.

# User input
> _
```
#### User Input Example
```
> QUERY 192.168.1.10 1 2014-10-31 00:00 2014-10-31 00:05
```
#### Query Output
```

```
