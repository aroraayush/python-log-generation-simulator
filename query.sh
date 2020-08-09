#! /bin/bash

# usage()
# {
#     echo "Usage : $0 <DATA_PATH>" 
# }

# usage2()
# {
#     echo "\nUsage : QUERY <IP_ADDRESS> <CPU_ID> <DATE(YYYY-MM-DD)> <TIME_START> <TIME_END> OR EXIT to exit.\n"
# }

# exit_str=EXIT

# if [ "$#" -ne 1 ]
# then
#     usage;
#     exit 3
# fi

# if [ ! -d $1 ]; then 
#     echo "========================================================"
#     echo "Non-existent directory : $1. " >&2
#     echo "========================================================\n"
#     exit 3 
# elif [ ! -d $1/logs ]; then 
#     echo "========================================================"
#     echo "Cannot read logs. $1/logs doesn't exist " >&2
#     echo "========================================================\n"
#     exit 3 
# fi

# echo "========================================================"
# echo "Please wait !!! Parsing logs..."

# # passing arguments as it is
# python3 generate_trie.py $@

# echo "Logs parsed. You can query the logs\n"
# usage2;

python3 query_logs.py "query 192.168.1.10 1 2014-10-31 00:00 2014-10-31 00:05"

# user_input()
# {
#     printf ">"
#     read -r query

#     shopt -s nocasematch
#     case "$query" in
#         $exit_str ) 
#             ;;
#         *) 
#             arr=( $query )
#             echo ${#arr[@]}
#             if [[ ${#arr[@]} -ne 7 ]]
#                 then
#                 usage2;
#                 user_input;
#             else
#                 if [[ ${arr[0]} == "QUERY" || ${arr[0]} == "query" ]]
#                 then
#                     python3 query_logs.py $query
#                     user_input;
#                 else
#                     usage2;
#                     user_input;
#                 fi
#             fi
#     esac
# }

user_input;