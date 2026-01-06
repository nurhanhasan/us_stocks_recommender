import mock_data
from pprint import pprint

# Algorithm
"""
## Goal: Sort by Highest Change and Highest Rel Volume.
Answer: Not feasible.

# Sort by CH desc
X: CH: 37, RV:5
Y: CH: 22, RV:7
Z: CH: 10, RV:9

# Sort by RV desc
Z: CH: 10, RV:9
Y: CH: 22, RV:7
X: CH: 37, RV:5

## Alternative #1: Use weighted score, Ex
for d in data:
    d['change_val'] = float(d['change'].replace('%', ''))
    # Create a combined momentum score
    d['weighted_score'] =  (d['rel_volume'] * 0.35) +  (d['float'] * 0.30) + (d['change'] * 0.20) + (d['price'] * 0.15)

sorted_data = sorted(data, key=lambda x: x['weighted_score'], reverse=True)

if Short_float
0.35 RV
0.30 Float
0.20 CH
0.15 price


## Alternative #2: Use nested if, Ex

potential_perfect_stocks = []
if d['short_float'] < 5:
    if d["rel_volume"] > 10:
        if d["float"] < 2:
            if d["price"] < 5:
                if d["change"] > 20:
                    potential_perfect_stock.append[d]
"""

DATA = mock_data.DATA

# print("Sorted by Order")
# DATA.sort(key=lambda x: x["order"])
# # print(DATA)


# print("Sorted by Rel Volume")
# DATA.sort(key=lambda x: x["rel_volume"])
# # print(DATA)

# Clean and mutate data
for d in DATA:
    d["change"]         = float(d["change"].replace("%", ""))
    d["short_float"]    = float(d["short_float"].replace("%", ""))
    d["float"]          = float(d["float"].replace("M", ""))
# print(DATA)


print("Sol. #1: Sorted by Weighted Score")
weighted_score_DATA = []
for d in DATA:
    if d['short_float'] < 5:
        d['weighted_score'] = (
            (d["rel_volume"] * 0.45)
            + (d["volume"] * 0.10)
            + (d["float"] * 0.10)
            + (d["change"] * 0.20)
            + (d["price"] * 0.15)
        )
        weighted_score_DATA.append(d)

weighted_score_DATA.sort(key=lambda x: x["weighted_score"], reverse=True)
pprint(weighted_score_DATA)
# print(print(x) for x in weighted_score_DATA)
# list(map(lambda x: print(x), weighted_score_DATA))
print("\n")
for item in weighted_score_DATA: print(item["ticker"])
print("\n")



print("Sol. #2: Filtered by by Weighted Score")
potential_perfect_stock = []
for d in DATA:
    # print(d)
    if d['short_float'] < 5:
        if d["rel_volume"] > 10:
            if d["float"] < 2:
                if d["price"] < 5:
                    if d["change"] > 20:
                        potential_perfect_stock.append(d)

potential_perfect_stock.sort(reverse=True)
pprint(potential_perfect_stock)


