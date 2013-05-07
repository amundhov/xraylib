import numpy as np
import optparse,os, time

import xraylib, fabio
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

class Script(object):
    def __init__(self):
        self.usage = "Usage: %prog <options>"
        self.description=""
        self.timings = []

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
        parser.add_option("-t", "--timings",
                          action="store_true", dest="timings", default=False,
                          help="Report execution times.")
        self.parser = parser

    def parse(self):
        (self.options,self.args) = self.parser.parse_args()

    @classmethod
    def timed(cls, fun):
        def wrapper(self, *args, **kwargs):
            start = time.time()
            fun(self, *args, **kwargs)
            self.timings.append((fun.__name__,time.time()-start),)
        return wrapper

    def print_timings(self):
        if not self.options.timings:
            return
        print("=== Execution time ===")
        for (i,j) in self.timings:
            print('%s: %.2fs' % (i.replace('_',' ').capitalize(),j))


    def print_verbose(self,*args):
        if self.options.verbose or not self.options.silent:
            for arg in args:
               print arg,
            print
