#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import with_statement

import os
import sys

from celery.bin.base import Command, Option, daemon_options
from celery.platforms import (
    detached,
    set_process_title,
    strargv,
    create_pidlock,
)

import logging

from service import MonitorService

STARTUP_INFO_FMT = """
Configuration ->
    . broker -> %(conninfo)s
""".strip()

OPTION_LIST = (
)


class MonitorCommand(Command):
    namespace = 'celery_stalker'
    enable_config_from_cmdline = True
    preload_options = Command.preload_options + daemon_options('celery_stalker.pid')

    def run(self, app=None, detach=False, pidfile=None,
            uid=None, gid=None, umask=None, working_directory=None, **kwargs):
        print('celery_stalker is starting.')
        app = self.app
        workdir = working_directory

        print(STARTUP_INFO_FMT % {
                'conninfo': app.broker_connection().as_uri(),
        })

        print('celery_stalker has started.')
        set_process_title('celery_stalker', info=strargv(sys.argv))
    
        logfile = 'celery_stalker.log'

        def _run_monitor():
            create_pidlock(pidfile)
            
            logger = logging.getLogger('celery_stalker')
        
            log_handler = logging.FileHandler(logfile)
            
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            
            log_handler.setFormatter(formatter)
            
            logger.addHandler(log_handler)
            
            logger.setLevel(logging.INFO)
            
            monitor = MonitorService(logger=logger)

            try:
                monitor.start()
            except Exception, exc:
                logger.error('celery_stalker raised exception %r',
                             exc, exc_info=True)
            except KeyboardInterrupt:
                pass

        if detach:
            with detached(logfile, pidfile, uid, gid, umask, workdir):
                _run_monitor()
        else:
            _run_monitor()

    def prepare_preload_options(self, options):
        workdir = options.get('working_directory')
        if workdir:
            os.chdir(workdir)

    def get_options(self):
        conf = self.app.conf
        return (
                Option('-D', '--detach',
                action='store_true', help='Run as daemon.'),
        )

try:
    from celery.bin.celery import Delegate

    class MonitorDelegate(Delegate):
        Command = MonitorCommand
except ImportError:
    try:
        MonitorDelegate = MonitorCommand
    except ImportError:
        class MonitorDelegate(object):
            pass


def main():
    mon = MonitorCommand()
    mon.execute_from_commandline()


if __name__ == '__main__':
    main()
