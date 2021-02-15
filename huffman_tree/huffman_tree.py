class node:
    """
    A Huffman Tree Node
    """
    def __init__(self, freq = None, pattern = None, left=None, right=None):
        # frequency of symbol
        self.freq = freq

        # symbol name (charecter)
        self.symbol = pattern

        # node left of current node
        self.left = left

        # node right of current node
        self.right = right

        # tree direction (0/1)
        self.huff = ''


def create_tree(freq, unique_pattern):
    """Create a Huffman Tree
    pattern: Characters for huffman tree
    freq: frequency of characters
    """
    nodes = []
    # list containing unused nodes
    # converting charecters and frequencies
    # into huffman tree nodes
    for i in range(len(unique_pattern)):
        nodes.append(node(freq[i], unique_pattern[i]))

    while len(nodes) > 1:
        # sort all the nodes in ascending order
        # based on theri frequency
        nodes = sorted(nodes, key=lambda x: x.freq)

        # pick 2 smallest nodes
        left = nodes[0]
        right = nodes[1]

        # assign directional value to these nodes
        left.huff = 0
        right.huff = 1

        # combine the 2 smallest nodes to create
        # new node as their parent
        new_node = node(left.freq + right.freq, left.symbol + right.symbol, left, right)

        # remove the 2 nodes and add their
        # parent as new node among others
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)
    return nodes


def recode_nodes(node, dictnr, val=''):
    """Recode a Huffman Tree into a dictionary
     each key of the dictionary: 4-bits substring of the old payload
     each value of the dictionary: substring of the new payload
    """
    # huffman code for current node
    new_val = val + str(node.huff)

    # if node is not an edge node
    # then traverse inside it
    if node.left:
        recode_nodes(node.left, dictnr, new_val)
    if node.right:
        recode_nodes(node.right, dictnr, new_val)

    # if node is edge node then
    # display its huffman code
    if not (node.left or node.right):
        dictnr.update({node.symbol:new_val})
    return dictnr


def regenerate_node(tree_lst):
    """Regenerate each node from a tree list"""

    # Initialise tree
    tree_nodes = {}

    # Extract tree
    for item in tree_lst:
        key = item[:4]
        need_extract = item[4] == '1'
        if not need_extract:
            value = item[5:]
        else:
            pos = len(item)-1
            while True:
                if item[pos] != item[pos-1]:
                    value = item[5:pos]
                    break
                pos -= 1
        tree_nodes.update({key: value})

    return tree_nodes


def get_node(parent, direction):
    """Get a node from its parent"""
    if direction == 0:
        if not parent.left:
            parent.left = node()
            parent.left.huff = 0
        return parent.left
    else:
        if not parent.right:
            parent.right = node()
            parent.right.huff = 1
        return parent.right


def regenerate_tree(tree_nodes):
    """Regenerate tree"""

    # Initialise tree
    nodes = [node()]

    # Regenerate tree
    for x, y in tree_nodes.items():
        current_node = nodes[0]
        for i in range(len(y)):
            if y[i] == '0':
                current_node = get_node(current_node, 0)
            elif y[i] == '1':
                current_node = get_node(current_node, 1)

            if i == len(y)-1:
                current_node.symbol = x
    return nodes


def print_tree(node, val=''):
    """Recode a Huffman Tree into a dictionary
     each key of the dictionary: 4-bits substring of the old payload
     each value of the dictionary: substring of the new payload
    """
    # huffman code for current node
    new_val = val + str(node.huff)

    # if node is not an edge node
    # then traverse inside it
    if node.left:
        print_tree(node.left, new_val)
    if node.right:
        print_tree(node.right, new_val)

    # if node is edge node then
    # display its huffman code
    if not (node.left or node.right):
        print(f"{node.symbol} <- {new_val}")


def search_pattern(node, pattern, end, result) -> list:
    """Search pattern"""

    # If we are not
    while end < len(pattern):
        if pattern[end] == '0':
            return search_pattern(node.left, pattern, end+1, result)

        elif pattern[end] == '1':
            return search_pattern(node.right, pattern, end+1, result)

    if not (node.left or node.right):
        result = node.symbol
        return result


def search_nodes(dictnr, target):
    """Search the a nodes of a Huffman tree and
    return the corresponding huffman code"""
    return dictnr.get(target)








