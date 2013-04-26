import numpy as np
import optparse,os

import xraylib
from xraylib import files

def strip_none_values(dictionary):
    return dict([ (o,v) for o,v in dictionary.items() if v is not None])

def toFloat(val):
    if hasattr(val, '__iter__'):
        return map(toFloat, val)
    try:
        return float(str(val).strip())
    except ValueError:
        return None

def averageImages(filenames, method='median', verbose=False):
    """ Load and average a list of images. """
    images = [files.ImageFile(f).getImage() for f in filenames if os.path.isfile(f)]
    images = np.array(images)
    if method == 'median':
        return np.median(images,axis=0)
    else:
        raise Exception('NOT IMPLEMENTED')

class Script(object):
    def __init__(self):
        self.usage = 'Usage: %prog <options> '
        self.description=""

    def parser_setup(self):
        parser = optparse.OptionParser(usage=self.usage,description=self.description)

        parser.add_option("-V", "--version", dest="version", action="store_true",
                          help="print version of the program and quit", metavar="FILE", default=False)
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose", default=False,
                          help="switch to debug/verbose mode")
        parser.add_option("-s", "--silent",
                          action="store_true", dest="silent", default=False,
                          help="supress output to terminal.")
        self.parser = parser

    def parse(self):
        (self.options,self.args) = self.parser.parse_args()

    def print_verbose(self,*args):
        if self.options.verbose or not self.options.silent:
            for arg in args:
               print arg,
            print
