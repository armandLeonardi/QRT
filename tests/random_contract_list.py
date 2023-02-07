"""
This script is a part of small rental compagny simulation ask by QRT for application process.

This script generate and save as json file a random list of contracts depending of the given size.

Ael - 06FEB2
"""

import numpy as np
import json
import datetime
import os

template = {"name": "", "start": -1, "duration": -1, "price": -1}


N = 500000 # number of contracts
start = 0 
duration_min = 1
duration_max = 9
price_min = 1
price_max = 20

now = datetime.datetime.now().strftime("%d%m%y%H%M%S")
filename = f"{now}_loc.json"
with open(filename, 'w', encoding="utf8") as f:
    f.write("[")
    f.flush()

    k = 1
    while k < N:

        n = np.random.randint(1, 5)
        durations = []
        for i in range(n):
            
            duration = np.random.randint(duration_min, duration_max)
            price = np.random.randint(price_min, price_max)

            current = template.copy()
            current["name"] = f"Contract{k}"
            current["start"] = start
            current["duration"] = duration
            current["price"] = price

            json.dump(current, f)
            f.write(", ")
            f.flush

            if k == N:
                break
            
            k += 1
            durations.append(duration)

        start += int(np.random.choice(durations))

    f.write("]")
    f.close()

abs_path = os.path.abspath(filename)
print(f"Created: {abs_path}")
