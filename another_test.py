
from AVLTree import AVLTree
from avl_tree_visualiser import print_pyramid 

def run_promote_demo():
    print("="*80)
    print("🚀 EXTENDED AVL PROMOTE & VISUALIZATION TESTER")
    print("="*80)
    
    T = AVLTree()
    
    # שלב 1: הכנסת שורש
    print("\n--- STEP 1: Insert 20 (Root) ---")
    node, path, promote = T.insert(20, "root")
    print_pyramid(T)
    print(f"Result: Path={path}, Promote={promote} | Expected: Path=0, Promote=0")

    # שלב 2: הוספת בן
    print("\n--- STEP 2: Insert 30 (Create Right Child) ---")
    node, path, promote = T.insert(30, "child")
    print_pyramid(T)
    print(f"Result: Path={path}, Promote={promote} | Expected: Path=1, Promote=1")

    # שלב 3: גלגול RR (פשוט)
    print("\n--- STEP 3: Insert 40 (Trigger RR Rotation) ---")
    # לפני הגלגול: 20 -> 30 -> 40. אחרי הגלגול: 30 שורש, 20 ו-40 בנים.
    node, path, promote = T.insert(40, "rotate")
    print_pyramid(T)
    print(f"Result: Path={path}, Promote={promote} | Expected: Path=2, Promote=1")

    # שלב 4: Finger Insert - עדכון גובה ללא גלגול (Propagation)
    # מסלול: 40(up)->30(up)->20(down)->10(new)
    # גובה 20 משתנה (0->1), גובה 30 משתנה (1->2).
    print("\n--- STEP 4: Finger Insert 10 (Search from Max=40) ---")
    node, search_cost, promote = T.finger_insert(10, "finger")
    print_pyramid(T)
    print(f"Result: Search Cost={search_cost}, Promote={promote} | Expected: Search=3, Promote=2")

    # שלב 5: הכנסה שגורמת לגלגול LL
    # מסלול: 30 -> 20 -> 10 -> 5. גלגול ב-20.
    print("\n--- STEP 5: Insert 5 (Trigger LL Rotation) ---")
    node, path, promote = T.insert(5, "deep_left")
    print_pyramid(T)
    print(f"Result: Path={path}, Promote={promote} | Expected: Path=3, Promote=1")

    # שלב 6: מקרה גלגול כפול RL (Right-Left)
    # נכניס 35. המקסימום הוא 40.
    # 35 קטן מ-40, גדול מ-30. יוכנס כבן שמאלי של 40.
    print("\n--- STEP 6: Finger Insert 35 (Trigger RL Rotation) ---")
    node, search_cost, promote = T.finger_insert(35, "double_rotate")
    print_pyramid(T)
    # מסלול מ-40 ל-35: 40(up)->30(up)->40(down)->35. סה"כ 3 קשתות.
    # גלגול RL ב-30 יספוג את הגובה.
    print(f"Result: Search Cost={search_cost}, Promote={promote} | Expected: Search=3, Promote=1")

    # שלב 7: הכנסה גדולה מאוד (עדכון מקסימום וגובה שורש)
    print("\n--- STEP 7: Insert 50 (New Maximum) ---")
    node, path, promote = T.insert(50, "new_max")
    print_pyramid(T)
    # מסלול: 30 -> 40 -> 50 (2 קשתות). גובה 40 עולה ל-1, גובה 30 עולה ל-2.
    print(f"Result: Path={path}, Promote={promote} | Expected: Path=2, Promote=2")

    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80)

if __name__ == "__main__":
    run_promote_demo()