import time


start_time = time.time()

while True:
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds", end='\r')  # `\r` for overwriting the same line
    time.sleep(1)
