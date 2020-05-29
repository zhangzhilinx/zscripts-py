import re
import time

from zscripts.core.power import PowerOperation


class CmdPwr(object):
    CMD_CALL = 'pwr'
    CMD_VER = '0.0.1'

    RE_INTERVAL = re.compile(r'(\d+)(ms|s|m|h)')
    TIME_FACTOR = {
        'h': 3600,
        'm': 60,
        's': 1,
        'ms': 0.001
    }

    def __init__(self):
        super(CmdPwr, self).__init__()
        self.actions = {
            'halt': PowerOperation.halt,
            'hibernate': PowerOperation.hibernate,
            'lock': PowerOperation.lock,
            'logout': PowerOperation.logout,
            'reboot': PowerOperation.reboot,
            'scroff': PowerOperation.screen_off,
            'suspend': PowerOperation.suspend
        }

    @classmethod
    def parse_my_simple_time(cls, simple_time):
        time_txt = simple_time
        time_map = {}

        pos, end = 0, len(simple_time)
        while pos < end:
            match = cls.RE_INTERVAL.search(time_txt, pos)
            if match is None:
                break
            time_map[match.groups()[1]] = int(match.groups()[0])
            pos = match.end()

        secs = 0
        for k, v in time_map.items():
            secs += cls.TIME_FACTOR.get(k, 0) * v
        return secs

    def run(self, args):
        after = 0 if args.after is None \
            else self.parse_my_simple_time(args.after)
        if after:
            time.sleep(after)
        self.actions[args.action](**{
            'force': args.force
        })

    def register_arg_parse(self, parsers):
        # parsers: argparse._SubParsersAction
        parser = parsers.add_parser(
            self.CMD_CALL,
            help="simple power control with countdown support"
        )
        parser.add_argument('action',
                            choices=self.actions.keys())
        parser.add_argument('--after',
                            help="wait a certain amount of time before performing the operation")
        parser.add_argument('-f', '--force',
                            action='store_true',
                            help="force the computer to shutdown or reboot")
        parser.add_argument('-v', '--version',
                            action='version',
                            version=self.CMD_VER)
        parser.set_defaults(func=self.run)
