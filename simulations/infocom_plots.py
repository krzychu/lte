import lte.tool
from lte.plot import *

# this class defines all plots available
# database access, plot selection, etc. are hidden in the base class
class InfocomPlotter(lte.tool.PlottingTool):
    def __init__(self):
        lte.tool.PlottingTool.__init__(self, 'INFOCOM plots')

        # here we define what happens, when selected plot name is 'welfare'
        # keyword arguments are passed to underlying matplotlib library, 
        # so refer to its documentation
        self.add_plot("encoded_welfare", [
            Welfare(1, label='MaxRate',                         color='r', marker='v', markevery=200),
            Welfare(2, label='ProportionalFair',                color='m', marker='^', markevery=200),
            Welfare(3, label='Hyperbolic (Gradient)',           color='b', marker='>', markevery=200),
            Welfare(4, label='Hyperbolic (MaxRate)',            color='g', marker='<', markevery=200)
        ])

        self.add_plot("encoded_efficiency", [
            RoundEfficiency(1, label='MaxRate',                 color='r', marker='v', markevery=3000),
            RoundEfficiency(2, label='ProportionalFair',        color='m', marker='^', markevery=3000),
            RoundEfficiency(3, label='Hyperbolic (Gradient)',   color='b', marker='>', markevery=3000),
            RoundEfficiency(4, label='Hyperbolic (MaxRate)',    color='g', marker='<', markevery=3000)
        ])

        self.add_plot("encoded_total_vs_possible", [
            TotalVsPossible(1, label='MaxRate',                 color='r', marker='v', linestyle='none', markevery=200),
            TotalVsPossible(2, label='ProportionalFair',        color='m', marker='^', linestyle='none', markevery=200),
            TotalVsPossible(3, label='Hyperbolic (Gradient)',   color='b', marker='>', linestyle='none', markevery=200),
            TotalVsPossible(4, label='Hyperbolic (MaxRate)',    color='g', marker='<', linestyle='none', markevery=200),
            Line(-7257.6, 0.25, (0, 500000), label='0.25x - 7257.6x', color='k')
        ])
  
        self.add_plot("simple_welfare", [
            Welfare(5, label='MaxRate',                         color='r', marker='v', markevery=200),
            Welfare(6, label='ProportionalFair',                color='m', marker='^', markevery=200),
            Welfare(7, label='Hyperbolic (Gradient)',           color='b', marker='>', markevery=200),
            Welfare(8, label='Hyperbolic (MaxRate)',            color='g', marker='<', markevery=200)
        ])

        self.add_plot("simple_efficiency", [
            RoundEfficiency(5, label='MaxRate',                 color='r', marker='v', markevery=3000),
            RoundEfficiency(6, label='ProportionalFair',        color='m', marker='^', markevery=3000),
            RoundEfficiency(7, label='Hyperbolic (Gradient)',   color='b', marker='>', markevery=3000),
            RoundEfficiency(8, label='Hyperbolic (MaxRate)',    color='g', marker='<', markevery=3000)
        ])

        self.add_plot("simple_total_vs_possible", [
            TotalVsPossible(5, label='MaxRate',                 color='r', marker='v', linestyle='none', markevery=200),
            TotalVsPossible(6, label='ProportionalFair',        color='m', marker='^', linestyle='none', markevery=200),
            TotalVsPossible(7, label='Hyperbolic (Gradient)',   color='b', marker='>', linestyle='none', markevery=200),
            TotalVsPossible(8, label='Hyperbolic (MaxRate)',    color='g', marker='<', linestyle='none', markevery=200),
            Line(-2.51e7, 0.25, (0, 500000), label='0.25x - 7257.6x', color='k')
        ])



if __name__ == '__main__':
    lte.tool.run(InfocomPlotter())
