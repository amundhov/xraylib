import common, crossection
import pickle
import numpy as np

from common import Constants

class Sample:
    fields = ['thickness','density','compound','chi']
    units  = ('cm'       ,'g/cm^3' ,''        ,u'\u00B0')
    def __init__(self, thickness, density, compound, chi):
        """ Sample with thickness in cm, density in g/cm^3
            compound as a string and sample angle chi in degrees """
        self.thickness = thickness
        self.density = density
        if isinstance(compound,basestring):
            self.compound = (compound,common.strtoz(compound))
        else:
            self.compound = compound
        self.chi = chi
    def __unicode__(self):
        format_str = u": %s%%s\n".join([ o.capitalize() for o in Sample.fields ])
        format_str +=u": %s%%s\n"
        return format_str % tuple(self._attribute_list()) % Sample.units
    def __str__(self):
        return unicode(self).encode('utf-8')
    def _attribute_list(self):
        return [getattr(self,o) for o in Sample.fields]

    # Computed quantities of compund

    def mass_attenuation(self,E):
        """ Mass attenuation coefficient cm^2 g^-1. """
        total_cross_section, cumm_density, total_mass = _weighted(crossection.get_cross_section)(self,E)
        return total_cross_section*(Constants.Na*1e-24)/total_mass

    def form_factor(self,q):
        """ Calculates the form factor of sample given
            scattering vector q = 4*pi*sin(Theta)/lambda """
        def interpolate():
            return 1
        form_factor = _weighted(interpolate)(q)
        return form_factor

def _weighted(fun):
    """ Decorator for calculations which are to be weighted
        according to sample stoichiometry. Returns a function
        which calls fun for each element in the sample. """
    def wrapped_fun(sample,*_args,**_kwargs):
        Z = [ o[1] for o in sample.compound[1].keys() ]
        weights = sample.compound[1].values()
        res = 0
        for i in xrange(0,len(weights)):
            res += weights[i]*fun(z=Z[i],*_args,**_kwargs)
        return res
    return wrapped_fun

