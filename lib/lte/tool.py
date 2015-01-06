import argparse
import matplotlib.pyplot
import numpy
import lte.plot
import lte.infrastructure as inf

class Dummy:
    def get_name(self):
        return 'Dummy'

    def add_arguments(self, parser):
        parser.add_argument('k', type=float)

    def run(self, plotter, args):
        plotter.title('dummy')
        plotter.xlabel('x')
        plotter.ylabel('y')
        xs = numpy.linspace(-10, 10, 1000)
        ys = numpy.sin(args.k * xs)
        plotter.plot(xs, ys)
        plotter.show()


class PlottingTool:
    def __init__(self, name):
        self.name = name
        self.plots = {}

    def get_name(self):
        return self.name

    def add_arguments(self, parser):
        parser.add_argument('simulation_database', type=str)
        parser.add_argument('command', choices=self.plots.keys())

    def add_plot(self, command, plots):
        self.plots[command] = plots

    def run(self, plotter, args):
        plots = self.plots[args.command]
        with inf.SqlStorage(args.simulation_database) as storage:
            for plot in plots:
                if plot.simulation_id:
                    executions = storage.get_all_executions(plot.simulation_id)
                else:
                    executions = []

                plot.draw(executions, plotter)

        plotter.show() 


def run(tool):
    parser = argparse.ArgumentParser(tool.get_name()) 
    parser.add_argument('-o', metavar='output_file', type=str, default=None, help='output plot file')
    tool.add_arguments(parser)
    
    args = parser.parse_args()
    plotter = matplotlib.pyplot
    tool.run(plotter, args)
