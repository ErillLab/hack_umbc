def partition_according_to(f,xs):
    """Partition xs according to f"""
    part = []
    xsys = [(x,f(x)) for x in xs]
    yvals = set([y for (x,y) in xsys])
    return [[x for (x,y) in xsys if y == yval] for yval in yvals]
