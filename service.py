from __future__ import absolute_import

from consumer import EventConsumer

class MonitorService(object):

    def __init__(self, logger):
        self.logger = logger

    def start(self):
        EventConsumer(self.logger).start()
