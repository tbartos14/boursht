## Purpose

This is a cool module I wrote related to signals in ECSE. The intent here is to solve the following:


*how do you guess the frequencies that make up a signal (with noise)?*.

There are two conditions for which
I chose to write this:

1. you receive a list of measurements, which can be at random intervals or not;
2. there is insufficient data to make an educated guess to the length of the period.

Electrical engineers and others may be able to quickly tell that a Fourier transform would very quickly solve this
problem. However, since I am just a freshman and don't quite understand how to apply it outside of a 3Blue1Brown video,
this module approaches it from a different angle with least-squares modeling.

## Method

This module uses the least-squares method to find a model that most closely matches a given signal. This method, which
is normally used in statistics to find linear models for sets of data, involves finding the distance between a specific
linear equation (y = mx + b) at a given point to the actual, experimental value at that point. This distance is squared,
and then summed up with all other squared distances for all other points, and then a total is calculated.

Since points further away from the model contribute significantly more than points closer to the model (due to squaring)
the total should be minimized such that the model follows the points most closely. This is called the least-squares
method. Normally, for linear models, the least-squares method is quite easy to do on a large scale, using some simple math.
However, for sinusoidal waves, the least-squares method is significantly harder and I haven't exactly figured out how to
do it yet.

Therefore, this method is implemented in a much more primitive way by checking a given range of frequencies across phases
from 0 to 2π. The function returns the maximum and minimum least-squares value for each frequency (between the
different phases tested). Now, to explain what this data means;

In terms of sinusoidal functions, there is technically a maximum least-squares value (which
I will refer to as perfect 'anti-harmony') and a minimum least-squares value (which I call 'harmony'). Generally,
harmony occurs when the model frequency and model phase match the real signal frequency and phase. Anti-harmony occurs
when a model signal is π radians out of phase with the real signal but correctly guesses the frequency. Since
anti-harmony and harmony will occur at the same frequency, the maximum and minimum least-squares value across all
frequencies signify the **the actual frequency of the signal.**

## How to Use

1. Find some data, in the form of two-value lists inside a list. Values need not be sorted. Example:

[[val_1, time_1], [val_2, time_2], ... [val_n, time_n]]

2. Find least-squares values by using the *boursht* function.

results = boursht(data)

3. Find the least-squares peaks using *salam* function.

frequencies = salam(results)

4. Optionally, graph your results using the *klobasa* function.

klobasa(results)

## Examples

(This is taken directly from the *`if __name__ == '__main__'`*)

    ## show an example graph, using random module for messed-up measurement data
    # (can be modified, so have fun)
    import random

    ##seed it if you would like to compare results
    #random.seed(2)

    ## constants
    measurements = 500  ## over 1 second
    ## increasing this will increase the time taken, but can "find" more frequencies, as well as
    ## reducing fake "hits"

    frequency1 = 140  ## in rads/sec
    ## frequency of the primary signal to be added

    frequency2 = 260  ## in rads/sec
    ## frequency of the secondary signal to be added

    variability = 1  ## scalar
    ## "scales" how messed up/noisy the signal is. Increasing will cause frequencies with lower
    ## amplitudes to be ignored, as the amount of "hits" can increase with signals that
    ## are more noisy

    phase = math.pi  ## radians
    ## adjusts the phase of the signal, should not impact results significantly. Simply shows that the
    ## program can detect frequencies even when the signal does not begin at t = 0

    ## generate a sine wave with noise

    ## generate random time points at which measurements occur
    ## (intended to simulate an environment where other methods would work poorly)
    times = [random.random() for i in range(measurements)]

    ## or equally spaced time points
    #times = [i / measurements for i in range(measurements)]
    times.sort()

    ## ok, time to bump it with noise
    signal = []
    for index in range(len(times)):
        signal.append([times[index],
            0.5 * math.sin(frequency1 * times[index] + phase) + 0.5 * math.sin(frequency2 * times[index] + phase) \
            + (variability * (0.5 - random.random()))])

    results = boursht(signal, freq_range=range(10,500))
    klobasa(results)
    salam(results)