import numpy as np
import optparse,os, time, inspect

import xraylib, fabio
from xraylib import files

def debug_print(**kwargs):
    for name,var in kwargs.iteritems():
        print('%s = %s' % (name,var,))

def strip_none_values(dictionary):
    return dict([ (o,v) for o,v in dictionary.items() if not (v == None or v ==  [None])])

def flatten(val):
    if type(val) == dict:
        return dict([ (o,flatten(v)) for o,v in val.items()])

    if hasattr(val, '__iter__') and len(val) == 1:
        return val[0]

    if hasattr(val, '__iter__'):
        flat_list = []
        for item in val:
            if hasattr(item, '__iter__'):
                flat_list.extend(flatten(item))
            else:
                flat_list.append(item)
        return flat_list
    else:
        return [val]

def convert(val,val_type):
    if type(val) == dict:
        return dict([ (o,convert(v,val_type),) for o,v in val.items() ])
    if hasattr(val, '__iter__'):
        return [ convert(o,val_type) for o in val ]
    try:
        return val_type(str(val).strip())
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


    def print_verbose(self, *args, **kwargs):
        if self.options.verbose or not self.options.silent:
            if 'indent' in kwargs:
                for i in xrange(0, kwargs['indent']):
                    print "      ",
            for arg in args:
               print arg,
            print
