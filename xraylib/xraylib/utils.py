def strip_none_values(dictionary):
    return dict([ (o,v) for o,v in dictionary.items() if v is not None])

def toFloat(val):
    if hasattr(val, '__iter__'):
        return map(toFloat, val)
    try:
        return float(str(val).strip())
    except ValueError:
        return None
