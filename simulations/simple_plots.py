import lte.tool
from lte.plot import *


class SimplePlots(lte.tool.PlottingTool):
    def __init__(self):
        lte.tool.PlottingTool.__init__(self, 'simple plots')

        self.add_plot("welfare", [Welfare(1, 'a', 'r')])
        self.add_plot("efficiency", [RoundEfficiency(1, 'a', 'r')])
        self.add_plot("total", [TotalVsPossible(1, 'a', 'r')])


if __name__ == '__main__':
    lte.tool.run(SimplePlots())
