import common

class Sample:
    fields = ['thickness','density','compound','chi']
    units  = ('cm'       ,'g/cm^3' ,''        ,u'\u00B0')
    def __init__(self, thickness, density, compound, chi):
        '''' Sample with thickness in cm, density in g/cm^3
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


