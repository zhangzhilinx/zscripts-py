import argparse
from typing import List

from zscripts.cmds.calc_phash import CmdCalcPHash
from zscripts.cmds.fs_watcher import CmdFsWatcher
from zscripts.cmds.get_explorer_paths import CmdGetExplorerPaths
from zscripts.cmds.pwr import CmdPwr
from zscripts.cmds.uac import CmdUAC


def main(args: List[str] = None):
    parser = argparse.ArgumentParser(
        description="A set of scripts for my personal use."
    )
    sub_parsers = parser.add_subparsers(help="cmds-command help")

    sub_commands = [CmdCalcPHash(),
                    CmdFsWatcher(),
                    CmdGetExplorerPaths(),
                    CmdPwr(),
                    CmdUAC()]
    for sub_command in sub_commands:
        sub_command.register_arg_parse(sub_parsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


__all__ = ['main']
