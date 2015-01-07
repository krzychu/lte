## Channel Model

Algorithms were evaluated in context of two channel models:

### Channel from paper [dronee]. 

Since authors ommited some important details, like channel baudrate, they had to be found elsewhere. 
Table in paper 1 relates SNR values to number of bits in one OFDM symbol, but authors didn't mention 
how many symbols are in each scheduling interval. [lte\_in\_nutshell] contains information
summarised below:

* Scheduling interval is one 1ms 'subframe'
* Scheduling interval consists of two 'slots'
* Each slot contains either 6 or 7 OFDM symbols

So in our model we assume that there are 14 OFDM symbols in one scheduling interval, and number of bits
transmitted is 14 * value from table 1 in [dronee]

Constant A becomes 
```
A = 12 * 3 * 3 * 14 * 4.8 = 7257.6
```
### Stationary Rayleigh channel with no coding scheme 

Linear SNR values for particular user are IID random variables obeying exponential distribution just like in [dronee]. To
calculate number of bits transmitted in each scheduling interval, we use Shannon theorem:

	#bits = bandwidth * log(1 + linear_snr) * interval_length

We assume that bandwidth is 20 MHz (like in real LTE) and maximal achievable SNR is 35 dB. Users are divided into three 
classes differing by expected value of linear SNR distribution:

```
User class	|  Mean		|	% of max achievable bitrate
=======================================================
Good		|	28 dB	|	80
Average		|	21 dB	|	60
Poor		|	10.5 dB	|	30
```

(values above are in decibels to be more readable). Values in 'Mean' column are determined by values in % column, 
and max achievable rate was obtained from Shannon formula for SNR = 35 dB.

We assume that scheduling interval is 1ms. Maximal achievable number of bits transmitted in single scheduling 
interval is 2.51e5, so constant A becomes
```
A = 2.51e5 * 3 * 3 * 12 = 2.51e7
```

## Plot Types

Def: T, L - like in paper
Def: User i state in time t - pair (T(i, t), L(i, t))
Def: Round efficiency - \frac{Number of transferred bits}{Sum of number possible transferred bits for each user}

### Total vs Possible

Each point on this plot is a state of particular user in time t, averaged over all simulation repetitions. 
Black line represents lower bound on transfer proven for UWR algorithm, i.e:
```
y = \delta * x - A 
```
### Channel Rate

Channel rate for one user from each user class (see channel model for more details). To keep this plot readable
I constrained it to 100 slots on horizontal axis.

### Round Efficiency

Empirical cumulative distribution function of round efficiency, where samples are taken from all repetitions of
simulation for particular algorithm.

### Welfare

Welfare function for proportional fair algorithm can be found in  [survey]

Points on this plot represent welfare achieved by particular algoirthm at given point in time averaged over
simulation repetitions.


## Simulation Parameters
```
Duration = 10000 scheduling intervals
Number of users = 3
Number of repetitions for each set of parameters = 10
```

## References

Papers are in simulations/for\_paper directory (on dropbox)
* [dronee] COMCOM\_DRONEE.pdf
* [lte\_in\_nutshell] lte\_in\_nutshell.pdf
* [survey] survey.pdf
