'''
Signal Spectrum Analysis, done with math module and matplotlib module
'''
import math
import matplotlib.pyplot as plt

def boursht(measurements, freq_range=range(10,1000),phase_measrs=30):
    """
    This function determines the frequencies in a given set of signal measurements. It does using
    least-squares, which calculates the "closest" approximation of a best-fit curve. In this case, it is
    a sinusoidal curve.
    In order to find which single frequency/combined frequencies best "match" a signal, the least-squares
    value is found for all frequencies in a given range (given by freq_range), over all possible phases
    (number of measurements given by phase_measrs). Since this least-squares value showcases how close a guess
    is to the correct signal, the lower the value, the closer the guess matches the signal. This could be
    interpreted as harmony. However, since the reverse applies for higher least-squares values, which can be
    interpreted as 'anti-harmony'.
    In order to interpret the data, use the visualize function to see the behavior of the least-squares value
    for frequencies that closely match the real signal.

    :param measurements: measurements input as a list of two-value lists, example:
    [[time_1, val_1], [time_2, val_2], ...]. Function only works nicely if the values are close to -1 ≤ x ≤ 1

    :param freq_range: list/range compatible with list comprehension. Examples:
    [20, 40, 80, 160, 320], range(1, 1000), range(20, 1000, 20). Default is range(10,1000)
    Tested frequencies of 0 or close to 0 will produce funky results. Proceed with caution.

    :param phase_measrs:  integer, number of tests from 0 to 2π. This ensures that signals with phase
    are correctly measured. Number from 10-50 recommended, but may be lowered to speed up the function.
    Default is 30. Increasing it beyond 50 will not yield better/more interesting results.

    :return: list of 3-values lists, as follows:
    [[max_least_squares_value, min_least_squares_value, frequency],...
    ...]
    """

    ## collect data
    points = measurements.copy()
    measurement_count = len(measurements)

    ## distance formula =
    def least_sq_dis(frequency, phase, data):
        ## data in this case is an individual point, frequency in rads/sec, and phase is in radians
        t = data[0]
        y_0 = data[1]
        y = math.sin(frequency * t + phase)
        return (y_0 - y) ** 2

    ## arrays built for 3D matplotlib graph (not really worth using though), also calculations
    freq_array = [[i] * phase_measrs for i in freq_range]
    phase_array = [[inter * 2 * math.pi / phase_measrs for inter in range(phase_measrs)] for i in freq_range]
    results_array = [[0] * phase_measrs for i in freq_range]

    ## ok, now we calculate the least-squares
    for index1, pair in enumerate(freq_array):
        for index2 in range(len(pair)):
            for point in points:
                results_array[index1][index2] += least_sq_dis(freq_array[index1][index2], phase_array[index1][index2],point)

    ## now we wish to collect the max/min frequencies for frequency tests, across all phase tests
    freq = [i for i in freq_range]
    maxs = []
    mins = []

    for index1, pair in enumerate(results_array):
        min_ls = math.inf
        max_ls = 0
        for index2 in range(len(pair)):
            lst_square = 0
            for point in points:
                lst_square += least_sq_dis(freq_array[index1][index2], phase_array[index1][index2], point)
            if lst_square < min_ls:
                min_ls = lst_square
            if lst_square > max_ls:
                max_ls = lst_square
        maxs.append(max_ls)
        mins.append(min_ls)

    ## bundle and send
    return_list = []
    for index in range(len(freq)):
        return_list.append([maxs[index],mins[index],freq[index]])
    return return_list


def salam(output_data):
    """
    This function simply returns what is deemed to be a frequency that definitely makes a part of the signal.
    "Definitely" is defined as 4 times greater than the average least-squares value, and is a local maximum.

    :param output_data: return from boursht()

    :return: list of two lists of two-value lists, for signals that pass the test, for maximum and minimum
    least-squares values. Example:
    [[[frequency_1, smallest_least_sq_value_1], ...], [[frequency_2, largest_least_sq_value_1], ...]]
    """

    freq = []
    mins = []
    maxs = []

    ## unpack
    for point in output_data:
        freq.append(point[2])
        mins.append(point[1])
        maxs.append(point[0])

    ## find the averages for the deviation
    avg_max = sum(maxs)/len(maxs)
    avg_min = sum(mins)/len(mins)
    avg = (avg_max + avg_min)/2

    min_freqs = []
    max_freqs = []
    for index in range(1, len(freq) - 1):
        if mins[index] < mins[index - 1] and mins[index] < mins[index + 1] and mins[index] < (avg - 4 * (avg - avg_min)):
            min_freqs.append([freq[index],mins[index]])
        if maxs[index] > maxs[index - 1] and maxs[index] > maxs[index + 1] and maxs[index] > (avg - 4 * (avg - avg_max)):
            max_freqs.append([freq[index],maxs[index]])

    return [min_freqs, max_freqs]


def klobasa(data, highlight_hits=True):
    """
    This function just uses matplotlib to plot the values returned from boursht. Pretty cool to visualize.

    :param data: literally just the data you got from the other function

    :param highlight_hits: Default True. Highlights in green the expected 'hits' for frequency.

    :return: None
    """

    freq = []
    mins = []
    maxs = []

    ## unpack
    for point in data:
        freq.append(point[2])
        mins.append(point[1])
        maxs.append(point[0])

    fig = plt.figure()
    plot = fig.add_subplot(111)

    if highlight_hits:
        highlight_points = salam(data)
        highlight_min = highlight_points[0]
        highlight_max = highlight_points[1]
        min_freqs = []
        min_vals = []
        max_freqs = []
        max_vals = []
        for point in highlight_min:
            min_freqs.append(point[0])
            min_vals.append(point[1])

        for point in highlight_max:
            max_freqs.append(point[0])
            max_vals.append(point[1])

    plot.scatter(freq, maxs, s=10, c='b', marker='s', label="Minimum least-squares")
    plot.scatter(freq, mins, s=10, c='r', label="Maximum least-squares")

    if highlight_hits:
        plot.scatter(min_freqs, min_vals, s=150, c='g', label="Predicted Signal Freq.")
        plot.scatter(max_freqs, max_vals, s=150, c='g')
    plt.legend(loc='upper right')
    plt.show()


if __name__ == "__main__":
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
