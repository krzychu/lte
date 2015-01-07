import itertools

# necessary imports
# if any of them fails, check your PYTHONPATH environment variable
import lte.infrastructure as inf
from lte.channel import EncodedRayleigh, SimpleRayleigh
from lte.scheduler import ProportionalFair, MaxRate, GradientHyperbolic, MaxRateHyperbolic

# list of all investigated channels, with corresponding constructor arguments
channels = [
    (EncodedRayleigh, EncodedRayleigh.args_from_user_classes(14, 1, 1, 1)),
    (SimpleRayleigh, SimpleRayleigh.args_from_user_classes(20e6, 1e-3, 35, 1, 1, 1))
]

# list of all investigated schedulers, with corresponding constructor arguments
schedulers = [
    (MaxRate, {}),
    (ProportionalFair, {'tau' : 0.03}),
    (GradientHyperbolic, {'decay_rate' : 1.0}),
    (MaxRateHyperbolic, {'decay_rate' : 1.0})
]

cross = itertools.product(channels, schedulers)

# results will be saved to infocom.sql file. 
# 'with' statement ensures that changes will be saved
with inf.SqlStorage('infocom.sql') as storage:
    # we iterate schedulers, create simulation objects
    # and execute them
    for ((channel, channel_args), (scheduler, scheduler_args)) in cross:
        print str(channel), str(scheduler)

        simulation = inf.Simulation()
        simulation.channel = channel
        simulation.channel_args = channel_args
        simulation.num_users = 3
        simulation.duration = 10000
        simulation.scheduler = scheduler
        simulation.scheduler_args = scheduler_args

        inf.execute_all(storage, simulation, 10)

