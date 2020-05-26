import os

import cv2
import numpy as np


class PHash(object):
    def __init__(self):
        self.calculator = cv2.img_hash.PHash_create()

    @staticmethod
    def array2list(phash_array):
        return phash_array.tolist()

    @staticmethod
    def array2str(phash_array, uppercase=False):
        t = '%02X' if uppercase else '%02x'
        return [''.join([t % ele for ele in a])
                for a in phash_array.tolist()]

    def compute(self, *args):
        return self.calculator.compute(*args)

    def compute_from_path(self, path):
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
        return self.calculator.compute(img)


class CmdCalcPHash(object):
    CMD_CALL = 'calc-phash'
    CMD_VER = '0.0.1'

    SUPPORTED_EXT = {'.bmp', '.dib',
                     '.jpeg', '.jpg', '.jpe',
                     '.jp2',
                     '.png',
                     '.pbm', '.pgm', '.ppm',
                     '.sr', '.ras',
                     '.tiff', '.tif'}

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
        paths = filter(
            lambda p: os.path.splitext(p)[-1] in self.SUPPORTED_EXT,
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
