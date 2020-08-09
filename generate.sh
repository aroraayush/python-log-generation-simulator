#! /bin/bash

usage()
{
    echo "Usage : $0 <DATA_PATH> [date]" 
    echo "If date not provided, logs will be created for current date" 
}

if [[ "$#" -gt 2 || "$#" -lt 1 ]]
then
    usage;
    exit 3
fi

if [ ! -d $1 ]; then 
    echo "Non-existent directory : $1. Cannot create logs here" >&2
    exit 3 
fi
echo "============================================================="
echo "Logs will be created in : ${1}/logs"
echo "=============================================================\n"

# passing arguments as it is
python3 generator.py $@

