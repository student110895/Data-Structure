import random
import math
import time
from AVLTree import AVLTree

def count_inversions(arr):
    """
    מחשב את מספר ההיפוכים במערך.
    הערה: עבור n גדול זה עשוי להיות איטי (O(n^2)). 
    בניסויים גדולים מומלץ להשתמש ב-Merge Sort מותאם.
    """
    if len(arr) > 5000: return "Too large" # חסכון בזמן ריצה ל-i גבוה
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def get_random_swaps_array(n):
    arr = list(range(1, n + 1))
    for i in range(n - 1):
        if random.random() < 0.5:
            arr[i], arr[i+1] = arr[i+1], arr[i]
    return arr

def run_experiment(n, array_type):
    total_search_cost = 0
    total_balance_cost = 0
    
    # יצירת המערך לפי הסוג
    if array_type == "sorted":
        arr = list(range(1, n + 1))
    elif array_type == "reverse":
        arr = list(range(n, 0, -1))
    elif array_type == "random":
        arr = list(range(1, n + 1))
        random.shuffle(arr)
    elif array_type == "swaps":
        arr = get_random_swaps_array(n)
        
    tree = AVLTree()
    for x in arr:
        # שימוש ב-finger_insert שמחזיר (node, search_cost, promote_cost)
        _, s_cost, p_cost = tree.finger_insert(x, str(x))
        total_search_cost += s_cost
        total_balance_cost += p_cost
        
    return total_search_cost, total_balance_cost, arr

def main():
    print(f"{'i':<3} | {'n':<6} | {'Type':<10} | {'Search Cost':<12} | {'Balance Cost':<12} | {'Inversions':<10}")
    print("-" * 85)
    
    for i in range(1, 11):
        n = 300 * (2**i)
        for t in ["sorted", "reverse", "random", "swaps"]:
            if t in ["random", "swaps"]:
                s_sum, b_sum, inv_sum = 0, 0, 0
                inv_is_string = False
                iterations = 20
                for _ in range(iterations):
                    s, b, arr = run_experiment(n, t)
                    s_sum += s
                    b_sum += b
                    res_inv = count_inversions(arr)
                    if isinstance(res_inv, str):
                        inv_is_string = True
                    elif not inv_is_string:
                        inv_sum += res_inv
                
                avg_s = s_sum / iterations
                avg_b = b_sum / iterations
                avg_inv = "Too large" if inv_is_string else (inv_sum / iterations)
                print(f"{i:<3} | {n:<6} | {t:<10} | {avg_s:<12.1f} | {avg_b:<12.1f} | {avg_inv}")
            else:
                s, b, arr = run_experiment(n, t)
                inv = count_inversions(arr)
                print(f"{i:<3} | {n:<6} | {t:<10} | {s:<12.1f} | {b:<12.1f} | {inv}")
                
                
if __name__ == "__main__":
    main()