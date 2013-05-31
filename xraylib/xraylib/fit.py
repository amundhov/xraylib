import numpy as np

import utils

gaussian = lambda x,x0,sigma: 1.0/(np.sqrt(2*np.pi)*sigma)*np.exp(-0.5*((x-x0)/sigma)**2)

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

