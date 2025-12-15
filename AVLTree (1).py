#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		if self.height == -1:
			return False
		else:
			return True
    
    

	def get_height(self, another_node) -> int:
		if not another_node.is_real_node():
			return -1
		return another_node.height

	def update_height(self):
		sons = [self.left, self.right]
		max_son_height = max([self.get_height(node) for node in sons])
		self.height = max_son_height + 1
  
	def get_balance(self):
		sons = [self.left, self.right]
		left_son_height = self.left.height if self.left is not None else -1
		right_son_height = self.right.height if self.right is not None else -1
		return self.get_height(self.left) - self.get_height(self.right)


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self.height: int = -1
		self.size: int = 0


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		count = 0
		curr = self.root
		while curr.height > -1:
			if curr.key == key:
				return curr, count
			elif curr.key > key: #go left
				curr = curr.left
				count += 1
			elif curr.key < key: #go right
				curr = curr.right
				count += 1
		return None, -1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		return None, -1
	
	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		return None, -1, -1


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	def rotate_right(self, root: AVLNode) -> AVLNode:
		"""
		make the left child of the root (subtree or whole tree) the new root
		"""
		new_root = root.left
		former_root = root
		sub_tree_to_move = new_root.right

        # ביצוע הסיבוב
		new_root.right = former_root
		former_root.left = sub_tree_to_move

        # עדכון גבהים
		former_root.update_height(former_root)
		new_root.update_height(new_root)
		return new_root


	def rotate_left(self, root: AVLNode) -> AVLNode:
		"""
		make the left child of the root (subtree or whole tree) the new root
		"""
		new_root = root.right
		former_root = root
		sub_tree_to_move = new_root.left

        # ביצוע הסיבוב
		new_root.left = former_root
		former_root.right = sub_tree_to_move

        # עדכון גבהים
		former_root.update_height(former_root)
		new_root.update_height(new_root)
		return new_root

# need to add rebalance
	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		if tree2.root is None:
			return 


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None


def print_avl_labeled(node, prefix="", is_left=None, label="root"):
    if node is None:
        connector = "├── " if is_left else "└── "
        print(prefix + connector + f"{label}: ∅")
        return

    if is_left is None:  # root
        print(f"{label}: {node.key} (h={node.height})")
    else:
        connector = "├── " if is_left else "└── "
        print(prefix + connector + f"{label}: {node.key} (h={node.height})")

    new_prefix = prefix + ("│   " if is_left else "    ")

    print_avl_labeled(node.left, new_prefix, True, "L")
    print_avl_labeled(node.right, new_prefix, False, "R")




# ----- TEMP MANUAL TREE (FOR PRINTING ONLY) -----

tree = AVLTree()

root = AVLNode(10, "root")
left = AVLNode(5, "left")
right = AVLNode(15, "right")
n2 = AVLNode(2, "n2")
n7 = AVLNode(7, "n7")
n12 = AVLNode(12, "n12")
n18 = AVLNode(18, "n18")

# set heights so they are considered "real"
root.height = 1
left.height = 0
right.height = 0
n2.height = 0
n7.height = 0
n12.height = 0
n18.height = 0
left.left = n2
left.right = n7
right.left = n12
right.right = n18

n2.parent = left
n7.parent = left
n12.parent = right
n18.parent = right


# connect pointers
root.left = left
root.right = right
left.parent = root
right.parent = root

tree.root = root

print_avl_labeled(tree.root)


def test_search(tree, key):
	return tree.search(key)

result = test_search(tree, 5)
print(result)

