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

## Internals
