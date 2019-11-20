import random
import datetime
import statistics
import math

random.seed(datetime.datetime.now())

TRIALS = 10000
SEGMENT_COUNT = 35  # Segments in the fence
DEFECT_RATE = 0.10
MAX_CHECK_DISTANCE = 4  # Maximum number of segments to test out in one go


# Generates a fence with defects (True values) at a rate of 1/n; n=inverse_defect_rate
def generate_fence_segments(segment_count=SEGMENT_COUNT, defect_rate=DEFECT_RATE):
    return [True if not random.randrange(math.floor(1 / defect_rate)) else False for x in range(0, segment_count)]


# Simulates recursive defect-checking on a section of fence, returning the number of checks required for that section
# Divide and Conquer
def check_fence(fence, start=0, end=SEGMENT_COUNT):
    if True in fence[start:end] and not start + 1 == end:
        middle = int((start + end) / 2)
        return 1 + check_fence(fence, start, middle) + check_fence(fence, middle, end)
    else:
        return 1


def find_first_fault_in(fence, start, end):
    # If this is the faulty section
    if True in fence[start:end] and start + 1 == end:
        # Return the section id and increment the check counter
        return {'fault_at': start, 'checks_performed': 1}

    elif True in fence[start:end]:
        middle = int((start + end) / 2)
        first_check = find_first_fault_in(fence, start, middle)
        if first_check['fault_at'] != -1:
            return {'fault_at': first_check['fault_at'], 'checks_performed': 1 + first_check['checks_performed']}
        else:
            second_check = find_first_fault_in(fence, middle, end)
            return {'fault_at': second_check['fault_at'], 'checks_performed': (1
                                                                               + first_check['checks_performed']
                                                                               + second_check['checks_performed'])}
    else:
        return {'fault_at': -1, 'checks_performed': 1}


def check_fence_limit_skips(fence, max_check_distance=MAX_CHECK_DISTANCE, start=0, end=SEGMENT_COUNT):
    checks_performed = 0
    sub_start = start
    sub_end = start + max_check_distance
    while sub_start < end:
        check = find_first_fault_in(fence, sub_start, sub_end)
        checks_performed += check['checks_performed']
        sub_start = check['fault_at'] + 1 if check['fault_at'] != -1 else sub_end
        sub_end = min(end, sub_start + max_check_distance)

    return checks_performed


# test_fence = [False, True, False, False, False, True]
# print(check_fence(test_fence, 0, len(test_fence)))
# print(check_fence_limit_skips(test_fence, 4, 0, len(test_fence)))

print(f'{SEGMENT_COUNT}-segment fence (would require {SEGMENT_COUNT} traditional tests)')

print('Tests performed, pure DnC:')
binary_result = statistics.mean([check_fence(generate_fence_segments()) for x in range(0, TRIALS)])
print(f'{binary_result} ({int(binary_result / SEGMENT_COUNT * 100)}% original time)')

print('Tests performed, DnC with maximum 4 segments:')
limited_binary_result = statistics.mean([check_fence_limit_skips(generate_fence_segments()) for x in range(0, TRIALS)])
print(f'{limited_binary_result} ({int(limited_binary_result / SEGMENT_COUNT * 100)}% original time)')

print()
