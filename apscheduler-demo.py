#!/usr/bin/env python

#-----------------------------------------------------------------------
# Author: Kevin Rui-sheng Lee 
#-----------------------------------------------------------------------

import time
import datetime
import random
from sys import exit, argv, stderr
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

'''
Import this to connect with your SQLAlchemy database
Afterwards, your scheduled jobs won't be cleared if Heroku crashes and restarts
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
'''

# Read the userguide here: https://apscheduler.readthedocs.io/en/stable/userguide.html

scheduler = BackgroundScheduler(timezone=utc)

#-----------------------------------------------------------------------

def job(message="Hello"):
	print("{} printed at {}".format(message, 
		datetime.datetime.now(tz=utc).strftime("%Y-%m-%d %H:%M:%S")))

#-----------------------------------------------------------------------

def main(argv):

	while True:
		scheduled_job1 = scheduler.add_job(job, "date", 
			run_date = datetime.datetime.now(tz=utc) + datetime.timedelta(seconds=10),
			kwargs={"message":"Konnichiwa"},id="job_konnichiwa")

		scheduled_job2 = scheduler.add_job(job, "date", 
			run_date = datetime.datetime.now(tz=utc) + datetime.timedelta(seconds=15),
			kwargs={"message":"Bonjour"},id="job_bonjour")

		# Newline
		print()
		for sched_job in scheduler.get_jobs():
			print(sched_job.id)

		print("Jobs scheduled at: {}".format(datetime.datetime.now(tz=utc).strftime("%Y-%m-%d %H:%M:%S"),))
		
		coinflip = random.randint(0, 1)
		if coinflip == True:
			scheduler.remove_job("job_bonjour")
			print("Removed job_bonjour")

		time.sleep(30)

#-----------------------------------------------------------------------

if __name__ == "__main__":
	scheduler.start()
	main(argv)
