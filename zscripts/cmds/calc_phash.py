import os

from zscripts.core.phash import PHash


class CmdCalcPHash(object):
    CMD_CALL = 'calc-phash'
    CMD_VER = '0.0.1'

    def __init__(self):
        super(CmdCalcPHash, self).__init__()
        self.calculator = PHash()

    @staticmethod
    def _expand_paths(paths, recursive=False, follow_symlink=False):
        for path in paths:
            if os.path.isfile(path):
                yield path
            elif recursive and os.path.isdir(path):
                # Please run the code in Python >= 3.5,
                # otherwise os.walk() will not be efficient enough.
                for root, dirs, files in os.walk(path, follow_symlink):
                    for file in files:
                        yield os.path.join(root, file)

    def run(self, args):
        supported_ext = self.calculator.SUPPORTED_EXT
        paths = filter(
            lambda p: os.path.splitext(p)[-1] in supported_ext,
            self._expand_paths(args.path,
                               args.recursive,
                               args.follow_symlink)
        )
        for path in paths:
            phash = self.calculator.compute_from_path(path)
            phash = self.calculator.array2str(phash, args.uppercase)
            if args.move:
                parent, filename = os.path.split(path)
                prefix, suffix = os.path.splitext(filename)
                os.rename(path, os.path.join(parent, phash[0] + suffix))
            print('%s\t%s' % (phash[0], path))

    def register_arg_parse(self, parsers):
        # parsers: argparse._SubParsersAction
        parser = parsers.add_parser(
            self.CMD_CALL,
            help="print the phash of images and provide renaming support"
        )
        parser.add_argument('path', nargs='+')
        parser.add_argument('-m', '--move',
                            action='store_true',
                            help="rename the file name to the corresponding phash value")
        parser.add_argument('-r', '-R', '--recursive',
                            action='store_true',
                            help="process directories and their contents recursively")
        parser.add_argument('-s', '--follow-symlink',
                            action='store_true',
                            help='follow symbolic links to subdirectories')
        parser.add_argument('-u', '-U', '--uppercase',
                            action='store_true',
                            help="print uppercase values")
        parser.add_argument('-v', '--version',
                            action='version',
                            version=self.CMD_VER)
        parser.set_defaults(func=self.run)
