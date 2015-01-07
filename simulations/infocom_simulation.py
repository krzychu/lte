# necessary imports
# if any of them fails, check your PYTHONPATH environment variable
import lte.infrastructure as inf
from lte.channel import EncodedRayleigh
from lte.scheduler import ProportionalFair, MaxRate, ClassicUwr, MaxRateUwr

# all simulations will use encoded rayleigh channel
channel = EncodedRayleigh # shortcut to its constructor

# dictionary containing necessary constructor arguments
# new channel object will be created for each execution
# so we need to store them somewhere
channel_args = {
    'means_db' : EncodedRayleigh.means_from_user_classes(1, 1, 1), 
    'symbols_per_interval' : 14
}

# list of all investigated schedulers, with corresponding 
# constructor arguments
schedulers = [
    (MaxRate, {}),
    (ProportionalFair, {'tau' : 0.03}),
    (ClassicUwr, {'decay_rate' : 1.0}),
    (MaxRateUwr, {'decay_rate' : 1.0})
]

# results will be saved to infocom.sql file. 
# 'with' statement ensures that changes will be saved
with inf.SqlStorage('infocom.sql') as storage:
    # we iterate schedulers, create simulation objects
    # and execute them
    for (scheduler, args) in schedulers:
        print str(scheduler)

        simulation = inf.Simulation()
        simulation.channel = channel
        simulation.channel_args = channel_args
        simulation.num_users = 3
        simulation.duration = 10000
        simulation.scheduler = scheduler
        simulation.scheduler_args = args

        inf.execute_all(storage, simulation, 10)

