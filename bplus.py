class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf  # is this node a leaf?
        self.keys = []  # to store keys
        self.children = []  # children nodes

class BPlusTree:
    def __init__(self, max_keys=4):
        self.root = BPlusTreeNode(True)
        self.max_keys = max_keys

    # find correct leaf for insertion
    def _find_leaf(self, node, key):
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node

    # insert key into a node, may cause split
    def insert(self, key):
        leaf = self._find_leaf(self.root, key)
        self._insert_into_node(leaf, key)

        if len(self.root.keys) >= self.max_keys:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0, self.root)
            self.root = new_root

    # insert key in a leaf or internal node (helper)
    def _insert_into_node(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        node.keys.insert(i, key)
        
        if node.leaf:
            node.children.insert(i + 1, None)  # keep balance in leaves

    # split an overfull node
    def _split_child(self, parent, index, child):
        new_child = BPlusTreeNode(child.leaf)
        mid_index = len(child.keys) // 2
        mid_key = child.keys[mid_index]

        if child.leaf:
            # handle leaf split
            new_child.keys = child.keys[mid_index:]
            child.keys = child.keys[:mid_index]
            new_child.children = child.children[mid_index:]
            child.children = child.children[:mid_index]
        else:
            # handle internal node split
            new_child.keys = child.keys[mid_index + 1:]
            new_child.children = child.children[mid_index + 1:]
            child.keys = child.keys[:mid_index]
            child.children = child.children[:mid_index + 1]
            parent.keys.insert(index, mid_key)

        parent.children.insert(index + 1, new_child)
        parent.keys.insert(index, child.keys.pop())

    # search for a key in the tree
    def search(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return key if key in node.keys else None

    # display tree (just in-order)
    def _display(self, node, level=0):
        print("  " * level + f"Node(keys={node.keys})")
        if not node.leaf:
            for child in node.children:
                self._display(child, level + 1)

    def display(self):
        self._display(self.root)
def main():
    bptree = BPlusTree(max_keys=3)

    keys_to_insert = [10, 20, 5, 6, 15, 30, 25, 3, 1]
    for key in keys_to_insert:
        print(f"\in {key}:")
        bptree.insert(key)
        bptree.display()

    search_keys = [15, 6, 100]
    print("\nsearching:", search_keys)
    for key in search_keys:
        result = bptree.search(key)
        print(f"{key}: {'found' if result is not None else 'Not found'}")

    more_keys = [12, 18, 17, 4, 8]
    for key in more_keys:
        print(f"inn {key}:")
        bptree.insert(key)
        bptree.display()

if __name__ == "__main__":
    main()
