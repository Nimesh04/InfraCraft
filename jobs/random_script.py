
import random
import time

print("Rolling the dice...")
time.sleep(2)

if random.choice([True, False]):
    print("Random success!")
else:
    raise RuntimeError("Random failure occurred.")

