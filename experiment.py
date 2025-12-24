import random
from AVLTree import AVLTree

TRIALS = 20

def get_swapped_array(n):
    arr = list(range(1, n + 1))
    for i in range(n - 1):
        if random.random() < 0.5:
            arr[i], arr[i+1] = arr[i+1], arr[i]
    return arr

def run_experiment(arr):
    tree = AVLTree()
    search_sum = 0
    balance_sum = 0
    for x in arr:
        _, s_cost, p_cost = tree.finger_insert(x, str(x))
        search_sum += s_cost
        balance_sum += p_cost
    return search_sum, balance_sum

def avg_random(n, kind):
    s_total, b_total = 0, 0
    for _ in range(TRIALS):
        if kind == "Random":
            arr = random.sample(range(1, n+1), n)
        else:
            arr = get_swapped_array(n)
        s, b = run_experiment(arr)
        s_total += s
        b_total += b
    return s_total / TRIALS, b_total / TRIALS


def main():
    
    print(f"{'i':<3} | {'n':<7} | {'Type':<10} | {'Search':<10} | {'Balance':<10}")
    print("-" * 55)

    for i in range(1, 11):
        n = 300 * (2**i)
        
        # ניסויים דטרמיניסטיים (פעם אחת)
        for name, arr in [("Sorted", list(range(1, n+1))), 
                          ("Reverse", list(range(n, 0, -1)))]:
            s, b = run_experiment(arr)
            print(f"{i:<3} | {n:<7} | {name:<10} | {s:<10.1f} | {b:<10.1f}")

        # ניסויים אקראיים (ממוצע 20)
        for name in ["Random", "Swaps"]:
            s_total, b_total = 0, 0
            for _ in range(20):
                arr = random.sample(range(1, n+1), n) if name == "Random" else get_swapped_array(n)
                s, b = run_experiment(arr)
                s_total += s
                b_total += b
            print(f"{i:<3} | {n:<7} | {name:<10} | {s_total/20:<10.1f} | {b_total/20:<10.1f}")

if __name__ == "__main__":
    main()
