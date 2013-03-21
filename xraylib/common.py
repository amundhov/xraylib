import pickle
import numpy as np
from pkg_resources import resource_string

class Bunch:
    def __init__(self, **kwds):
        self.add(**kwds)
    def add(self, **kwds):
        self.__dict__.update(kwds)
    def __repr__(self):
        return unicode(self)
    def __unicode__(self):
        format_str = u": %s\n".join(self.__dict__.keys())
        format_str +=u": %s\n"
        return format_str % tuple(self.__dict__.values())

#
# >>> import xraylib
# >>> xraylib.XrayTable.dtype # list all available fields
# >>> xraylib.Xraytable['Density'][1] # density of Hydrogen
# >>> xraylib.Xraytable[1]['Density'] # also density of Hydrogen
#
# Please note that numpy's dot function for matrix multiplication does _not_
# work with scipy sparse matrices (such as the JumpMatrix). Use jumpMatrix.dot(foo)
# instead.

class XrayTable:
    ''' XrayTable contains various data related to
    interactions with X-rays for a range of elements. '''

    def __init__(self):
        self.table = pickle.loads(resource_string(__name__,'data/xraytable.pickle'))

    def __getitem__(self,key):
        if not isinstance(key,int):
            raise IndexError('First index must be an atomic number')
        if key > self.table.shape[0] or key < 1:
            raise IndexError('Invalid atomic number')
        return self.table[key-1]

# Replace class by singleton instance
XrayTable = XrayTable()

Elements = pickle.loads(resource_string(__name__,'data/elements.pickle'))


Constants = Bunch(
    c  = 299792458,        # (m/s) speed of light in vacuum (exact)
    mu =   4.0e-7*np.pi,   # (N/A^2) magnetic constant mu_0 (exact)
    Na =   6.0221415e23,   # Avogadro constants
    kB =   1.3806505e-23,  # (J/K) Boltzmann constant
    h  =   6.6260693e-34,  # (Js) Planck constant
    G  =   6.6742e-11,     # (m^3/kg/s^2) gravitational constant
    e  =   1.60217653e-19, # (J) electron volt
    me = 510.998918        # electron mass in keV
)

Constants.add(
    ep = 1/(Constants.mu*Constants.c**2),         # (F/m) electric constant eps_0
    hc = 1e7*Constants.h*Constants.c/Constants.e,        # (keV A) hc
    re = Constants.c**2*Constants.e/Constants.me,         # classical radius of electron in A
    ia = 2*Constants.h/(Constants.e**2*Constants.mu*Constants.c)  # 1/fine-structure
)

def strtoz(string):
    ''' Converts a string of stoichiometry into a dictionary 
        of corresponding atomic numbers and element count.
        E.G H2O -> { ('H':1):2, ('O':8):1 }                 '''
    string = string.replace('Air', 'N4O')
    return _strtoz(string)


def _strtoz(string):
    try:
        return { int(string) : 1 }
    except ValueError:
        # Not an integer
        (leftBracket,rightBracket) = _getmatchedparentheses(string)
        if leftBracket != -1:
            # string is of form a(b)c
            a_z = _strtoz(string[0:leftBracket])
            b_z = _strtoz(string[leftBracket+1:rightBracket])

            c = string[rightBracket+1:]
            factor = 1
            if len(c):
                try:
                    factor = int(c[0])
                    c = c[1:]
                except ValueError:
                    # No integer followed parenthesis.
                    pass
            c_z = _strtoz(c)
            for element,count in b_z.items():
                a_z[element] = a_z.get(element,0) + factor*count
            for element,count in c_z.items():
                a_z[element] = a_z.get(element,0) + count
            return a_z
        else:
            # string with only elements and integers
            result = dict()
            while string:
                count = 1
                if len(string) == 0:
                    continue
                if len(string) > 1 and string[1].islower():
                    el = (string[0:2],Elements[string[0:2]])
                    string = string[2:]
                else:
                    if not string[0] in Elements.keys():
                        raise Exception('Invalid element %s' % string[0])
                    el = (string[0],Elements[string[0]])
                    string = string[1:]
                try:
                    count = int(string[0])
                    string = string[1:]
                except (IndexError,ValueError):
                    # No count given
                    pass

                result[el] = result.get(el,0) + count
            return result
    raise Exception('FIXME')

def _getmatchedparentheses(string):
    balance = 0
    left = string.find('(')
    index = left
    for char in string[left:]:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance == 0:
            return (left,index)
        index += 1
    if balance > 0:
        raise ValueError('Unmatched ( parenthesis')
    elif balance < 0:
        raise ValueError('Unmatched ) parenthesis')
    return (left,index)

def _teststrtoz():
    assert(strtoz('H') == { ('H',1):1, })
    assert(strtoz('(H)') == { ('H',1):1, })
    assert(strtoz('(H)2') == { ('H',1):2, })
    assert(strtoz('(H)()') == { ('H',1):1, })
