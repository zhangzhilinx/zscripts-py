from urllib import parse

from win32com.client import Dispatch


class CmdGetExplorerPaths(object):
    CMD_CALL = 'get-explorer-paths'
    CMD_VER = '0.0.1'

    SHELL = Dispatch('Shell.Application')

    def __init__(self):
        super(CmdGetExplorerPaths, self).__init__()

    @classmethod
    def get_paths(cls):
        for win in cls.SHELL.Windows():
            yield parse.unquote(win.LocationURL)

    def run(self, args):
        for path in self.get_paths():
            print(path)

    def register_arg_parse(self, parsers):
        # parsers: argparse._SubParsersAction
        parser = parsers.add_parser(
            self.CMD_CALL,
            help="print all urls in the explorer.exe address bar"
        )
        parser.add_argument('-v', '--version',
                            action='version',
                            version=self.CMD_VER)
        parser.set_defaults(func=self.run)
