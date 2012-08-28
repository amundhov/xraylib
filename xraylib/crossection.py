from common import Constants, XrayTable
import numpy as np

def get_cross_section(E,z):
    ''' Calculate cross section of element with atomic number z,
        Energy is units of FIXME'''
    if z < 1 or z > 92:
        raise Exception('Z is out of range')
    if not isinstance(E,np.ndarray):
        E = np.array(E)
    logE = np.log(E)
    B = XrayTable[z]['Edge']
    A = np.array([ logE**i for i in xrange(0,4)])
    cross_section = np.exp(np.dot(XrayTable[z]['Absorption'],A))
    Q = np.array([ B[i] <= E for i in xrange(0,5) ] + [ np.ones(E.shape,dtype=bool) ])
    Q[1:6] *= 1-Q[0:5]
    cross_section[0:6] = XrayTable[z]['JumpMatrix'].dot(cross_section[0:6]*Q)
    return sum(cross_section), XrayTable[z]['Density']

def klein_nishina(e0, two_theta, polarisation=0):
    ct = np.cos(np.deg2rad(two_theta))
    r2 = (Constants.re*1e-8)**2 * 1e24
    k  = 1/(1+e0*(1-ct)/Constants.me)
    s  = r2*k**2 * (1/k+k-(1-polarisation)*(1-ct**2))/2
    return (s,e0*k)

def thomson(two_theta, polarisation=0):
    ct = np.cos(np.deg2rad(two_theta))
    r2 = (Constants.re*1e-8)**2 * 1e24
    return (r2/2)*(2-(1-ct**2)*(1-polarisation))
