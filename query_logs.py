import sys
from time import strftime, localtime
from datetime import datetime

# ================== trie data structure ==================


class Node(object):
    def __init__(self):
        self.is_valid = False
        self.prefix = ""
        self.children = [None]*10


class CompactPrefixTree(object):

    def __init__(self, file=None):
        self.root: Node = None

    def __str__(self):
        s = ""
        indent = 0
        s = self.make_string(s, self.root, indent)
        return s

    def query_trie(self, ip_address, cpu_id, starting_date, starting_time, end_date, end_time):

        start_datetime_obj = datetime.strptime(
            starting_date+" " + starting_time + ":00", '%Y-%m-%d %H:%M:%S')
        end_datatime_obj = datetime.strptime(
            end_date+" " + end_time + ":00", '%Y-%m-%d %H:%M:%S')

        # Epoch time
        starting_ts = int(start_datetime_obj.strftime('%s'))
        ending_ts = int(end_datatime_obj.strftime('%s'))

        starting_ts_str = f"{ip_address} {cpu_id} {starting_ts}"
        ending_ts_str = f"{ip_address} {cpu_id} {ending_ts}"
        # print("starting_ts_str", starting_ts_str)
        # print("ending_ts_str", ending_ts_str)
        ip_list = []
        self.check(f"{starting_ts_str} 56", ip_list)
        return ip_list

        # print("ip_address, cpu_id, , , end_date, end_time", ip_address, cpu_id, starting_date, starting_time, end_date, end_time)
        # print("In trie")

    def get_suffix(self, common, word) -> str:
        '''
        Helps in finding the suffix
        common => the prefix which is to be removed
        word => the original word
        return => the remaining suffix
        '''
        if len(word) <= len(common):
            return ""
        return word[len(common):]

    def print_tree(self, node, indent):
        if node == null:
            return
        for i in range(indent):
            print("\t")
        print(node.prefix)
        if node.is_valid:
            print("*")
        print()
        for j in range(10):
            if node.children[j] is not None:
                print_tree(node.children[j], indent + 1)

    def get_longest_common_prefix(self, s1, s2):
        res = ""
        length = min(len(s1), len(s2))
        for x in range(length):
            if s1[x] == s2[x]:
                res = res + s1[x]
            else:
                break
        return res

    def make_string(self, s, node, indent):
        if node is None:
            return s
        for x in range(indent):
            s = s + "\t"

        s = s + node.prefix
        if node.is_valid:
            s = s + "*"
        s = s + "\n\t"
        for y in range(10):
            if node.children[y] is not None:
                s = self.make_string(s, node.children[y], indent + 1)

        return s

    def check(self, s, arr):
        return self.check_util(s, self.root, arr)

    def check_util(self, s, node, arr):
        if node is None or not s.startswith(node.prefix) or (s == node.prefix and not node.is_valid):
            return False
        if s == node.prefix:
            ts_usage = s.split()[-2:]
            arr.append(f"({strftime('%Y-%m-%d %H:%M', localtime(int(ts_usage[0])))}, {ts_usage[1]})")
            return True
        s = self.get_suffix(node.prefix, s)
        idx = ord(s[0]) - ord('0')
        return self.check_util(s, node.children[idx], arr)

    def check_prefix(self, prefix, node):
        if len(prefix) == 0:
            return True
        if node is None or (not prefix.startswith(node.prefix) and not node.prefix.startswith(prefix)):
            return False

        prefix = self.get_suffix(node.prefix, prefix)
        if not len(prefix):
            return True
        idx = ord(prefix[0]) - ord('0')
        return self.check_prefix(prefix, node.children[idx])

    def add(self, s) -> Node:
        self.root = self.add_util(s, self.root)

    def add_util(self, s, node) -> Node:
        if not len(s):
            return node

        # if node is None, we create a new node
        if node is None:
            node = Node()
            node.prefix = s
            node.is_valid = True
            return node

        # earlier was a prefix, but is now node itself
        if node.prefix == s and not node.is_valid:
            node.is_valid = True
            return node

        # IP adress already exists
        if node.prefix == s:
            return node

        # case when 1596956400 192.168.0.1 1 is added after 1596956400 192.168.0.0 1
        if(s.startswith(node.prefix)):
            s = self.get_suffix(node.prefix, s)
            idx = ord(s[0]) - ord('0')
            if node.children[idx] is None:
                node.children[idx] = Node()
                node.children[idx].prefix = s
                node.children[idx].is_valid = True
            else:
                node.children[idx] = self.add_util(s, node.children[idx])
            return node

        # recursive case, checks for common prefix
        common = self.get_longest_common_prefix(node.prefix, s)
        suf1 = self.get_suffix(common, node.prefix)
        suf2 = self.get_suffix(common, s)

        if len(suf2) == 0:
            node.prefix = s
            node.is_valid = True
            new_node = Node()
            new_node.prefix = suf1
            new_node.is_valid = true
            node.children[ord(suf1[0]) - ord('0')] = new_node
            return node

        # if block ends, continue with the normal logic for recursive case

        new_node = Node()
        new_node.prefix = common
        node.prefix = suf1
        idx = ord(suf1[0]) - ord('0')
        new_node.children[idx] = node
        idx = ord(suf2[0]) - ord('0')
        new_node.children[idx] = self.add_util(suf2, new_node.children[idx])
        return new_node

# ================== Helper Functions ==================


def usage2():
    print("\nUsage : QUERY <IP_ADDRESS> <CPU_ID> <DATE(YYYY-MM-DD)> <TIME_START> <TIME_END> OR EXIT to exit.")


def user_input(dict):

    # usr_input = "query 192.168.0.0 1 2020-08-09 00:00 2020-08-09 00:05"
    usr_input = input("\n> ")
    usr_input_arr = usr_input.lower().split()
    
    if len(usr_input_arr) == 7:
        if usr_input_arr[0] == "query":

            ip_address = usr_input_arr[1:][0]
            cpu_id = usr_input_arr[1:][1]
            starting_date = usr_input_arr[1:][2]
            starting_time = usr_input_arr[1:][3]
            end_date = usr_input_arr[1:][4]
            end_time = usr_input_arr[1:][5]
            my_list = dict.query_trie(ip_address, cpu_id, starting_date,
                            starting_time, end_date, end_time)
            print(f"\nCPU{cpu_id} usage on {ip_address}:\n{','.join(my_list)}\n")
            # user_input(dict)
        else:
            usage2()
            user_input()
    elif usr_input_arr[0] == "exit":
        sys.exit()
    else:
        usage2()
        user_input()

# ================== Driver File - Main Code ==================


dict = CompactPrefixTree()
with open('logs/2020-08-09.log', buffering=200000) as f:
    for line in f:
        # 
        line_arr = line.strip().split()
        dict.add(f"{line_arr[1]} {line_arr[2]} {line_arr[0]} {line_arr[3]}")

# print(dict)

print("Logs parsed successfully. You can now query the logs...\n")
user_input(dict)
