import sys, time, os, subprocess

min_time = float('inf')
total_time = 0.0
while True:
    start_time = time.perf_counter()
    #os.system(sys.argv[1])
    subprocess.check_output(sys.argv[1])
    elapsed = time.perf_counter() - start_time
    min_time = min(min_time, elapsed)
    total_time += elapsed
    if total_time >= 1.0:
        break

print(min_time)
