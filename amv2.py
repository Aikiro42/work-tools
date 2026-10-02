def room_change(coins, target):
    dp = [float('inf')] * (target + 1)
    choice = [0] * (target + 1)
    dp[0] = 0

    for amount in range(1, target + 1):
        for coin in coins:
            if coin <= amount and dp[amount - coin] + 1 < dp[amount]:
                dp[amount] = dp[amount - coin] + 1
                choice[amount] = coin

    result = []
    while target > 0:
        coin = choice[target]
        result.append(coin)
        target -= coin

    return dp[sum(result)], result

pax = 25
execs = 3

# calculate accoms; unbounded knapsack algorithm for rooms
# dedicate single rooms to execs
# includes breakfast

# Twin Sharing Room - 2,500.00
# Solo Room - 2,000.00
_, rooms_list = room_change([2, 1], pax - execs)
rooms = {}
for room in rooms_list:
  rooms[str(room)] = rooms.get(str(room), 0) + 1
twinRooms = rooms.get("2", 0)
singleRooms = rooms.get("1", 0) + execs
roomCost = ( (twinRooms * 2500) + (singleRooms * 2000) ) * 3

print(f"Twin Sharing Room - 2,500.00 X {twinRooms} rooms X 3 nights = {twinRooms * 2500 * 3:,.2f}")
print(f"Solo Room - 2,000.00 X {singleRooms} rooms X 3 nights = {singleRooms* 2000 * 3:,.2f}")
print("_"*50)

# meals

pax = 30
snacks = 150
lunch = 250
dinner = 150

firstHalf = ((snacks * 2) + lunch + dinner) * pax * 2  # morning/afternoon snacks + lunch + dinner for 2 days
secondHalf = ((snacks * 2) + lunch) * pax  # egress on afternoon so only lunch

print(f"Rate: ({snacks:,.2f}/Snack - Plated, {lunch:,.2f}/Lunch - Managed Buffet, {dinner:,.2f}/Dinner)\n")
print(f"Day 1-2 AM snack, PM snack, Dinner - {((snacks * 2) + lunch + dinner):,.2f} x {pax} pax x 2 days = {firstHalf:,.2f}")
print(f"Day 3 AM snack, PM snack, Lunch -  {(snacks * 2) + lunch:,.2f} x {pax} pax x 1 day = {secondHalf:,.2f}")
print("_"*50)

# calculate venue cost
venue = 11000
venueCost = venue * 3
print(f"Rate: ({venue:,.2f}/Day)\n")
print(f"{venue:,.2f} x 3 days = {venueCost:,.2f}")
print("_"*50)

# calculate total cost
print(f"total cost: {roomCost + firstHalf + secondHalf + venueCost}")