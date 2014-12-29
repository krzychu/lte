import numpy


class MaxRate:
    '''
    Always selects user with highest rate
    '''
    def __init__(self, simulation):
        pass

    def get_active_user(self, rates):
        return numpy.argmax(rates)


class ProportionalFair:
    def __init__(self, simulation, tau):
        '''
        during execution of this algorithm, accululated transfer decays
        exponentially with rate tau
        '''
        self.tau = tau
        self.average = numpy.zeros(simulation.num_users)

    def get_active_user(self, rates):
        if rates.shape != self.average:
            raise TypeError("rates shape is {0} but should be {1}" % (rates.shape, self.average.shape))

        selected = numpy.argmax(rates / self.average)
        self.average *= 1.0 - self.tau
        self.average[selected] += self.tau * rates[selected]

        return selected


class RoundRobin:
    def __init__(self, simulation):
        self.simulation = simulation

    def get_active_user(self, rates):
        return self.simulation.time % self.simulation.num_users
