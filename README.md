# pylte - network scheduling simulator

This program is a python version of simulator used to obtain results published
in paper "Provable Fairness for TDMA Scheduling" by Marcin Bienkowski, Jarosław
Byrka, Krzysztof Chrobak, Tomasz Jurdzinski and Dariusz Kowalski.

Original simulator is available at https://krzychu@bitbucket.org/krzychu/lte.git, 
but will no longer be developed.

## Installation
Make sure that following packages are installed:
* python 2.7 (python 3 not supported)
* numpy
* matplotlib

You need to clone this repository:
```
git clone https://github.com/krzychu/pylte.git
```
And add `plyte/lib` to your PYTHONPATH:
```
PYHONPATH=$PYTHONPATH:/path/to/repository/lib
```

## Usage
### Running Existing Simulations
Let's assume that you want to run simulations published on INFOCOM conference. Go to
`simulations` directory and issue command:
```
python infocom_simulation.py
```
Program will create `infocom.sql` file. It contains sqlite3 database, and can be 
browsed using `sqlite3` command line utility. If execution terminates with error, delete
or rename previous `infocom.sql` file - simulator protects you from overwriting already
computed results.

In order to plot results you need to use another program from this directory:
```
python infocom_plot.py infocom.sql welfare
```
It will plot welfare for different algorithms over time. Run this program with no arguments
to see other plot options.

### Defining New Simulations
See `infocom_simulation.py` and `infocom_plot.py` for commented example.

## Internals
Simulator works in two stages: simulation and plotting. Simulation is computationaly expensive
so its results are saved to the database, for later processing and plotting.

### Data Flow
Settings of each simulation are stored in `lte.infrastructure.Simulation` object. Simulation
can be executed many times, each time producing a `lte.infrastructure.Execution` object
holding experiment results. Both sorts of objects are saved to the database, to
be later read by plotting tools.

### Main Loop
Main loop of the simulation can be found in `lib/lte/infrastructure.py`:
```python
def execute_once(sim, seed):
    channel = sim.channel(sim, **sim.channel_args)
    scheduler = sim.scheduler(sim, channel, **sim.scheduler_args)
   
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
```

### Database
Database is a sqlite3 database, so python can access it using just standard library. It consists
of just two tables:
```sql
CREATE TABLE Simulation 
(
    num_users INTEGER, 
    duration INTEGER, 
    chanel TEXT,
    channel_args TEXT,
    scheduler TEXT,
    scheduler_args TEXT
);

CREATE TABLE Execution
(
    simulation_id INTEGER NOT NULL,
    seed INTEGER,
    rate_history BLOB,
    selection_history BLOB,
    FOREIGN KEY(simulation_id) REFERENCES Simulation(ROWID) ON DELETE CASCADE 
);
```
`Simulation` holds general settings, while `Execution` contains results of
particular simulation execution. `rate_history` and `selection_history` are
base64 encoded numpy tables of sizes (duration, num\_users) and (duration, 1) 
respectively. Both tables have no explicitly defined primary key, but sqlite
provides special `ROWID` column which is utilized for this purpose. When defining
plots `simulation_id` is required and it's precisely `ROWID` from `Simulation` table.

Convenient database access is provided by `lte.infrastructure.SqlStorage` class.
