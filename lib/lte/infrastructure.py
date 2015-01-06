import importlib
import numpy
import sqlite3
import os.path
import json
import pdb
import base64
from contextlib import closing
import cStringIO as StringIO


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

    def get_rate_shape(self):
        return self.rate_history.shape

    def get_duration(self):
        return self.rate_history.shape[0]

    def get_num_users(self):
        return self.rate_history.shape[1]

    def get_transmissions(self):
        trans = numpy.zeros(self.get_rate_shape())
        ts = range(self.get_duration())
        hs = self.selection_history
        trans[ts, hs] = rates[ts, hs]
        return trans


def execute_once(sim, seed):
    channel = sim.channel(sim, **sim.channel_args)
    scheduler = sim.scheduler(sim, **sim.scheduler_args)
   
    rate_history = []
    selection_history = []
    for t in xrange(sim.duration):
        rates = channel.next_rates()
        rate_history.append(rates)

        active_user = scheduler.get_active_user(rates)
        selection_history.append(active_user)

    rate_history = numpy.array(rate_history)
    selection_history = numpy.array(selection_history)

    return Execution(seed, rate_history, selection_history)


def execute_all(storage, sim, num_repetitions):
    storage.add_simulation(sim)
    for i in xrange(num_repetitions):
        execution = execute_once(sim, i)
        storage.add_execution(sim, execution)


def dump_to_string(array):
    with closing(StringIO.StringIO()) as out:
        numpy.save(out, array) 
        return base64.b64encode(out.getvalue())


def load_from_string(data):
    with closing(StringIO.StringIO(base64.b64decode(data))) as inp:
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
        self.existed = os.path.isfile(filename)
        self.sim_id = {}
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = sqlite3.Row

        if not self.existed:
            self.connection.execute(create_simulations_table)
            self.connection.execute(create_executions_table)

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.connection.commit()
        self.connection.close()

    def add_simulation(self, sim):
        assert not self.existed
        t = (sim.num_users, sim.duration, \
            str(sim.channel), json.dumps(sim.channel_args), \
            str(sim.scheduler), json.dumps(sim.scheduler_args))
            
        with closing(self.connection.cursor()) as c:
            c.execute('INSERT INTO Simulation VALUES (?, ?, ?, ?, ?, ?)', t)
            self.sim_id[sim] = c.lastrowid

    def add_execution(self, sim, exe):
        assert not self.existed
        if not sim in self.sim_id:
            raise Exception('Simulation not in the database')

        t = (self.sim_id[sim], exe.seed, \
            dump_to_string(exe.rate_history), dump_to_string(exe.selection_history))

        self.connection.execute('INSERT INTO Execution VALUES (?, ?, ?, ?)', t)

    def parse_execution(self, row):
        seed = int(row['seed'])
        rates = load_from_string(row['rate_history'])
        selections = load_from_string(row['selection_history'])
        return Execution(seed, rates, selections)

    def get_execution(self, execution_rowid):
        q = 'SELECT * FROM Execution WHERE rowid = ?'
        t = (execution_rowid,)
        with closing(self.connection.execute(q, t)) as c:
            return self.parse_execution(c.fetchone())

    def get_all_executions(self, simulation_rowid):
        q = 'SELECT * FROM Execution WHERE simulation_id = ?'
        t = (simulation_rowid,)
        with closing(self.connection.execute(q, t)) as c:
            return map(self.parse_execution, c.fetchall())

