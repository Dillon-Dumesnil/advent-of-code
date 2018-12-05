import os
import re

from datetime import datetime

script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    data = []
    with open(abs_file_path) as f:
        for line in f:
            date_time, action = line.split(']')
            date_time = date_time[1:]
            date, time = date_time.split()
            year, month, day = [int(i) for i in date.split('-')]
            hour, minute = [int(i) for i in time.split(':')]
            dt = datetime(year, month, day, hour, minute)
            data.append((dt, action.strip()))

    return sorted(data)

def organize_guard_data(data):
    guard_data = {}
    guard_id = None
    fall_asleep_time = None
    wake_up_time = None
    for dt, action in data:
        # setting a new guard_id
        if '#' in action:
            fall_asleep_time = None
            wake_up_time = None
            guard_id = ''.join(re.findall('\d', action))
            if guard_id not in guard_data:
                guard_data[guard_id] = [0, []]
        # actual actions happening to current guard_id
        else:
            if action == 'falls asleep':
                fall_asleep_time = dt.minute
            elif action == 'wakes up':
                wake_up_time = dt.minute
            if fall_asleep_time and wake_up_time:
                guard_data[guard_id][0] += (wake_up_time - fall_asleep_time)
                guard_data[guard_id][1].extend(range(fall_asleep_time, wake_up_time))
                fall_asleep_time = None
                wake_up_time = None

    return guard_data

def find_sleepiest_guard(guard_data):
    sleepy_guard = None
    sleepy_minute = None
    sleepy_minute_count = 0
    for guard_id in guard_data:
        minutes_asleep = guard_data[guard_id][1]
        if len(minutes_asleep) > 0:
            temp_minute = max(set(minutes_asleep), key=minutes_asleep.count)
            temp_count = int(minutes_asleep.count(temp_minute))
            if temp_count > sleepy_minute_count:
                sleepy_guard = guard_id
                sleepy_minute = temp_minute
                sleepy_minute_count = temp_count

    return int(sleepy_guard), int(sleepy_minute)

if __name__ == '__main__':
    data = parse_input('input.txt')
    guard_data = organize_guard_data(data)
    sleepy_guard, sleepy_minute = find_sleepiest_guard(guard_data)
    print(sleepy_guard * sleepy_minute)
