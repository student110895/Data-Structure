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
        self.left = self.right = self.parent = None
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
    

    def get_height(self):
        return self.height  


    def update_height(self):
        if not self.is_real_node(): 
            return 
        self.height = max(self.left.get_height(), self.right.get_height()) + 1

  
    def get_balance(self):
        return self.left.get_height() - self.right.get_height()


"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    
    
    # ---------- GLOBAL (shared) sentinel ----------
    _GLOBAL_FAKE = AVLNode(None, None)
    _GLOBAL_FAKE.left = _GLOBAL_FAKE
    _GLOBAL_FAKE.right = _GLOBAL_FAKE
    _GLOBAL_FAKE.parent = _GLOBAL_FAKE
    _GLOBAL_FAKE.height = -1
    # --------------------------------------------

    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.fake_node = AVLTree._GLOBAL_FAKE
        self.root = self.fake_node
        self.height = -1
        self._size = 0
        self._max_node = None

        self.root = self.fake_node
        self.height = -1
        self._size = 0
        self._max_node = None
    
    def _new_real_node(self, key, val, parent):
        """ Creates a node instantly considered as real with height 0"""
        n = AVLNode(key,val)
        n.left = AVLTree._GLOBAL_FAKE
        n.right = AVLTree._GLOBAL_FAKE
        n.parent = parent
        n.height = 0
        return n
  
  
    def update_tree_height(self):
        self.root.update_height()
        self.height = self.root.get_height()
        

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
        return None, count

    
    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        if self._max_node is None:
            return None, -1
        curr = self._max_node
        e = 0   # count upwards movements
        while curr.key > key and curr.parent.is_real_node():
            e += 1
            curr = curr.parent

        count = 0 # count downwards movements
        while curr.height > -1:
            if curr.key == key:
                return curr, count + e
            elif curr.key > key: #go left
                curr = curr.left
                count += 1
            elif curr.key < key: #go right
                curr = curr.right
                count += 1
        return None, count + e
    
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
        #case 1: empty tree
        if not self.root.is_real_node():
            new_node = self._new_real_node(key, val, self.fake_node)
            self.root = self._max_node = new_node
            self._size = 1
            self.height = 0
            return new_node, 0, 0
        
        #case 2: normal BST insert
        curr = self.root 
        path = 0    #edges walked from root to insertion point (before rebalancing)
        promote = 0  #counts number of PROMOTE (height-increase) events during rebalancing
        
        while True:
             
            if key < curr.key: #go left
                if curr.left.is_real_node():
                    curr = curr.left
                    path += 1
                else:
                    new_node = self._new_real_node(key, val, curr)
                    curr.left = new_node
                    path += 1
                    break   
                
            elif key > curr.key: #go right
                if curr.right.is_real_node():
                    curr = curr.right
                    path += 1
                else:
                    new_node = self._new_real_node(key, val, curr)
                    curr.right = new_node
                    path += 1
                    break
        
        #rebalance tree in place and counts number of PROMOTE 
        promote += self.rebalance_after_insert(new_node) 
        
        self._size += 1
        if self._max_node is None or key > self._max_node.key:
            self._max_node = new_node
        self.height = self.root.height
        return new_node, path, promote



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
        if not self.root.is_real_node(): #if tree is empty
            self.insert(key, val)
            return self.root, 0, 0
        edges = 0 #count upwards movements
        curr = self._max_node
            
        #climb up until key belongs in curr's right subtree
        while key < curr.key and curr.parent.is_real_node():
            curr = curr.parent
            edges += 1
   
        promote = 0 
        path = 0  #count downwards movements
        #normal BST descent from curr
        while curr.is_real_node(): #while not leaf
            path += 1
            if key < curr.key: #go left
                if curr.left.is_real_node(): #if exists left son, descend
                    curr = curr.left
                else:#no left son, insert here
                    new_node = self._new_real_node(key, val, curr)
                    curr.left = new_node 
                    break
            elif key > curr.key: #go right
                if curr.right.is_real_node(): #if exists right son, descend
                    curr = curr.right
                else:
                    new_node = self._new_real_node(key, val, curr) #no right son, insert here
                    curr.right = new_node
                    break
            
            
        #rebalance tree in place and adds promote to count
        promote += self.rebalance_after_insert(new_node) 
        return new_node, path + edges, promote 


    def find_max_node(self) -> AVLNode | None:
        current_node = self.root
        while current_node.right.is_real_node():
            current_node = current_node.right
        if not current_node.is_real_node():
            return None
        return current_node
    
    
    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        if not node.is_real_node():
            return
        
        # If the node we are deleting is the root
        if self._size == 1:
            self.root = self.fake_node
            self._max_node = None
            self.height = -1
            self._size = 0
            return
                
        new_max_node = False #check if new max is required
        if node == self._max_node:
            new_max_node = True
        child = node
        parent = node.parent
        
        #node is a leaf -> remove it
        if not (child.left.is_real_node() or child.right.is_real_node()):
            if parent.left == child:
                parent.left = self.fake_node
            else:
                parent.right = self.fake_node
            self.rebalance_tree(parent)
            self._size = self._size - 1

        #node has only left child
        elif not node.right.is_real_node():
            if parent.left == child:
                parent.left = child.left
            else:
                parent.right = child.left
            if child.left.is_real_node():
                child.left.parent = parent
            self.rebalance_tree(node)
            self._size = self._size - 1
    
        #node has only right child
        elif not node.left.is_real_node():
            if parent.left == child:
                parent.left = child.right
            else:
                parent.right = child.right
            if child.right.is_real_node():
                child.right.parent = parent
            self.rebalance_tree(node) #rebalance
            self._size = self._size - 1
        
        #node has two children 
        #recursive - find successor and delete it
        elif node.right.is_real_node():
            successor = node.right
            while successor.left.is_real_node():
                successor = successor.left
            
            node.key, node.value = successor.key, successor.value #lazy deletion
            self.delete(successor) #complete deletion
        
        if new_max_node:
            self._max_node = self.find_max_node()
 
    def rotate_directly_right(self, root: AVLNode) -> AVLNode:
        former_root = root
        new_root = former_root.left
        sub_tree_to_move = new_root.right  # may be fake_node

        parent = former_root.parent

        # hook new_root to parent (or make it the tree root)
        new_root.parent = parent
        if parent == self.fake_node:
            self.root = new_root
        elif parent.left == former_root:
            parent.left = new_root
        else:
            parent.right = new_root

        # rotate
        new_root.right = former_root
        former_root.parent = new_root
        former_root.left = sub_tree_to_move
        if sub_tree_to_move.is_real_node():
            sub_tree_to_move.parent = former_root

        former_root.update_height()
        new_root.update_height()
        return new_root


    def rotate_directly_left(self, root: AVLNode) -> AVLNode:
        former_root = root
        new_root = former_root.right
        sub_tree_to_move = new_root.left  # may be fake_node

        parent = former_root.parent

        # hook new_root to parent (or make it the tree root)
        new_root.parent = parent
        if parent == self.fake_node:
            self.root = new_root
        elif parent.left == former_root:
            parent.left = new_root
        else:
            parent.right = new_root

        # rotate
        new_root.left = former_root
        former_root.parent = new_root
        former_root.right = sub_tree_to_move
        if sub_tree_to_move.is_real_node():
            sub_tree_to_move.parent = former_root

        former_root.update_height()
        new_root.update_height()
        parent.update_height()
        return new_root


 
    def rotate_fully_right(self, root: AVLNode) -> AVLNode:
        """
        make the right subtree higher by 1 and left lower by 1
        """
        left_son = root.left
        #fix left child first if it is right-heavy
        if left_son.is_real_node() and left_son.get_balance() < 0:
            root.left = self.rotate_directly_left(left_son)
        #single right rotation
        return self.rotate_directly_right(root)


    def rotate_fully_left(self, root: AVLNode) -> AVLNode:
        """
        make the left subtree higher by 1 and right lower by 1
        """
        right_son = root.right
      
        #fix right child first if it is left-heavy
        if right_son.is_real_node() and right_son.get_balance() > 0:
            root.right = self.rotate_directly_right(right_son)
        
        #single left rotation
        return self.rotate_directly_left(root)

    #helpers for join/split
    def search_left_by_height(self, height: int) -> AVLNode:
        """
        return the left most node with height or height -1
        """
        current_node = self.root
        while current_node.height > height:
            current_node = current_node.left
        return current_node

    def search_right_by_height(self, height: int) -> AVLNode:
        """
        return the right most node with height or height -1
        """
        current_node = self.root
        while current_node.height > height:
            current_node = current_node.right
        return current_node

    #used after join/split operations:
    def change_tree(self, another_tree) -> None:
        """ 
        change current tree to another tree
        """
        self.root = another_tree.root
        self.height = another_tree.height
        self._size = another_tree._size
        self._max_node = another_tree._max_node
        return
   
   
    def stop_rabalance(self, old_height: int, current_node: AVLNode, did_rotation: int) -> bool:
        #stop if height stayed, but the node is not a leaf (as we saw in class)
        # and change wasn't because of rotation
        # also stop if root
        height_same = current_node.height == old_height 
        not_leaf = current_node.height > 0
        is_root = current_node == self.root
        return is_root or (height_same and not_leaf and not did_rotation)
   

    def rebalance_after_insert(self, start_node: AVLNode) -> int:
        #start at inserted node
        #count promotions
        promote = 0
        current_node = start_node 

        while current_node.is_real_node():
            old_height = current_node.height             
            current_node.update_height() 
            after_update_height = current_node.height
            
            #check if node height changed and is not a leaf
            #if not changed, then change will not be needed upwards
            if after_update_height == old_height and after_update_height > 0:
                promote -= 1 # do not count upward movements made earlier resulted in unchanged parent
                return promote
            
            
            
            #if BF illegal, rotate 
            did_rotation = False
            if current_node.get_balance() < -1:
                current_node = self.rotate_fully_left(current_node)
                did_rotation = True
                promote -= 1 # do not count upward movements made earlier resulted in rotations
            elif current_node.get_balance() > 1:
                current_node = self.rotate_fully_right(current_node)
                did_rotation = True
                promote -= 1  # do not count upward movements made earlier resulted in rotations
                           
            # after insert rotation returns the original height of subtree
            # so rebalance can stop
            #if node is root and balanced -> can stop rebalance
            if did_rotation or current_node == self.root: 
                return promote
            
            current_node = current_node.parent
            promote += 1
        return promote
    

    def rebalance_tree(self, start_node: AVLNode):
        """go through all parents, balance and update heights"""
        current_node = start_node
        while current_node.is_real_node():
            current_node.update_height() #compute height from children
            
            while current_node.get_balance() < -1:
                current_node = self.rotate_fully_left(current_node) #fix right heavy
            while current_node.get_balance() > 1:
                current_node = self.rotate_fully_right(current_node) #fix left heavy
    
            current_node = current_node.parent #move up tree
        return
    
        
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
     
    # in case one tree is empty
        if not tree2.root.is_real_node():
            self.insert(key, val)
            return
        elif not self.root.is_real_node():
            self.change_tree(tree2)
            self.insert(key, val)
            return

        #compare keys
        smaller_tree, bigger_tree = (self, tree2) if tree2.root.key > self.root.key else (tree2, self)
        #compare height
        shorter_tree, higher_tree = (self, tree2) if tree2.height > self.height else (tree2, self)

        smaller_tree_size = smaller_tree._size
        bigger_tree_size = bigger_tree._size
        max_node = bigger_tree._max_node
        #original might be shorter, so original will be added to tree2 and then changed into tree 2
        change_needed_after_joining = higher_tree == tree2

        
        connector = self._new_real_node(key, val, self.fake_node)
  
        if shorter_tree == smaller_tree:
        # add the keys left to the higher_tree
            higher_tree_same_level_node = higher_tree.search_left_by_height(shorter_tree.height)
            parent = higher_tree_same_level_node.parent
            if parent.is_real_node():
                parent.left = connector
            else:
                higher_tree.root = connector
            connector.parent = parent
            connector.right = higher_tree_same_level_node
            connector.left = shorter_tree.root
        else:
        # add the keys right to the higher_tree
            higher_tree_same_level_node = higher_tree.search_right_by_height(shorter_tree.height)
            parent = higher_tree_same_level_node.parent
            if parent.is_real_node():
                parent.right = connector
            else:
                higher_tree.root = connector
            connector.parent = parent
            connector.left = higher_tree_same_level_node
            connector.right = shorter_tree.root
            
        shorter_tree.root.parent = connector #update parent of subtrees
        higher_tree_same_level_node.parent = connector
        
        if change_needed_after_joining:
            self.change_tree(tree2)
        connector.update_height()
        higher_tree.rebalance_tree(connector)

        self._size = bigger_tree_size + smaller_tree_size + 1
        self._max_node = max_node
        self.update_tree_height()
        return


    def make_tree_from_node(self, node: AVLNode):
    # note size and max node are not updated
        tree = AVLTree()
        if node is None or(not node.is_real_node()):
            return tree
        
        tree.root = node
        node.update_height()
        tree.height = node.get_height()
        node.parent = tree.fake_node
        return tree
    


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
        if not node.is_real_node() or not self.root.is_real_node() :
            return AVLTree() , self
        left_child = node.left
        right_child = node.right
        t1 = self.make_tree_from_node(left_child) #smaller than node
        t2 = self.make_tree_from_node(right_child) #bigger than node
            
        current_node = node
        while current_node.parent.is_real_node():
            current_node_is_left_child = current_node.parent.left == current_node
            if current_node_is_left_child:
                sibling = current_node.parent.right
                current_sibling_tree = self.make_tree_from_node(sibling)                 
                t2.join(current_sibling_tree, current_node.parent.key, current_node.parent.value) 
                   
            else:
                sibling = current_node.parent.left
                current_sibling_tree = self.make_tree_from_node(sibling)
                t1.join(current_sibling_tree, current_node.parent.key, current_node.parent.value)
            current_node = current_node.parent
        t1._max_node = t1.find_max_node()
        t2._max_node = t2.find_max_node()
        return t1, t2

    
    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        nodes_array = []
        #using rec in-order walk
        def rec_in_order_walk(node: AVLNode, nodes_array: list) -> None:
            
            if node.is_real_node():
                rec_in_order_walk(node.left, nodes_array)
                nodes_array.append((node.key, node.value))
                rec_in_order_walk(node.right, nodes_array)
    
        rec_in_order_walk(self.root, nodes_array)
        return nodes_array


    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        if self._max_node is None or not self._max_node.is_real_node():
            return None
        return self._max_node

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self._size	


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root

