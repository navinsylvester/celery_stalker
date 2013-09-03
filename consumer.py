from __future__ import absolute_import

from celery import current_app
from celery.events.state import state

import logging

class EventConsumer(object):

    def __init__(self, logger, state=state):
        self.logger = logger
        self.app = current_app
        self.state = state
        self.connection = self.app.broker_connection()
        self.receiver = self.app.events.Receiver(self.connection,
                                 handlers={'task-failed': self.failed_tasks,
                                           'task-succeeded' : self.succeeded_tasks,
                                           'task-received' : self.received_tasks,
                                           'task-started' : self.started_tasks,
                                           'worker-heartbeat': self.workers_heartbeat,
                                           'worker-offline': self.worker_down,
                                           'worker-online': self.worker_up
                                           })

    def start(self):
        self.receiver.capture(limit=None, timeout=None, wakeup=True)

    def failed_tasks(self, event):
        self.logger.info("Task FAILED: {0} {1} {2} {3}".format(event['uuid'], event['timestamp'], event['hostname'], event['exception']))
        self.logger.debug("Failed task uuid & traceback: ".format(event['uuid'], event['traceback']))
        
    def succeeded_tasks(self, event):
        self.logger.info("Task SUCCEEDED: {0} {1} {2} {3}".format(event['uuid'], event['timestamp'], event['hostname'], event['runtime']))
        
    def received_tasks(self, event):
        self.logger.info("Task RECEIVED: {0} {1} {2} {3} {4}".format(event['uuid'], event['timestamp'], event['hostname'], event['name'], event['retries']))
        
    def started_tasks(self, event):
        self.logger.info("Task STARTED: {0} {1} {2}".format(event['uuid'], event['timestamp'], event['hostname']))
        
    def worker_down(self, event):
        self.logger.info("Worker DOWN: {0} {1}".format(event['hostname'], event['timestamp']))
        
    def worker_up(self, event):
        self.logger.info("Worker UP: {0}".format(event['hostname'], event['timestamp']))
        
    def workers_heartbeat(self, event):
        #Noisy bitch
        self.logger.info("Worker HEARTBEAT: {0} {1} {2}".format(event['hostname'], event['timestamp'], event['freq']))
