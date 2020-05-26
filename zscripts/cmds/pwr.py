import re
import time
from ctypes import windll

import win32api
import win32con
import win32security


class PowerOperation(object):
    def __init__(self):
        super(PowerOperation, self).__init__()

    @staticmethod
    def adjust_privilege(privilege: str, enable: bool = False) -> bool:
        new_privileges = [(
            win32security.LookupPrivilegeValue(None, privilege),
            win32con.SE_PRIVILEGE_ENABLED if enable else 0
        )]

        flags = win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
        token = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            flags
        )

        if not token:
            return False

        win32security.AdjustTokenPrivileges(
            token,
            0,
            new_privileges
        )

    @classmethod
    def halt(cls, force=False, **kwargs):
        cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, True)
        try:
            win32api.ExitWindowsEx(
                win32con.EWX_SHUTDOWN | win32con.EWX_FORCE if force
                else win32con.EWX_SHUTDOWN,
                0
            )
            # timeout = 0
            # message = 0
            # win32api.InitiateSystemShutdown(
            #     None,
            #     message, timeout,
            #     force, False
            # )
        finally:
            cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, False)

    @classmethod
    def hibernate(cls, force=False, **kwargs):
        # The force parameter has no effect actually
        cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, True)
        try:
            win32api.SetSystemPowerState(False, force)
        finally:
            cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, False)

    @staticmethod
    def lock(**kwargs):
        user32 = windll.LoadLibrary('user32.dll')
        user32.LockWorkStation()

    @staticmethod
    def logout(**kwargs):
        win32api.ExitWindows(0, 0)

    @classmethod
    def reboot(cls, force=False, **kwargs):
        cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, True)
        try:
            win32api.ExitWindowsEx(
                win32con.EWX_REBOOT | win32con.EWX_FORCE if force
                else win32con.EWX_REBOOT,
                0
            )
            # timeout = 0
            # message = 0
            # win32api.InitiateSystemShutdown(
            #     None,
            #     message, timeout,
            #     force, True
            # )
        finally:
            cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, False)

    @staticmethod
    def screen_off(**kwargs):
        user32 = windll.user32
        hwnd_broadcast = user32.FindWindowExA(None, None, None, None)
        user32.SendMessageA(hwnd_broadcast,
                            win32con.WM_SYSCOMMAND,
                            win32con.SC_MONITORPOWER,
                            2)

    @classmethod
    def suspend(cls, force=False, disable_wake_event=True, **kwargs):
        # The force parameter has no effect actually
        cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, True)
        try:
            # SetSuspendState(False, force, disable_wake_event)
            win32api.SetSystemPowerState(True, force)
        finally:
            cls.adjust_privilege(win32con.SE_SHUTDOWN_NAME, False)


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
