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
        self.add_plot("welfare", [
            Welfare(1, label='MaxRate',          color='r', marker='v', markevery=200),
            Welfare(2, label='ProportionalFair', color='g', marker='^', markevery=200),
            Welfare(3, label='Classic UWR',      color='b', marker='>', markevery=200),
            Welfare(4, label='MaxRate UWR',      color='m', marker='<', markevery=200)
        ])

        self.add_plot("efficiency", [
            RoundEfficiency(1, label='MaxRate',          color='r', marker='v', markevery=3000),
            RoundEfficiency(2, label='ProportionalFair', color='g', marker='^', markevery=3000),
            RoundEfficiency(3, label='Classic UWR',      color='b', marker='>', markevery=3000),
            RoundEfficiency(4, label='MaxRate UWR',      color='m', marker='<', markevery=3000)
        ])

        self.add_plot("total_vs_possible", [
            TotalVsPossible(1, label='MaxRate',          color='r', marker='v', linestyle='none', markevery=200),
            TotalVsPossible(2, label='ProportionalFair', color='g', marker='^', linestyle='none', markevery=200),
            TotalVsPossible(3, label='Classic UWR',      color='b', marker='>', linestyle='none', markevery=200),
            TotalVsPossible(4, label='MaxRate UWR',      color='m', marker='<', linestyle='none', markevery=200),
            Line(-7257.6, 0.25, (0, 500000), label='0.25x - 7257.6x', color='k')
        ])


if __name__ == '__main__':
    lte.tool.run(InfocomPlotter())
