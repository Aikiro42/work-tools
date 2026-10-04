import math
import heapq

COPYPASTA = True
MAXIMIZE = False
MIN_COUNT = 1

DEBUG_GINI = False
PRINT_GINI = False

def frobenius(prices: list[int]) -> int | float:
    """
    Calculates the the maximum budget that cannot be 100% utilized
    given the list of prices.
    
    Returns:
        int: The maximum budget that cannot be fully utilized given the prices.
        float('inf'): If gcd of the set is > 1 (No maximum underutilized budget).
        -1: If 1 is in the set. What the fuck are we procuring, candy?
    """
    numbers = prices
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


def gini(item_counts):
    """
    Given a list of item counts, returns a decimal number between 0 and 1 (inclusive)
    that describes how evenly distributed the counts are. The more evenly distributed the numbers are,
    the closer the value is to 0.
    """
    values = item_counts
    # print(f"[DEBUG] Calculating gini coefficient of {values}")
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
budget_offset = 0
items_to_procure = {}
determined_procurements = {}
excluded_items = []
filler_item = ""
filler_items = []
missing_decimal = 0

def obj_5020301001():
    global target_budget, budget_offset, items_to_procure, filler_item, filler_items, determined_procurements, excluded_items, missing_decimal
    target_budget = 29125
    """
    - Sign Pen (Fine Tip, Black): 25.00 x 88 pens = 2,200.00
    - Folder (Folio Size (9" x 14"), with tab): 12.00 x 91 folders = 1,092.00
    - Markers (Black, Permanent): 16.00 x 88 markers = 1,408.00
    """
    items_to_procure = {
        # Certificate Paper
        "Certificate Paper (A4 Size (210 mm × 297 mm), 200 GSM, White, Matte Finish, 100 sheets/ream)": (400, "ream"),  # 3 reams
        "Certificate Holder (A4 Size, compatible with A4 certificates (210 mm × 297 mm), 50 pcs./box)": (2500, "box"),  # 3 boxes
        
        # Certificate holder
        "Copy Paper (A4 Size (210 mm × 297 mm), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream)": (300, "ream"),  # 5 reams
        "Copy Paper (Folio Size (8.5\" × 13\"), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream)": (350, "ream"),  # 6 reams
    
        # Printer Ink
        "Ink Printer set (003 Genuine Ink Bottle, (Black, Cyan, Magenta, Yellow), Dye-Based, Original EcoTank Refill)": (1200, "set"),  # OLD
        "Ink Printer set (HP 32XL black bottles, HP 31 color bottle (Cyan, Magenta, Yellow))": (1225, "set"),
        
        "Printer Ink (Epson 664, Black, 70mL, 4 btl./bundle)": (640, "bundle"),
        "Printer Ink (Epson 664, Cyan, 70mL, 4 btl./bundle)": (640, "bundle"),
        "Printer Ink (Epson 664, Magenta, 70mL, 4 btl./bundle)": (640, "bundle"),
        "Printer Ink (Epson 664, Yellow, 70mL, 4 btl./bundle)": (640, "bundle"),
        
        "Printer Ink (Epson 664, Black, 70mL)": (236, "bottle"),
        "Printer Ink (Epson 664, Cyan, 70mL)": (246, "bottle"),
        "Printer Ink (Epson 664, Magenta, 70mL)": (246, "bottle"),
        "Printer Ink (Epson 664, Yellow, 70mL)": (246, "bottle"),
    
        # Markers
        "Markers (Black, Permanent)": (16, "marker"),  # PER PIECE
        "Markers (Black, Permanent, 12 pcs./box)": (50, "box"),  # OLD
        "Markers (Black, 12 pcs./box)": (50, "box"),
        "Markers (Red, 12 pcs./box)": (50, "box"),
        "Markers (Blue, 12 pcs./box)": (50, "box"),
        
        # Pens
        "Sign Pen (Dong-A MyGel, 0.5mm, Black)": (25, "pen"),  # PER PIECE
        "Sign Pen (Dong-A MyGel, 0.5mm, Black, 12 pcs./box)": (259, "box"),
        
        # Folders
        "Folder (Folio Size (9\" x 14\"), with tab)": (12, "folder"),
        "Folder (Letter Size (9\" x 12\"), with tab)": (10, "folder"),
    
        # Clips
        "Clip (50mm, Backfold, 12 pieces per box)": (63, "box"),
        "Paper Clip (50mm, Vinyl/Plastic Coated, Jumbo, 100 pieces per box)": (17, "box"),
    }

    determined_procurements = {
        "Certificate Paper (A4 Size (210 mm × 297 mm), 200 GSM, White, Matte Finish, 100 sheets/ream)": 3,
        "Certificate Holder (A4 Size, compatible with A4 certificates (210 mm × 297 mm), 50 pcs./box)": 3,
        "Copy Paper (A4 Size (210 mm × 297 mm), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream)": 5,
        "Copy Paper (Folio Size (8.5\" × 13\"), 80 GSM, White, Multipurpose Copy Paper, 500 sheets per ream)": 6,
        "Ink Printer set (HP 32XL black bottles, HP 31 color bottle (Cyan, Magenta, Yellow))": 5,
        "Sign Pen (Dong-A MyGel, 0.5mm, Black, 12 pcs./box)": 5,
        "Folder (Folio Size (9\" x 14\"), with tab)": 35,
        "Folder (Letter Size (9\" x 12\"), with tab)": 35,
        "Markers (Black, 12 pcs./box)": 5,
        "Markers (Red, 12 pcs./box)": 5,
        "Markers (Blue, 12 pcs./box)": 5,
        
        # Excluded
        "Ink Printer set (003 Genuine Ink Bottle, (Black, Cyan, Magenta, Yellow), Dye-Based, Original EcoTank Refill)": 5,
    }

    excluded_items = [
        "Ink Printer set (003 Genuine Ink Bottle, (Black, Cyan, Magenta, Yellow), Dye-Based, Original EcoTank Refill)",

        "Printer Ink (Epson 664, Black, 70mL, 4 btl./bundle)",
        "Printer Ink (Epson 664, Cyan, 70mL, 4 btl./bundle)",
        "Printer Ink (Epson 664, Magenta, 70mL, 4 btl./bundle)",
        "Printer Ink (Epson 664, Yellow, 70mL, 4 btl./bundle)",
        
        "Sign Pen (Dong-A MyGel, 0.5mm, Black)",

        "Markers (Black, Permanent)",
        "Markers (Black, Permanent, 12 pcs./box)",

        "Clip (50mm, Backfold, 12 pieces per box)",
        "Paper Clip (50mm, Vinyl/Plastic Coated, Jumbo, 100 pieces per box)",
    ]
    
    filler_item = "Printer Ink (Epson 664, Black, 70mL)"


def obj_5021199000(): 
    global target_budget, budget_offset, items_to_procure, filler_item, filler_items, determined_procurements, excluded_items, missing_decimal
    target_budget = 6200
    items_to_procure = {
        "Presentation Clicker (Wireless, with Laser)": (400, "clicker"),
        "HDMI (Wireless)": (2750, "set"),
        "Flash Drive (64GB Capacity)": (175, "drive"),  # philgeps item code 43202010-FD-U04
    }
    determined_procurements = {
        "Presentation Clicker (Wireless, with Laser)": 6
    }


def obj_5020321003(): 
    global target_budget, budget_offset, items_to_procure, filler_item, filler_items, determined_procurements, excluded_items, missing_decimal
    target_budget = 237323
    missing_decimal = 0.72
    items_to_procure = {
        "dslr": (49998, "set"),
        "monitor": (6500, "unit"),
        "macbook": (49999, "unit"),
        "hdd": (5000, "unit"),
        "ssd": (9500, "unit"),
    }
    determined_procurements = {
        "hdd": 8,  # 1 per team member
        "ssd": 5,  # 1 per province
        "monitor": 5,  # 1 per province excl. Quirino
    }
    filler_items = ["dslr", "macbook", "ssd"]
    print("HDD: 1 unit per team member incl. focals")
    print("SSD: 1 unit per province")
    print("Monitor: 1 unit per province (Quirino's unit is for the person to replace me pagkalipat ko)")
    print("DSLR: dynamic qty")
    print("Macbook: dynamic qty")
    print("-------------------------")

obj_5020321003()

if filler_item != "" and (filler_item not in filler_items): 
    filler_items += [filler_item]

filler_item_infos = {}
for item in filler_items:
    filler_item_infos[item] = items_to_procure.get(item, (0, "unit"))

for item in excluded_items:
    del items_to_procure[item]
    if item in determined_procurements:
        del determined_procurements[item]

determined_utilization = 0
determined_itemlist = []
for item, item_count in determined_procurements.items():
    # do not handle keyerror
    item_value = items_to_procure.get(item, [0, "unit"])[0]
    item_unit = items_to_procure[item][1]
    item_total_cost = item_value * item_count

    # unit
    item_unit_plural = plurals.get(item_unit, item_unit + 's')
    
    item_print_name = item
    if not COPYPASTA:
        item_print_name = item[:item.find("(")]

    determined_itemlist += [(f"{item_print_name}: {item_value:,.2f} x {item_count} {item_unit_plural if item_count > 1 else item_unit}", f"{item_total_cost:,.2f}")]
    determined_utilization += item_total_cost

    budget_offset += item_total_cost

    del items_to_procure[item]

target_budget -= budget_offset

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
        
        gini_coeff = 0
        if len(result) > 0:
            gini_coeff = gini(list(result.values()))

        utilization = 0
        for k, v in result.items():
            utilization += to_procure[k] * v

        if best_result is None \
        or best_gini_coeff > gini_coeff:
            best_result = result
            best_gini_coeff = gini_coeff
        
        if len(result) <= 0:
            break
        i += 1


utilization = 0
itemList = [] + determined_itemlist
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

maxItemStrlen = 0
if len(itemList) > 0:
    maxItemStrlen = max(len(x[0]) for x in itemList)

for x in itemList:
  if COPYPASTA:
    print(f"- {x[0]} = {x[1]}")
  else:
    print(f"{' '*(maxItemStrlen - len(x[0]))}{x[0]} = {x[1]}")

unallocated_budget = target_budget - utilization + missing_decimal
print(f"\nTotal: {utilization+budget_offset:,.2f}/{target_budget+budget_offset+missing_decimal:,.2f}")
print(f"Gini Coefficient: {best_gini_coeff}")
print(f"Unallocated: {unallocated_budget:,.2f}")


if len(filler_items) > 0:

    # divide unallocated budget among items
    unallocated_per_item = unallocated_budget / len(filler_items)
    print(f"\nAdjust budget per item: {unallocated_per_item:,.2f}")
    for filler_item in filler_items:

        print(f"\nPrice Adjustment for {filler_item}:")
        filler_item_info = filler_item_infos.get(filler_item, (0, "unit"))
        filler_item_price = filler_item_info[0]
        filler_item_unit = filler_item_info[1]
        filler_item_count = best_result.get(filler_item, determined_procurements.get(filler_item, 0))

        if filler_item_price > 0 and filler_item_count > 0:
            filler_item_total = filler_item_count * filler_item_price
            print(f"{filler_item}: {filler_item_count} x {filler_item_price:,.2f} = {filler_item_total:,.2f}")

            filler_item_total_target = filler_item_total + unallocated_per_item
            print(f"{len(filler_item) * ' '}: {filler_item_total:,.2f} + {unallocated_per_item:,.2f} = {filler_item_total_target:,.2f}")

            filler_item_target_price = filler_item_total_target / filler_item_count
            print(f"{len(filler_item) * ' '}: (Accurate per-unit price): {filler_item_target_price}")
            print(f"{len(filler_item) * ' '}: (Accurate subtotal price): {filler_item_target_price * filler_item_count}")
            print(f"{len(filler_item) * ' '}: {filler_item_target_price * filler_item_count:,.2f} ÷ {filler_item_count} = {filler_item_target_price:,.2f}/{filler_item_unit}")
        else:
            print("Error")