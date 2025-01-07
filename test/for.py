@wireflow
def rangeStop():
    stop = 10
    total = 0
    for i in range(stop):
        total += i*2
@wireflow
def rangeStartStop():
    start = 5
    stop = 15
    product = 1
    for i in range(start, stop):
        if i % 2 == 0:
            product *= i
@wireflow
def rangeStartStopStep():
    start = 2
    stop = 20
    step = 4
    weighted_sum = 0
    index = 0
    for i in range(start, stop, step):
        weighted_sum += i * index
        index += 1



