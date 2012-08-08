import common, crossection
import pickle
import numpy as np

from common import Constants

class Sample:
    fields = ['thickness','density','compound','chi']
    units  = ('cm'       ,'g/cm^3' ,''        ,u'\u00B0')
    def __init__(self, thickness, density, compound, chi):
        ''' Sample with thickness in cm, density in g/cm^3
             compound as a string and sample angle chi in degrees '''
        self.thickness = thickness
        self.density = density
        if isinstance(compound,basestring):
            self.compound = (compound,common.strtoz(compound))
        else:
            self.compound = compound
        self.chi = chi
    def __repr__(self):
        return 'Sample(%s)' % ",".join(Sample.fields)
    def __unicode__(self):
        format_str = u": %s%%s\n".join([ o.capitalize() for o in Sample.fields ])
        format_str +=u": %s%%s\n"
        return format_str % tuple(self._attribute_list()) % Sample.units
    def __str__(self):
        return unicode(self).encode('utf-8')
    #FIXME: FUGLY, Fix object-passing in workbench
    def serialize(self):
        return _attribute_list()
    def _attribute_list(self):
        return [getattr(self,o) for o in Sample.fields]
    def mass_attenuation_coefficient(self,E):
        cross_section,mass = weighted(crossection.get_cross_section)(self,E)
        return total_cross_section*(Constants.Na*1e-24/mass)


def weighted(fun):
    ''' Decorator for calculations which are to be
        weighted according to sample stoichiometry. '''
    def wrapped_fun(sample,*_args,**_kwargs):
        Z = [ o[1] for o in sample.compound[1].keys() ]
        weights = sample.compound[1].values()
        res = 0
        for i in xrange(0,len(weights)):
            res += weights[i]*fun(z=Z[i],*_args,**_kwargs)
        return res
    return wrapped_fun

