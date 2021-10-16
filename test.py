import time

start_time = time.time()
while True:
    print(time.time() - start_time)
    if time.time() - start_time > 5:
        start_time = time.time()
