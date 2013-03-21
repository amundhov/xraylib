import xraylib
from xraylib import strtoz

def _teststrtoz():
    assert(strtoz('H') == { ('H',1):1, })
    assert(strtoz('O2') == { ('O',8): 2, })
    assert(strtoz('(H)') == { ('H',1):1, })
    assert(strtoz('(H)2') == { ('H',1):2, })
    assert(strtoz('(H)()') == { ('H',1):1, })
