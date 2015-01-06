import lte.infrastructure as inf
from lte.channel import Constant
from lte.scheduler import MaxRate

sim = inf.Simulation()
sim.channel = Constant
sim.channel_args = { 'rates': [1, 2, 3] }
sim.scheduler = MaxRate

with inf.SqlStorage('simple.sql') as storage:
    inf.execute_all(storage, sim, 100)
