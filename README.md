Deconvolution of Raman spectra

Written to deconvolute soot spectra

Usage:

	$./Deconvolution.py <FileName> 

Help:

	$./Deconvolution.py --help
	$./Deconvolution.py -h  

Spike detection

The script has an integrated "spike" detector. To detect "spikes" the moving average of two ajacent poins is compared and, if the difference is higher than the threshold value, the point is considered as a spike. If the algorithm fails to detect spikes, the user can specify another threshold value and try again.

Polynomial degree for the baseline

By default the baseline is calculated using a third degree polynomial function. However, the user is able to change the degree of the poly-function if the baseline does not fit the experimental data. A plot with the calculated baseline and the experimental data is displayed after each attempt.

Configuration

Default values are loaded from the configuration file (./config/config/ini). 
To change the initial guess, bounds and the shape of peaks, edit the ./config/initialData.csv

Dependencies

Before runnig this script, please make sure that Python3 and following libraries are 
installed:
	numpy, matplotlib, pandas, peakutils, scipy, argparse, configparser, recordtype, collections
