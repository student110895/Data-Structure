# ---------------------------------------------------------
# avl_tree_visualizer.py
# Standalone AVL tree visualization tool.
# Works with your AVLTree.py implementation.
# ---------------------------------------------------------

from AVLTree import AVLTree, AVLNode


# =========================================================
#   ROTATED (VERTICAL) TREE PRINT
# =========================================================

def _print_subtree_vertical(node, indent="", last=True):
    """Pretty-print the AVL subtree vertically (rotated)."""
    if node is None or not node.is_real_node():
        return

    print(indent + ("`-- " if last else "|-- ") + f"{node.key} (h={node.height})")

    indent += "    " if last else "|   "

    children = []
    if node.left and node.left.is_real_node():
        children.append(node.left)
    if node.right and node.right.is_real_node():
        children.append(node.right)

    for i, child in enumerate(children):
        _print_subtree_vertical(child, indent, i == len(children) - 1)


def print_tree_vertical(tree: AVLTree):
    """Public wrapper for vertical tree printing."""
    if tree.root is None or not tree.root.is_real_node():
        print("<empty AVL>")
        return
    _print_subtree_vertical(tree.root)


# =========================================================
#   ASCII (HORIZONTAL) TREE PRINT
# =========================================================
def _build_ascii_tree(node):
    """
    Returns: (lines, width, height, middle)
    lines: list[str] drawing this subtree
    width: total width of drawing
    height: number of lines
    middle: x-index (column) of the root label center in the drawing
    """
    if node is None or not node.is_real_node():
        return [], 0, 0, 0

    # Make the label compact + stable width
    bf = node.left.height - node.right.height
    label = f"({bf},{node.key},{node.height})"
    u = len(label)

    left_lines, left_w, left_h, left_mid = _build_ascii_tree(node.left)
    right_lines, right_w, right_h, right_mid = _build_ascii_tree(node.right)

    # Leaf
    if left_h == 0 and right_h == 0:
        return [label], u, 1, u // 2

    # Make both sides the same height by padding with spaces
    height = max(left_h, right_h)
    left_lines  = left_lines  + [" " * left_w]  * (height - left_h)
    right_lines = right_lines + [" " * right_w] * (height - right_h)

    # Gap between left block and right block under the label
    gap = 2  # feel free to change to 1/3
    total_w = left_w + gap + right_w

    # Where do we want the label center to sit?
    # If a side doesn't exist, fall back to edge.
    if left_w > 0 and right_w > 0:
        root_mid = left_mid + gap + right_mid  # between the two subtree centers
        root_mid //= 2
    elif left_w > 0:
        root_mid = left_mid
    else:
        root_mid = left_w + gap + right_mid

    # Put the label so its center is at root_mid
    label_start = max(0, root_mid - (u // 2))
    # Ensure label fits inside total_w (expand if needed)
    needed_w = label_start + u
    if needed_w > total_w:
        total_w = needed_w

    # First line (label line)
    first = [" "] * total_w
    first[label_start:label_start + u] = list(label)
    first_line = "".join(first)

    # Second line (connectors)
    second = [" "] * total_w
    label_center = label_start + (u // 2)

    if left_w > 0:
        left_x = left_mid
        second[left_x] = "/"
        # draw a horizontal run up to under the label
        for x in range(left_x + 1, label_center):
            if second[x] == " ":
                second[x] = "_"

    if right_w > 0:
        right_x = left_w + gap + right_mid
        second[right_x] = "\\"
        for x in range(label_center + 1, right_x):
            if second[x] == " ":
                second[x] = "_"

    second_line = "".join(second)

    # Merge children lines with the same total width
    merged = []
    for i in range(height):
        left_part = left_lines[i] if left_w > 0 else ""
        right_part = right_lines[i] if right_w > 0 else ""
        line = left_part.ljust(left_w) + (" " * gap) + right_part.ljust(right_w)
        merged.append(line.ljust(total_w))

    return [first_line, second_line] + merged, total_w, height + 2, label_center





def print_tree_ascii(tree: AVLTree):
    """Prints the tree using a horizontal ASCII diagram."""
    if tree.root is None or not tree.root.is_real_node():
        print("<empty AVL>")
        return

    lines, *_ = _build_ascii_tree(tree.root)
    for line in lines:
        print(line)


# =========================================================
#   DEMO (RUN THIS FILE DIRECTLY)
# =========================================================

if __name__ == "__main__":
    print("Building sample AVL tree...\n")
   

    

    
    T = AVLTree()

    for k in [3, 1, 2]:
        T.insert(k, str(k))

        print(f"\nAfter inserting {k}:")
        r = T.root
        print(f"root.key={r.key}, height={r.height}, balance={r.get_balance()}")
        print_tree_vertical(T)
