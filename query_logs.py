output = open('logs/2020-08-09.log','a')

class Node(object):
    def __init__(self):
        self.is_valid = False
        self.prefix = ""
        self.children = [None]*10

class CompactPrefixTree(object):

    def __init__(self, file=None):
        self.root = Node()

    def get_suffix(self, common,word) -> str:
        '''
        Helps in finding the suffix
        common => the prefix which is to be removed
        word => the original word
        return => the remaining suffix
        '''
        if(len(word) <= len(common)):
            return "";
        return word[len(common):]

    
    def add(self, s, node) -> Node:
        if(len(s)==0):
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
        
        idx = 0
        # case when 1596956400 192.168.0.1 1 is added after 1596956400 192.168.0.0 1
        if(s.startswith(node.prefix)):
            s = self.get_suffix(node.prefix, s)
            idx = ord(s[0]) - ord('0')
            if node.children[idx] is None :
                node.children[idx] = Node()
                node.children[idx].prefix = s
                node.children[idx].isWord = True
            else:
                node.children[idx] = self.add(s, node.children[idx])
            return node
        
        # recursive case, checks for common prefix
        common = get_longest_common_prefix(node.prefix, s)
        suf1 = self.get_suffix(common,node.prefix)
        suf2 = self.get_suffix(common,s)

        if len(suf2) == 0:
            node.prefix = s
            node.is_valid = True
            new_node = Node()
            new_node.prefix = suf1
            new_node.isWord = true
            node.children[ord(suf1[0]) - ord('0')] = new_node
            return node;
        
        # if block ends, continue with the normal logic for recursive case

        new_node = Node()
        new_node.prefix = common
        node.prefix = suf1
        idx = ord(suf1[0]) - ord('0')
        new_node.children[idx] = node
        idx = ord(suf2[0]) - ord('0')
        new_node.children[idx] = self.add(suf2,new_node.children[idx])
        return new_node;

node = Node()
dict = CompactPrefixTree()
dict.add("1596956400", node)
dict.add("1596956401", node)
# with open('logs/2020-08-09.log', buffering=200000) as f:
#     for line in f:
#         print("line", line.strip())