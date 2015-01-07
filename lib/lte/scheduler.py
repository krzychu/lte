import numpy
import pdb
import hyperbolic


class MaxRate:
    '''
    Always selects user with highest rate
    '''
    def __init__(self, simulation, channel):
        pass

    def get_active_user(self, rates):
        return numpy.argmax(rates)


class ProportionalFair:
    def __init__(self, simulation, channel, tau):
        '''
        during execution of this algorithm, accululated transfer decays
        exponentially with rate tau
        '''
        self.tau = tau
        self.average = numpy.zeros(simulation.num_users)

    def get_active_user(self, rates):
        if rates.shape != self.average.shape:
            raise TypeError("rates shape is {0} but should be {1}" % (rates.shape, self.average.shape))

        selected = numpy.argmax(rates / (self.average + 1e-10))
        self.average *= 1.0 - self.tau
        self.average[selected] += self.tau * rates[selected]

        return selected


class RoundRobin:
    def __init__(self, simulation, channel):
        self.simulation = simulation
        self.time = 0

    def get_active_user(self, rates):
        self.time += 1
        return self.time % self.simulation.num_users


class HyperbolicConstants:
    def __init__(self, num_users, max_capacity, decay_rate):
        self.num_users = num_users
        self.max_capacity = max_capacity
        self.delta = 1.0 / (1 + num_users)
        self.A = 12.0 * num_users * num_users * max_capacity
        self.decay_rate = decay_rate


class Hyperbolic:
    def __init__(self, simulation, channel, decay_rate):
        self.constants = HyperbolicConstants(simulation.num_users, \
                channel.max_bits_per_interval(), decay_rate)
        self.total = numpy.zeros(simulation.num_users)
        self.possible = numpy.zeros(simulation.num_users)

    def get_updated_total(self, rates, selected):
        return hyperbolic.update_total(self.constants, rates, selected, self.total)

    def get_updated_possible(self, rates):
        return hyperbolic.update_possible(self.constants, rates, self.possible)

    def update_state(self, rates, selected):
        self.possible = self.get_updated_possible(rates)
        self.total = self.get_updated_total(rates, selected)

    def select(self, rates):
        raise NotImplementedError()

    def get_active_user(self, rates):
        selected = self.select(rates)
        self.update_state(rates, selected)
        return selected


class MaxRateHyperbolic(Hyperbolic):
    def __init__(self, simulation, channel, decay_rate):
        Hyperbolic.__init__(self, simulation, channel, decay_rate)

    def select(self, rates):
        best = None
        p = self.get_updated_possible(rates)
        for i in xrange(self.constants.num_users):
            t = self.get_updated_total(rates, i)
            
            if not hyperbolic.is_feasible(self.constants, t, p):
                continue

            current = (rates[i], i)
            if not best or best < current:
                best = current

        assert best
        return best[1]


class GradientHyperbolic(Hyperbolic):
    def __init__(self, simulation, channel, decay_rate):
        Hyperbolic.__init__(self, simulation, channel, decay_rate)

    def select(self, rates):
        p = hyperbolic.get_position(self.constants, self.total, self.possible)
        thr = 6 * self.constants.num_users ** 2
        obligatory = - self.constants.delta * rates
        is_small = numpy.all(obligatory * thr <= p)

        if is_small:
            return numpy.argmax(obligatory * hyperbolic.potential_derivatives(p))
        else:
            return numpy.argmax(-obligatory)
