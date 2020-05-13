import argparse
import ctypes


class CmdUAC(object):
    CMD_CALL = 'uac'
    CMD_VER = '0.0.1'

    def __init__(self):
        super(CmdUAC, self).__init__()

    def run(self, args):
        params = ' '.join(args.arg)
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas",
            args.file, params,
            args.directory,
            args.show_cmd
        )
        print("Succeeded" if result > 32 else "Failed", result)

    def register_arg_parse(self, parsers):
        # parsers: argparse._SubParsersAction
        parser = parsers.add_parser(
            self.CMD_CALL,
            help="run a program as an administrator"
        )
        parser.add_argument('-v', '--version',
                            action='version',
                            version=self.CMD_VER)
        parser.add_argument('-d', '--directory',
                            default=None,
                            help='specify a work directory')
        parser.add_argument('-s', '--showcmd',
                            choices=range(11),
                            default=1,
                            dest='show_cmd',
                            help="set ShowCmd parameter (default is 1)",
                            type=int)
        parser.add_argument('file',
                            help="file or program to be executed")
        # argparse.REMAINDER allows parameters such as -/-- to be read
        # https://bugs.python.org/issue13922
        parser.add_argument('arg',
                            help="parameters that need to be passed into the program",
                            nargs=argparse.REMAINDER)
        parser.set_defaults(func=self.run)
