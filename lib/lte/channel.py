import numpy

def shannon_bits_per_second(linear_snr, bandwidth_hz):
    '''
    linear_snr - SNR NOT IN DB
    bandwidth_hz - bandwidth [hz]
    '''
    return bandwidth_hz * numpy.log2(1 + linear_snr)


enc_thresholds = [0.54, 0.91, 1.2, 1.41, 2.81, 4.78, 6.3, 7.41, 12.3, 26.91, 33.13, 38.01, 85.11, 141.25, 181.97]
enc_bps = [0.25, 0.4, 0.5, 0.67, 1, 1.3, 1.5, 1.6, 2, 2.66, 3, 3.2, 4, 4.5, 4.8]

def encoded_bits_per_symbol(linear_snr):
    for (t, r) in reversed(zip(enc_thresholds, enc_bps)):
        if t < linear_snr:
            return r
    return 0


def db_to_linear(db):
    '''
    converts decibels to linear scale
    '''
    return 10 ** (db / 10)


class Constant:
    '''
    Channel with constant rates
    '''
    def __init__(self, simulation, rates):
        self.rates = numpy.array(rates)

    def next_rates(self):
        return rates


class SimpleRayleigh:
    '''
    Rayleigh channel without encoding
    '''
    def __init__(self, simulation, means_db, interval_s, bandwidth_hz, max_bits_per_interval):
        '''
        arguments:
            means_db - array-like, mean SNR for each user [db]
            interval_s - length of scheduling interval [s]
            bandwidth_hz - bandwidth [hz]
            max_bits_per_interval - max number of bits possible to send in one interval
        '''
        self.linear_means = db_to_linear(numpy.array(means_db))
        self.interval = interval_s
        self.bandwidth = bandwidth_hz
        self.max_bits_per_interval = max_bits_per_interval

    def get_rate(self, linear_mean):
        snr = numpy.random.exponential(m)
        bps = shannon_bits_per_second(snr, self.bandwidth_hz)
        return min(bps, self.max_bits_per_interval)

    def next_rates(self):
        return numpy.array([self.get_rate(m) for m in self.linear_means])


class EncodedRayleigh:
    '''
    Rayleigh channel with encoding
    '''
    def __init__(self, simulation, means_db, symbols_per_interval):
        '''
        arguments:
            means_db - array-like, mean SNR for each user [db]
            symbols_per_interval - number of symbols in scheduling interval
        '''
        self.linear_means = db_to_linear(numpy.array(means_db))
        self.symbols_per_interval = symbols_per_interval

    def get_rate(self, linear_mean):
        snr = numpy.random.exponential(m)
        bpi = self.symbols_per_interval * encoded_bits_per_symbol(snr)

    def next_rates(self):
        return numpy.array([self.get_rate(m) for m in self.linear_means])


