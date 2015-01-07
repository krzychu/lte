import numpy

def potential_value(position):
    outer = 1.0 / numpy.outer(position, position) 
    outer -= numpy.triu(outer)
    return numpy.sum(outer.flatten()) 


def potential_derivatives(position):
    inv = 1.0 / (position + 1e-10)
    base = numpy.sum(inv) - inv
    return - base * inv * inv


def get_position(constants, total, possible):
    return constants.A + total - constants.delta * possible


def update_possible(constants, rates, possible):
    return possible * constants.decay_rate + rates


def update_total(constants, rates, selected, total):
    p = total * constants.decay_rate 
    p[selected] += rates[selected]
    return p


def is_feasible(constants, total, possible):
    position = get_position(constants, total, possible)
    if numpy.any(position < 0):
        return False

    n = constants.num_users
    maxp = (n * (n - 1.0)) / 2.0 / constants.A ** 2
    return potential_value(position) <= maxp



