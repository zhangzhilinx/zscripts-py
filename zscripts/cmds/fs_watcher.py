import logging

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class CmdFsWatcher(object):
    CMD_CALL = 'fs-watcher'
    CMD_VER = '0.0.1'

    def __init__(self):
        super(CmdFsWatcher, self).__init__()

    def run(self, args):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        observer = Observer()
        handler = LoggingEventHandler()

        for p in args.path:
            observer.schedule(handler, p, args.recursive)

        observer.start()
        logging.info("Monitoring service have been activated")

        try:
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def register_arg_parse(self, parsers):
        # parsers: argparse._SubParsersAction
        parser = parsers.add_parser(
            self.CMD_CALL,
            help="monitor events of specified paths and print logs"
        )
        parser.add_argument('path', nargs='+')
        parser.add_argument('-r', '-R', '--recursive',
                            action='store_true',
                            help="process directories and their contents recursively")
        parser.add_argument('-v', '--version',
                            action='version',
                            version=self.CMD_VER)
        parser.set_defaults(func=self.run)
