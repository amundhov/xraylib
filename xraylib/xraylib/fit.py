import numpy as np

import utils

SQRT2 = 0.4142135623730951

GAUSSIAN  = 'gaussian'
DELTA     = 'delta'
GAUSS_ERF = 'erf'

def erf(x):
    a1 =  0.254829592; a2 = -0.284496736
    a3 =  1.421413741; a4 = -1.453152027
    a5 =  1.061405429; p  =  0.3275911

    if not type(x) == np.ndarray:
        x = np.array(x)
    sign = np.ones(x.shape)
    sign[x<0] = -1
    x = np.abs(x)

    # A & S 7.1.26
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*np.exp(-x*x)

    return sign*y


PEAK_FUNCTIONS = {
        GAUSSIAN  : lambda x,x0,sigma: 1.0/(np.sqrt(2*np.pi)*sigma)*np.exp(-0.5*((x-x0)/sigma)**2),
        DELTA     : lambda x,x0: 1 if  x == x0 else 0,
        GAUSS_ERF : lambda x,x0,sigma: erf( (x+0.5-x0) / (SQRT2*sigma)) -\
                                      erf( (x-0.5-x0) / (SQRT2*sigma))
}

def get_peak_function(position=0, fwhm=1, shape=DELTA, **kwargs):
    if shape == GAUSSIAN:
        sigma = fwhm / 2.35482004503  # FWHM = 2 sqrt(2 ln(2) ) sigma
        if fwhm < 10:
            # Few points, so we need to use proper quadrature
            shape = GAUSS_ERF
    elif shape == DELTA:
        return lambda x: PEAK_FUNCTIONS[shape](x,position)

    return lambda x: PEAK_FUNCTIONS[shape](x,position,sigma)

def fit_peak_intensity(signal, peak, bias=1):
    """
    """

    try:
        assert(signal.shape == peak.shape)
    except:
        raise Exception("Arguments must be compatible vectors.")

    A = np.array([np.ones(signal.size), np.arange(0,signal.size), peak])
    w = 1.0 / (signal+bias) # Use signal as squared error. dy ~ sqrt(y)
    B = A * np.array([w,w,w])

    covC = np.linalg.inv(np.dot(B,A.T))
    c = np.dot(np.dot(covC, B), signal)

    print c

def test_signal(x,c,fun,rand=0):
        signal =np.dot(np.array([np.ones(len(x)), x, fun]).T,c)
        signal = signal + rand*np.random.normal(0,2,signal.size)
        return signal

def test(N=21,(xmin,xmax)=(-10,10),c=[13.45,1.23,49.0],peak_width=2.2):
        x = np.linspace(xmin,xmax,N)
        #c = np.array([13.45, 1.23, 49.0]) # Constant, slope and peak magnitude
        signal = test_signal(x, c, gaussian(x,0,peak_width),2)
        peak = gaussian(x,0,peak_width)
        fit_peak_intensity(signal,peak)




