import cv2
import numpy as np


class PHash(object):
    SUPPORTED_EXT = {'.bmp', '.dib',
                     '.jpeg', '.jpg', '.jpe',
                     '.jp2',
                     '.png',
                     '.pbm', '.pgm', '.ppm',
                     '.sr', '.ras',
                     '.tiff', '.tif'}

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

    def compute_from_path(self, path: str):
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
        return self.calculator.compute(img)

    @classmethod
    def is_support_ext(cls, ext: str) -> bool:
        return ext in cls.SUPPORTED_EXT
