import lte.infrastructure as inf
from lte.channel import EncodedRayleigh
from lte.scheduler import ProportionalFair, MaxRate, ClassicUwr, MaxRateUwr


channel = EncodedRayleigh
channel_args = {
    'means_db' : EncodedRayleigh.means_from_user_classes(1, 1, 1), 
    'symbols_per_interval' : 14
}

schedulers = [
#    (MaxRate, {}),
#    (ProportionalFair, {'tau' : 0.03}),
#    (ClassicUwr, {'decay_rate' : 1.0}),
    (MaxRateUwr, {'decay_rate' : 1.0})
]


with inf.SqlStorage('infocom.sql') as storage:
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

