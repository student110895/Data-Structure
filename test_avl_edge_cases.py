from AVLTree import AVLTree
from avl_tree_visualiser import print_pyramid, print_tree_ascii

def test_cases():
    # --- Case 1: Double Rotation (LR) ---
    print("\n=== Case 1: Double Rotation (Left-Right) ===")
    t1 = AVLTree()
    for k in [10, 5, 7]:
        print(f"Inserting {k}...")
        t1.insert(k, str(k))
    print("Result (Should have 7 as root):")
    print_tree_ascii(t1)

    # --- Case 2: Complex Deletion (Root with 2 children) ---
    print("\n=== Case 2: Deletion of Root (Two Children + Rebalance) ===")
    t2 = AVLTree()
    # Build a balanced tree
    for k in [10, 5, 15, 3, 7, 12, 20]:
        t2.insert(k, str(k))
    print("Before deleting 10:")
    print_tree_ascii(t2)
    
    node_to_del, _ = t2.search(10)
    t2.delete(node_to_del)
    print("After deleting 10 (Successor 12 should move up):")
    print_tree_ascii(t2)

    # --- Case 3: Joining Trees of Different Heights ---
    print("\n=== Case 3: Join (Height 0 tree + Height 2 tree) ===")
    # Small tree (Left side)
    left_t = AVLTree()
    left_t.insert(2, "2")
    
    # Larger tree (Right side)
    right_t = AVLTree()
    for k in [10, 8, 15, 12, 20]:
        right_t.insert(k, str(k))
    
    print("Left Tree:")
    print_tree_ascii(left_t)
    print("Right Tree:")
    print_tree_ascii(right_t)
    
    print("Joining with key 5...")
    left_t.join(right_t, 5, "5")
    print("Resulting Joined Tree:")
    print_tree_ascii(left_t)
    print(f"New Size: {left_t.size()}, New Max: {left_t.max_node.key}")


def test_split():
    print("\n=== Case: Splitting at the Root ===")
    t = AVLTree()
    for k in [10, 5, 15, 3, 7, 12, 20]:
        t.insert(k, str(k))
    
    print("Original Tree:")
    print_tree_ascii(t)
    
    root_node = t.get_root()
    left_tree, right_tree = t.split(root_node)
    
    print("Left Tree (Keys < 10):")
    print_tree_ascii(left_tree)
    print("Right Tree (Keys > 10):")
    print_tree_ascii(right_tree)
    


def run_extreme_tests():
    # --- Case 1: Split at the Root ---
    print("\n" + "="*50)
    print("EXTREME CASE 1: SPLIT AT THE ROOT")
    t1 = AVLTree()
    for k in [10, 5, 15, 3, 7, 12, 20]:
        t1.insert(k, str(k))
    print("Full tree before split:")
    print_tree_ascii(t1)
    
    root_node = t1.get_root()
    left_t, right_t = t1.split(root_node)
    
    print("\nLeft Tree (Smaller than 10):")
    print_tree_ascii(left_t)
    print("\nRight Tree (Larger than 10):")
    print_tree_ascii(right_t)

    # --- Case 2: Split at a Leaf (Minimum Node) ---
    print("\n" + "="*50)
    print("EXTREME CASE 2: SPLIT AT A LEAF (KEY 3)")
    t2 = AVLTree()
    for k in [10, 5, 15, 3, 7, 12, 20]:
        t2.insert(k, str(k))
    
    node_3, _ = t2.search(3)
    left_t2, right_t2 = t2.split(node_3)
    
    print("Left Tree (Should be empty):")
    print_tree_ascii(left_t2)
    print("\nRight Tree (Everything except 3):")
    print_tree_ascii(right_t2)

    # --- Case 3: Joining Identical Height Trees ---
    print("\n" + "="*50)
    print("EXTREME CASE 3: JOIN IDENTICAL HEIGHTS")
    tree_a = AVLTree()
    for k in [1, 2, 3]: tree_a.insert(k, str(k))
    tree_b = AVLTree()
    for k in [5, 6, 7]: tree_b.insert(k, str(k))
    
    print("Joining Tree [1,2,3] and [5,6,7] with connector 4...")
    tree_a.join(tree_b, 4, "4")
    print_tree_ascii(tree_a)

    # --- Case 4: Cascading Rotations (The 'Zig-Zag' Delete) ---
    print("\n" + "="*50)
    print("EXTREME CASE 4: CASCADING ROTATIONS ON DELETE")
    # Building a specific unbalanced tree:
    t4 = AVLTree()
    # Inserting in an order that creates a right-leaning structure
    for k in [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35, 55]:
        t4.insert(k, str(k))
    
    print("Tree before complex deletion:")
    print_tree_ascii(t4)
    # Deleting a node that should trigger rebalancing multiple levels up
    node_to_del, _ = t4.search(80)
    t4.delete(node_to_del)
    print("\nAfter deleting 80 (Check if root or sub-roots rotated):")
    print_tree_ascii(t4)

    # --- Case 5: Finger Search on Single Node ---
    print("\n" + "="*50)
    print("EXTREME CASE 5: FINGER SEARCH ON SINGLE NODE")
    t5 = AVLTree()
    t5.insert(100, "100")
    print("Searching for 50 (smaller than only node) using Finger Search...")
    node, edges = t5.finger_search(50)
    print(f"Result: Found {node} with {edges} edges.")
    print(f"Max node is: {t5.max_node.key}")


def test_complex_deletions():
    # --- Case 1: Cascading Double Rotation ---
    print("\n" + "="*50)
    print("DELETE CASE 1: CASCADING ROTATIONS (Double Ripple)")
    # This specific sequence creates a tree where height changes propagate
    t1 = AVLTree()
    # Build a left-heavy tree
    for k in [50, 30, 70, 20, 40, 80, 10]:
        t1.insert(k, str(k))
    
    print("Tree before deleting 80:")
    print_tree_ascii(t1)
    
    node_80, _ = t1.search(80)
    t1.delete(node_80)
    
    print("\nAfter deleting 80: (Should trigger rotation at sub-root and root)")
    print_tree_ascii(t1)

    # --- Case 2: Deletion triggers a Double Rotation (RL) ---
    print("\n" + "="*50)
    print("DELETE CASE 2: TRIGGER RL DOUBLE ROTATION")
    t2 = AVLTree()
    # Constructing a right-heavy zig-zag
    for k in [30, 20, 50, 40, 60, 35]:
        t2.insert(k, str(k))
    
    print("Tree before deleting 20:")
    print_tree_ascii(t2)
    
    node_20, _ = t2.search(20)
    t2.delete(node_20)
    
    print("\nAfter deleting 20: (Node 50 was RL heavy, should rebalance at 30)")
    print_tree_ascii(t2)

    # --- Case 3: The "Deep Successor" Rebalance ---
    print("\n" + "="*50)
    print("DELETE CASE 3: DEEP SUCCESSOR REBALANCE")
    t3 = AVLTree()
    # Create a tree where the successor is deep in the right subtree
    for k in [40, 20, 60, 10, 30, 50, 70, 45]:
        t3.insert(k, str(k))
    
    print("Tree before deleting root (40):")
    print_tree_ascii(t3)
    
    node_40, _ = t3.search(40)
    t3.delete(node_40)
    
    print("\nAfter deleting 40: (Successor 45 moves to root, rebalance starts at its old parent 50)")
    print_tree_ascii(t3)

def test_max_node_integrity():
    print("\n" + "="*50)
    print("MAX_NODE INTEGRITY TEST")
    t = AVLTree()
    
    # 1. Build a tree
    keys = [50, 30, 70, 20, 40, 60, 80]
    for k in keys:
        t.insert(k, str(k))
    
    print("Initial Tree:")
    print_tree_ascii(t)
    print(f"Current Max: {t.max_node.key}") # Should be 80
    
    # 2. Delete the Max (Leaf)
    print("\n--- Deleting 80 (The Max Leaf) ---")
    node_80, _ = t.search(80)
    t.delete(node_80)
    print_tree_ascii(t)
    print(f"New Max: {t.max_node.key}") # Should be 70
    
    # 3. Delete the Max (Node with a Left Child)
    # First, let's insert 65 to give 70 a left child
    print("\n--- Inserting 65 and then Deleting 70 (The New Max) ---")
    t.insert(65, "65")
    node_70, _ = t.search(70)
    t.delete(node_70)
    
    print_tree_ascii(t)
    # After 70 is gone, 65 should be the new max
    print(f"Final Max: {t.max_node.key}") 

def test_drain_tree():
    print("\n" + "="*50)
    print("THE DRAIN TEST (Deleting to Empty)")
    t = AVLTree()
    nums = list(range(1, 11))
    for n in nums:
        t.insert(n, str(n))
    
    print(f"Tree size before draining: {t.size()}")
    
    for n in nums:
        node, _ = t.search(n)
        t.delete(node)
        
    print(f"Tree size after draining: {t.size()}")
    print(f"Root is real node: {t.get_root().is_real_node()}")
    if not t.get_root().is_real_node():
        print("Success: Tree is empty and root is a fake node.")

def test_split_max_node():
    print("\n" + "="*50)
    print("TEST: MAX_NODE UPDATE AFTER SPLIT")
    
    # 1. Setup a tree
    # Inserting keys that create a varied structure
    t = AVLTree()
    keys = [50, 25, 75, 10, 30, 60, 90, 80, 100]
    for k in keys:
        t.insert(k, str(k))
    
    print("Original Tree:")
    print_tree_ascii(t)
    print(f"Original Tree Max: {t.max_node.key}") # Should be 100
    
    # 2. Split at a middle-right node (75)
    # This will put [10, 25, 30, 50, 60] in T1
    # And [80, 90, 100] in T2
    print("\nSplitting at node 75...")
    split_node, _ = t.search(75)
    t1, t2 = t.split(split_node)
    
    print("\n--- Tree T1 (Keys < 75) ---")
    print_tree_ascii(t1)
    if t1.max_node and t1.max_node.is_real_node():
        print(f"T1 Max Node: {t1.max_node.key} (Expected: 60)")
    else:
        print("T1 Max Node: None")

    print("\n--- Tree T2 (Keys > 75) ---")
    print_tree_ascii(t2)
    if t2.max_node and t2.max_node.is_real_node():
        print(f"T2 Max Node: {t2.max_node.key} (Expected: 100)")
    else:
        print("T2 Max Node: None")

    # 3. Edge Case: Split at the actual Max (100)
    print("\n" + "-"*30)
    print("Edge Case: Splitting at the maximum node (100)")
    # Re-build t
    t_edge = AVLTree()
    for k in [50, 25, 75]: t_edge.insert(k, str(k))
    
    max_node, _ = t_edge.search(75)
    t_small, t_empty = t_edge.split(max_node)
    
    print(f"T_small Max: {t_small.max_node.key} (Expected: 50)")
    print(f"T_empty Root is Real: {t_empty.get_root().is_real_node()} (Expected: False)")

if __name__ == "__main__":
    test_split_max_node()