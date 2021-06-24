import os
import argparse
from time import sleep


# FUCKING BAD IMPLEMENTATION OF CRONJOB.
# BUT I WANT TO BE SURE THAT EVERYTHING IS WORKING FINE.
# PROBLEM: while loop will eventually crash in python.
# PROBLEM 2: If a script takes 1 hour to finish, the next one will start end_timing + seconds
# TODO: validate if your input is correct (eg. does this file exists, eg. is seconds a number?)
# I am a fan of this approach for the "more" control you have than cron command


# Example usage:
# Run Test.py every 10 minutes: python3 cron.py --file test.py --seconds 3600
# Run Test.py every 60 minutes: python3 cron.py --file test.py --seconds 600
# Run Test.py every 10 minutes, without open terminal: sudo pm2 start cron.py --name cron-test.py -- --file test.py --seconds 600
# Run Test.py every 60 minutes, without open terminal: sudo pm2 start cron.py --name cron-imgs -- --file watermark.py --seconds 3600

# Run Test.py every 6 hours, without open terminal: sudo pm2 start cron.py --name cron-hubspot -- --file hubspot.py --seconds 21600
# Run contacts.py every 60 minutes, without open terminal: sudo pm2 start cron.py --name cron-contacts -- --file contacts.py --seconds 3600


parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--seconds')
args = parser.parse_args()

file = args.file
seconds = args.seconds


if file and seconds:
    print('Running ' + file + ' every '+str(seconds)+' seconds')

    while(True):
        os.system('python3 '+str(file))
        sleep(int(seconds))

else:
    print('Missing parameter(s)')

# os.system('python3 test.py')
