import argparse
import matplotlib.pyplot
import numpy

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


def run(tool):
    parser = argparse.ArgumentParser(tool.get_name()) 
    parser.add_argument('-o', metavar='output_file', type=str, default=None, help='output plot file')
    tool.add_arguments(parser)
    
    args = parser.parse_args()
    plotter = matplotlib.pyplot
    tool.run(plotter, args)
