import math
import heapq

COPYPASTA = True
MAXIMIZE = True
MIN_COUNT = 1

def frobenius(numbers: list[int]) -> int | float:
    """
    Calculates the Frobenius number for a list of positive integers.
    
    Returns:
        int: The largest integer that cannot be formed as a non-negative 
             linear combination of the given numbers.
        float('inf'): If gcd of the set is > 1 (infinitely many numbers cannot be formed).
        -1: If 1 is in the set (all non-negative integers can be formed).
    """
    # Remove non-positive integers and duplicate elements
    nums = sorted(set(x for x in numbers if x > 0))
    if not nums:
        raise ValueError("Input list must contain at least one positive integer.")

    # 1. Check if gcd equals 1
    if math.gcd(*nums) != 1:
        return float('inf')

    # 2. Base case: If 1 is present, 0 is the smallest and every integer is reachable
    if nums[0] == 1:
        return -1

    # 3. Dijkstra's algorithm over residue classes modulo a1 (smallest generator)
    a1 = nums[0]
    dist = [float('inf')] * a1
    dist[0] = 0
    pq = [(0, 0)]  # (distance, remainder_class)

    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
            
        for x in nums[1:]:
            v = (u + x) % a1
            if dist[u] + x < dist[v]:
                dist[v] = dist[u] + x
                heapq.heappush(pq, (dist[v], v))

    # The Frobenius number is max(dist[v]) - a1
    return max(dist) - a1

def procure(items: dict, budget: int) -> dict:
    """
    Finds the combination of items that maximally utilizes the given budget.
    
    :param items: Dictionary of {item_name: unit_price}
    :param budget: Total budget available (integer)
    :return: Dictionary of {item_name: count} for the optimal purchase
    """
    # Filter out invalid or non-positive prices
    valid_items = {item: price for item, price in items.items() if price > 0}
    
    if not valid_items or budget <= 0:
        return {}

    # dp[w] stores the maximum total price achievable with a budget capacity of w
    dp = [0] * (budget + 1)
    # best_item[w] stores the item chosen to achieve dp[w]
    best_item = [None] * (budget + 1)

    # Compute maximum spend for each capacity up to budget
    for w in range(1, budget + 1):
        # Default: carry forward optimal spend from capacity (w - 1)
        dp[w] = dp[w - 1]

        for item, price in valid_items.items():
            if price <= w:
                cand = dp[w - price] + price
                if cand > dp[w]:
                    dp[w] = cand
                    best_item[w] = item

    # Backtrack from budget capacity to reconstruct item counts
    result = {}
    curr = budget
    while curr > 0 and dp[curr] > 0:
        if best_item[curr] is None:
            curr -= 1
        else:
            item = best_item[curr]
            result[item] = result.get(item, 0) + 1
            curr -= valid_items[item]

    return result


def gini(values):
    values = sorted(values)
    n = len(values)

    if n == 0:
        raise ValueError("List cannot be empty")
    if any(x < 0 for x in values):
        raise ValueError("Values must be non-negative")

    total = sum(values)
    if total == 0:
        return 0.0

    weighted_sum = sum((i + 1) * x for i, x in enumerate(values))

    return (2 * weighted_sum) / (n * total) - (n + 1) / n

plurals = {
  "box": "boxes"
}

target_budget = 0
items_to_procure = {}

def pap_5020301001():
    global target_budget, items_to_procure
    target_budget = 29125
    items_to_procure = {
    # "Certificate Paper (A4 Size (210 mm × 297 mm), 200 GSM, White, Matte Finish, 100 sheets/ream)": (400, "ream"),  # 3 reams
    # "Certificate Holder (A4 Size, compatible with A4 certificates (210 mm × 297 mm), 50 pcs./box)": (2500, "box"),  # 3 boxes
    # "Copy Paper (A4 Size (210 mm × 297 mm), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream)": (300, "ream"),  # 5 reams
    # "Copy Paper (Folio Size (8.5\" × 13\"), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream)": (350, "ream"),  # 6 reams
    # "Ink Printer set (003 Genuine Ink Bottle, (Black, Cyan, Magenta, Yellow), Dye-Based, Original EcoTank Refill)": (1200, "set"),
    # "Ink Printer set ( HP 32XL black bottles, HP 31 color bottle (Cyan, Magenta, Yellow) )": (1225, "set"),
    "Sign Pen (Fine Tip, Black)": (25, "pen"),
    "Folder (Folio Size (9\" x 14\"), with tab)": (12, "folder"),
    "Markers (Black, Permanent)": (16, "marker"),
    # "Clip (50mm, Backfold, 12 pieces per box)": (63, "box"),
    # "Paper Clip (50mm, Vinyl/Plastic Coated, Jumbo, 100 pieces per box)": (17, "box"),
    }

    print("- Certificate Paper (A4 Size (210 mm × 297 mm), 200 GSM, White, Matte Finish, 100 sheets/ream): 400.00 X 3 reams = 1,200.00")
    target_budget -= 1200

    print("- Certificate Holder (A4 Size, compatible with A4 certificates (210 mm × 297 mm), 50 pcs./box): 2,500.00 X 3 boxes = 7,500.00")
    target_budget -= 7500

    print("- Bond Paper (A4 Size (210 mm × 297 mm), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream): 300.00 X 5 reams = 1,500.00")
    target_budget -= 1500

    print("- Bond Paper (Legal Size (8.5\" × 13\"), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream): 350.00 X 6 reams = 2,100.00")
    target_budget -= 2100

    print("- Ink Printer set (003 Genuine Ink Bottle, (Black, Cyan, Magenta, Yellow), Dye-Based, Original EcoTank Refill): 1,200.00 x 5 set = 6,000.00")
    target_budget -= 6000

    print("- Ink Printer set ( HP 32XL black bottles, HP 31 color bottle (Cyan, Magenta, Yellow) ): 1,225.00 x 5 set = 6,125.00")
    target_budget -= 6125


def obj_5021199000():
    global target_budget, items_to_procure
    target_budget = 6200
    items_to_procure = {
    "Presentation Clicker (Wireless, with Laser)": (400, "clicker"),
    "HDMI (Wireless)": (2750, "set"),
    }

obj_5021199000()

i = 0
best_result = None
best_gini_coeff = 1

to_procure = {k: v[0] for k, v in items_to_procure.items()}

if MAXIMIZE:
    bdgt = target_budget - sum([x * MIN_COUNT for x in to_procure.values()])
    if bdgt > 0:
        best_result = procure(to_procure, bdgt)
        for k in to_procure.keys():
            best_result[k] = best_result.get(k, 0) + MIN_COUNT
        best_gini_coeff = gini(list(best_result.values()))
else:
    while True:
        bdgt = target_budget - sum([x * i for x in to_procure.values()])
        if bdgt <= 0: break

        result = procure(to_procure, bdgt)
        for k in to_procure.keys():
            result[k] = result.get(k, 0) + i
        
        gini_coeff = gini(list(result.values()))

        utilization = 0
        for k, v in result.items():
            utilization += to_procure[k] * v

        if best_result is None \
        or best_gini_coeff > gini_coeff:
            best_result = result
            best_gini_coeff = gini_coeff
        i += 1


utilization = 0
itemList = []
for item in to_procure:
  item_value = items_to_procure[item][0]
  item_unit = items_to_procure[item][1]
  item_count = best_result.get(item, 0)
  item_total_cost = item_value * item_count

  # unit
  item_unit_plural = plurals.get(item_unit, item_unit + 's')
  
  item_print_name = item
  if not COPYPASTA:
    item_print_name = item[:item.find("(")]

  itemList += [(f"{item_print_name}: {item_value:,.2f} x {item_count} {item_unit_plural if item_count > 1 else item_unit}", f"{item_total_cost:,.2f}")]
  utilization += item_total_cost

maxItemStrlen = max(len(x[0]) for x in itemList)

for x in itemList:
  if COPYPASTA:
    print(f"- {x[0]} = {x[1]}")
  else:
    print(f"{' '*(maxItemStrlen - len(x[0]))}{x[0]} = {x[1]}")

print(f"\nTotal: {utilization:,.2f}/{target_budget:,.2f}")
print(f"Gini Coefficient: {best_gini_coeff}")