# Daniel Baker
# CS 3310
# Assignment 3
# 10 / 31 / 2023

# The dictionary 'frequencies' contains the frequenc counts for each letter in the alphabet.
frequencies = {'A' : 77, 'B' : 17, 'C' :  32, 'D' : 42, 'E' : 120, 'F' : 24, 'G' : 17, 'H' : 50, 'I' : 76, 'J' : 4, 'K' : 7, 'L' : 42, 'M' : 24, 
               'N' : 67, 'O' : 67, 'P' : 20, 'Q' : 5, 'R' : 59, 'S' : 67, 'T' : 85, 'U' : 37, 'V' : 12, 'W' : 22, 'X' : 4, 'Y' : 22, 'Z' : 2}

# The Node class represents an individual node in the Huffman tree.
class Node:
    def __init__(self, char, freq):
        self.char = char # Charachter the node represents
        self.freq = freq # Frequency of the charachter
        self.left = None # Left child
        self.right = None # Right child
    
    # Overload the less than operator to compare the frequency of the nodes.
    def __lt__(self, other):
        return self.freq < other.freq

# This class represents a minimum heap data structure.
class MinHeap:
    def __init__(self):
        self.heap = [] # Initialize the empty heap list.
    
    # This method adds a node to the heap and ensures the heap property is maintained.
    def push(self, node):
        self.heap.append(node)
        self._bubble_up(len(self.heap) - 1)
     
    # This method removes the smallest node (root) from the heap.   
    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        if len(self.heap) > 0:
            self._bubble_down(0)
        
        return root
    
    # Helper methods to maintain the heap property.
    def _parent(self, index):
        return (index - 1) // 2
    
    def _left_child(self, index):
        return 2 * index + 1
    
    def _right_child(self, index):
        return 2 * index + 2
    
    # Method to move the node up until the heap property is maintained.
    def _bubble_up(self, index):
        parent = self._parent(index)
        
        while index > 0 and self.heap[index].freq < self.heap[parent].freq:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = self._parent(index)

    # Method to move the node down to its appropriate position.
    def _bubble_down(self, index):
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)
        
        
        if left < len(self.heap) and self.heap[left].freq < self.heap[smallest].freq:
            smallest = left
        
        if right < len(self.heap) and self.heap[right].freq < self.heap[smallest].freq:
            smallest = right
        
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest)

   
# Generate the Huffman tree using the frequencies dictionary.
class HuffmanTree:
    
    # Initialize the tree by creating a min heap and pushing all the nodes onto the heap.
    def __init__(self, frequencies):
        
        self.heap = MinHeap() # Creates a new min heap instance.
        
        # Convert each (character, frequency) pair into a node and push it onto the heap.
        for char, freq in frequencies.items():
            node = Node(char, freq)
            self.heap.push(node)
        
        # While there is more than one node in the heap, pop the two smallest nodes and merge them.    
        while len(self.heap.heap) > 1:
            node1 = self.heap.pop()
            node2 = self.heap.pop()
            
            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            self.heap.push(merged)
            
        self.root = self.heap.pop() # The last node in the heap is the root of the tree.
    
    # Recursive method to get the Huffman codes for each character.
    def get_huffman_codes(self, node, prefix=""):
        if node is not None:
            # If it's a leaf node (has a character), return its Huffman code.
            if node.char is not None:
                return {node.char : prefix}

            # Otherwise, recursively call the method on the left and right children.
            left_codes = self.get_huffman_codes(node.left, prefix + '0')
            right_codes = self.get_huffman_codes(node.right, prefix + '1')
            
            # Merge the huffman codes from the left and right subtrees.
            return {**left_codes, **right_codes}
        return {}
    
# Create the Huffman tree.    
tree = HuffmanTree(frequencies)

# Get the Huffman codes for each character.
huffman_codes = tree.get_huffman_codes(tree.root)

# Display each character, its frequency, the Huffman code, and the total number of bits used.
for char,freq in sorted(frequencies.items()):
    code = huffman_codes[char]
    print(f"{char} : {freq} : {code} : {len(code)} : {freq * len(code)}")
