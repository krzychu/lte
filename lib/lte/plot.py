import numpy
import pdb


class Plot:
    def __init__(self, simulation_id, style):
        self.simulation_id = simulation_id
        self.style = style

    def draw(self, executions, plotter):
        pass


class Line(Plot):
    def __init__(self, shift, slope, interval, **style):
        Plot.__init__(self, None, style)
        self.shift = shift
        self.slope = slope
        self.interval = numpy.array(interval)

    def draw(self, executions, plotter):
        assert executions == None
        plotter.plot(self.interval, self.shift + self.slope * self.interval, \
                **self.style)


class TotalVsPossible(Plot):
    def __init__(self, simulation_id, **style):
        Plot.__init__(self, simulation_id, style)

    def draw(self, executions, plotter):
        assert len(executions) > 0
        
        plotter.xlabel('Possible [bits]')
        plotter.ylabel('Total [bits]')

        s = executions[0].get_rate_shape()
        possible = numpy.zeros(s)
        total = numpy.zeros(s)

        for ex in executions:
            possible += numpy.cumsum(ex.rate_history, axis=0)
            total += numpy.cumsum(ex.get_transmissions(), axis=0)

        possible /= len(executions)
        total /= len(executions)

        plotter.plot(possible.flatten(), total.flatten(), **self.style)


class RoundEfficiency(Plot):
    def __init__(self, simulation_id, **style):
        Plot.__init__(self, simulation_id, style)    

    def get_efficiencies(self, execution):
        rates = numpy.sum(execution.rate_history, axis=1, dtype='f')
        trans = execution.get_transmitted_rates()
        return trans[rates != 0] / rates[rates != 0]

    def draw(self, executions, plotter):
        plotter.ylabel('Probability')
        plotter.xlabel('Efficiency')

        efficiencies = numpy.sort(numpy.hstack([self.get_efficiencies(x) for x in executions]))
        ys = numpy.arange(len(efficiencies), dtype='f') / len(efficiencies)
        plotter.plot(efficiencies, ys, **self.style)


class Welfare(Plot):
    def __init__(self, simulation_id, **style):
        Plot.__init__(self, simulation_id, style)

    def draw(self, executions, plotter):
        plotter.xlabel('Time')
        plotter.ylabel('Welfare')
        n = len(executions)
        avg = numpy.zeros(executions[0].get_duration())
        for execution in executions:
            trans_sum = numpy.cumsum(execution.get_transmissions(), axis=0)
            welfare = numpy.sum(numpy.log(trans_sum + 1e-6), axis=1)
            welfare[welfare < 0] = 0
            avg += welfare / n
        
        plotter.plot(numpy.arange(len(avg)), avg, **self.style)



