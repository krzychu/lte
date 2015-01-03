import importlib
import numpy
import sqlite3
import os.path
import json
import pdb
from contextlib import closing
import cStringIO as StringIO


def create_with_args(cls, args, sim):
    parts = cls.split('.')
    modulename = '.'.join(parts[:-1])
    classname = parts[-1]

    module = importlib.import_module(modulename)
    constructor = getattr(module, classname)

    return constructor(sim, **args)


class Simulation:
    def __init__(self):
        self.num_users = 32
        self.duration = 1000

        self.channel = None
        self.channel_args = {}

        self.scheduler = None
        self.scheduler_args = {}


class Execution:
    def __init__(self, seed, rate_history, selection_history):
        self.seed = seed
        self.rate_history = rate_history
        self.selection_history = selection_history


def execute(sim, seed):
    channel = create_with_args(sim.channel, sim.channel_args, sim)
    scheduler = create_with_args(sim.scheduler, sim.scheduler_args, sim)
   
    rate_history = []
    selection_history = []
    for t in xrange(sim.duration):
        rates = channel.next_rates()
        rate_history.append(rates)

        active_user = scheduler.get_active_user(rates)
        selection_history.append(active_user)

    rate_history = np.array(rate_history)
    selection_history = np.array(selection_history)

    return Execution(seed, rate_history, selection_history)


def dump_to_string(array):
    with closing(StringIO.StringIO()) as out:
        numpy.save(out, array) 
        return out.getvalue()


def load_from_string(data):
    with closing(StringIO.StringIO(data)) as inp:
        return numpy.load(inp)


create_simulations_table = '''
CREATE TABLE Simulation 
(
    num_users INTEGER, 
    duration INTEGER, 
    chanel TEXT,
    channel_args TEXT,
    scheduler TEXT,
    scheduler_args TEXT
);
'''

create_executions_table = '''
CREATE TABLE Execution
(
    simulation_id INTEGER NOT NULL,
    seed INTEGER,
    rate_history BLOB,
    selection_history BLOB,
    FOREIGN KEY(simulation_id) REFERENCES Simulation(ROWID) ON DELETE CASCADE 
);
'''


class SqlStorage:
    def __init__(self, filename):
        if os.path.isfile(filename):
            raise IOError('file %s already exists' % (filename,))

        self.connection = sqlite3.connect(filename)
        self.connection.execute(create_simulations_table)
        self.connection.execute(create_executions_table)
        self.sim_id = {}

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.connection.commit()
        self.connection.close()

    def add_simulation(self, sim):
        t = (sim.num_users, sim.duration, \
            sim.channel.__name__, json.dumps(sim.channel_args), \
            sim.scheduler.__name__, json.dumps(sim.scheduler_args))
            
        with closing(self.connection.cursor()) as c:
            c.execute('INSERT INTO Simulation VALUES (?, ?, ?, ?, ?, ?)', t)
            self.sim_id[sim] = c.lastrowid

    def add_execution(self, sim, exe):
        if not sim in self.sim_id:
            raise Exception('Simulation not in the database')

        t = (self.sim_id[sim], exe.sim, \
            dump_to_string(exe.rate_history), dump_to_string(exe.selection_history))

        self.connection.execute('INSERT INTO Execution VALUES (?, ?, ?, ?)', t)

