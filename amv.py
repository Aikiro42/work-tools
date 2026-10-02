venue = 11000

snacks = 150
lunch = 350
dinner = 150
pax = 28

firstHalf = ((snacks * 2) + dinner) * pax * 2
secondHalf = ((snacks * 2)) * pax

venueCost = (venue + (lunch * pax)) * 3

print(f"Day 1-2 AM snack, PM snack, Dinner - {((snacks * 2) + dinner):,.2f} x {pax} pax x 2 days = {firstHalf:,.2f}")
print(f"Day 3 AM snack, PM snack, Lunch -  {(snacks * 2):,.2f} x {pax} pax x 1 day = {secondHalf:,.2f}")

print(f"{(venue + (lunch * pax)):,.2f} x 3 days = {venueCost:,.2f}")