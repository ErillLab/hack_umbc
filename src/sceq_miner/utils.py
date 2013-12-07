def partition_according_to(f,xs):
    """Partition xs according to f"""
    part = []
    xsys = [(x,f(x)) for x in xs]
    yvals = set([y for (x,y) in xsys])
    return [[x for (x,y) in xsys if y == yval] for yval in yvals]

def concat(xxs):
    return [x for xs in xxs for x in xs]

def h(ps):
    """compute entropy (in bits) of a probability distribution ps"""
    return -sum([p * safe_log2(p) for p in ps])

def normalize(xs):
    total = float(sum(xs))
    return [x/total for x in xs]

