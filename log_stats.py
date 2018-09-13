#!/usr/bin/env python3


import sys
import re
from datetime import datetime, timedelta

# Checks if a specific number of minutes exists
# In case of no specific number of minutes the default will be 1 minute


def minutes(argv):
    try:
        index = argv.index('--interval')
    except ValueError:
        return 1
    if len(argv) == 2:
        return 1
    elif argv[index + 1].isdigit():
        return int(argv[index + 1])
    else:
        return 1

# Checks if '--start' argument exists
# If it exists, the function will return its value


def start(argv):
    try:
        index = argv.index('--start')
        return argv[index + 1]
    except IndexError:
        return
    except ValueError:
        return

# Checks if '--end' argument exists
# If it exists, the function will return its value


def end(argv):
    try:
        index = argv.index('--end')
        return argv[index + 1]
    except IndexError:
        return
    except ValueError:
        return


# Extracts the endpoint
# Eg: '/fedora.html'


def endpoint(log):

    substring_1 = 'GET '
    substring_2 = '.html'

    endpoint = log.split(substring_1)[-1].split(substring_2)[0] + '.html'
    return endpoint

# Gets status code
# Eg: 201


def status_code(log):

    status_code = [int(s) for s in log.split() if s.isdigit()]
    return status_code[0]


# Function to return date
# Eg: '2017-02-22T18:45'

def format_date(log):

    date = re.search(r'\[(.*?)\]', log).group(1)
    date = date[:17]
    datetime_object = datetime.strptime(date, '%d/%b/%Y:%H:%M')
    date = datetime_object.strftime('%Y-%m-%dT%H:%M')

    return date


# Pastes date, interval duration and endpoint
# Produces strings to work with
# Eg: '2017-02-22T18:45 1 /centos.html'


def date_interval_endpoint():
    for date, interval, endpoint in zip(date_list, interval_list, endpoint_list):
        date_interval_endpoint_list.append(
            date + ' ' + str(interval) + ' ' + endpoint)


# Filters final output after all paramaters
# --interval, --start, --end


def output(interval):

    success = 0
    total = 0
    i = 0
    j = 0

    if start(sys.argv) is not None:
        start_date = start(sys.argv)

        while date_interval_endpoint_list[0].split(' ')[0] < start_date:
            date_interval_endpoint_list.pop(0)
            status_code_list.pop(0)

    if end(sys.argv) is not None:
        end_date = end(sys.argv)

        while date_interval_endpoint_list[-1].split(' ')[0] > end_date:
            date_interval_endpoint_list.pop(-1)
            status_code_list.pop(-1)

    while i < len(date_interval_endpoint_list):

        date1 = date_interval_endpoint_list[i].split(' ')[0]
        date1 = datetime.strptime(date1, '%Y-%m-%dT%H:%M')
        date2 = date1 + timedelta(minutes=interval)
        curr_date = date1
        end1 = date_interval_endpoint_list[i].split(' ')[-1]

        while(curr_date < date2):
            end2 = date_interval_endpoint_list[j].split(' ')[-1]
            if end1 == end2:

                if status_code_list[j] >= 200 and status_code_list[j] < 300:
                    success += 1
                    total += 1
                else:
                    total += 1
                if i < j:
                    status_code_list.pop(j)
                    date_interval_endpoint_list.pop(j)
                    j -= 1

            j += 1
            if(j == len(date_interval_endpoint_list)):
                break
            curr_date = date_interval_endpoint_list[j].split(' ')[0]
            curr_date = datetime.strptime(curr_date, '%Y-%m-%dT%H:%M')
        result = success / total * 100
        success_rate_list.append("%0.2f" % result)
        i += 1
        j = i
        success = 0
        total = 0

# Makes output a single list (date + interval + success rate)
# Eg: '2017-02-22T18:46 2 65.24'


def full_output():
    for date, success in zip(date_interval_endpoint_list, success_rate_list):
        final_output.append(date + ' ' + success)

# Sorts output and prints it


def print_sorted_output():
    for i in sorted(final_output):
        print(i)


# Creates lists
interval_list = []
date_list = []
endpoint_list = []
status_code_list = []
date_interval_endpoint_list = []
success_rate_list = []
final_output = []


with open(sys.argv[1]) as logs:
    for log in logs:
        interval_list.append(minutes(sys.argv))
        date_list.append(format_date(log))
        endpoint_list.append(endpoint(log))
        status_code_list.append(status_code(log))

date_interval_endpoint()
output(minutes(sys.argv))
full_output()
print_sorted_output()
