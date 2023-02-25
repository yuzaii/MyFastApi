import time

print(time.time())

microsecond_timestamp = int(time.time() * 1000000 + time.perf_counter() * 1000000 % 1000000)
print(microsecond_timestamp)
