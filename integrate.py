import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET
import sys
from classes import *
from functions import *

import matplotlib.pyplot as plt

plt.ion()

if len(sys.argv) != 3:
	raise IOError('Wrong number of arguments!!')

eedf_filename = sys.argv[1]
reactions_filename = sys.argv[2]
#eedf_filename = 'EEDFs.dat'
#reactions_filename = 'aladdin.xml'

eedfs_str = open(eedf_filename).read()
eedfs = parseeedf(eedfs_str)


reactions = cross(reactions_filename)
#print eedfs
for reaction in reactions:
	reaction.integrate(eedfs)
	#print reaction.rate_x
	#print reaction.rate_y
	plt.figure()
	plt.title(reaction.description + ' - reaction rate')
	plt.xlabel('Mean energy [eV]')
	plt.ylabel('Rate Coefficient [1/(m^3*s)]')
	plt.plot(reaction.rate_x, reaction.rate_y)
	plt.savefig('results/' + reaction.description + '.png')
	tosave = reaction.get_rate_string()
	handle = open('results/' + reaction.description + '.dat', 'w').write(tosave)
