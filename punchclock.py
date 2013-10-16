#! /usr/bin/env python

''' Something to keep track of hours. '''

import sys
import os.path
import dateutil.parser
from datetime import datetime
from datetime import timedelta

FILEPATH = '/home/juliusrain/code/punchclock/hours.log'

def clockin():
    if os.path.exists(FILEPATH):
        f=open(FILEPATH)
        last_operation = f.read().splitlines()[-1].split(' ')[0]
        if last_operation == 'in':
            sys.exit('You fucked up. Remember to clock out next time.')
        f.close()
    f = open(FILEPATH, 'ab')
    f.write('in %s\n' % datetime.now().isoformat())
    f.close()
def clockout():
    if os.path.exists(FILEPATH):
        f=open(FILEPATH)
        last_operation = f.read().splitlines()[-1].split(' ')[0]
        if last_operation == 'out':
            sys.exit('Sigh. Hand edit that file to have an in time. God.')
        f.close()
    else:
        sys.exit('First time here? Clock in first.')
    f = open(FILEPATH, 'ab')
    f.write('out %s\n' % datetime.now().isoformat())
    f.close()
def day():
    now = datetime.now()
    period('%d-%d-%d' % (now.year, now.month, now.day), now.isoformat())
def week():
    now = datetime.now()
    period('%d-%d-%d' % (now.year, now.month, now.day-now.weekday()), now.isoformat())
def month():
    now = datetime.now()
    period('%d-%d-01' % (now.year, now.month), now.isoformat())
def total():
    period('1000-1-1', datetime.now().isoformat())
def period(start, end):
    start = dateutil.parser.parse(start)
    end = dateutil.parser.parse(end)
    if not os.path.exists(FILEPATH):
        sys.exit("Sorry, we don't have a file for you")
    f = open(FILEPATH)
    lines = f.read().splitlines()
    # parse into list of [operation, datetime]
    lines = [line.split(' ') for line in lines]
    datetimes = [[line[0], dateutil.parser.parse(line[1])] for line in lines]
    # find where to start and end in the datetime list
    # i.e. find least date1 > start and greatest date2 < end
    start_i = 0
    end_i = 0
    for (i, x) in enumerate(reversed(datetimes)):
        if start <= x[1]:
            start_i = i
        else:
            break
    start_i = len(datetimes) - start_i - 1
    for (i,x) in enumerate(datetimes):
        if end >= x[1]:
            end_i = i
        else:
            break
    if start_i == end_i:
        hours = 0
    else:
        ins = [x for x in datetimes[start_i:end_i+1] if datetimes.index(x)%2==0]
        outs = [x for x in datetimes[start_i:end_i+1] if datetimes.index(x)%2==1]
        # sanity check
        if len(ins) != len(outs):
            sys.exit('you fucked up 1')
        for [operation, timestamp] in ins:
            if operation != 'in':
                sys.exit('you fucked up 2')
        for [operation, timestamp] in outs:
            if operation != 'out':
                sys.exit('you fucked up 3')
        time_pairs = zip([x[1] for x in ins], [x[1] for x in outs])
        delta = timedelta()
        for (in_time, out_time) in time_pairs:
            delta += out_time - in_time
        hours = delta.total_seconds() / 3600
    print 'Your hours for %s to %s are %0.2fh' % (start.date().__str__(), end.date().__str__(), hours)
    
def info():
    print 'Usage: python punchlock.py <command> \n \n \
  The available commands are:\n \
      [clock]in \t log clockin time \n \
      [clock]out \t log clockout time \n \
      day \t\t display total hours worked for the current day \n \
      week \t\t display total hours worked for the current week \n \
      month \t\t display total hours worked for the current monty \n \
      total \t\t display total hours worked ever \n \
      period \t\t display total hours worked from start [dd.mm.yyyy] to end [dd.mm.yyyy] \n \
      help \t\t display this stuff'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        info()
    elif sys.argv[1] == 'clockin' or sys.argv[1] == 'in':
        clockin()
    elif sys.argv[1] == 'clockout' or sys.argv[1] == 'out':
        clockout()
    elif sys.argv[1] == 'day':
        day()
    elif sys.argv[1] == 'week':
        week()
    elif sys.argv[1] == 'month':
        month()
    elif sys.argv[1] == 'total':
        total()
    elif sys.argv[1] == 'period':
        try:
            period(sys.argv[2], sys.argv[3])
        except IndexError:
            sys.exit('This command requires two dates.')
    else:
        help()
