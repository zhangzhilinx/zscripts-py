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
