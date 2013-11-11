# -*- coding: utf-8 -*-
import re, string, os, shutil
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET
import sys
from classes import *
from functions import *

import matplotlib.pyplot as plt

#plt.ion()

if len(sys.argv) != 4:
	raise IOError('Wrong number of arguments!!')

eedf_filename = sys.argv[1]
reactions_filename = sys.argv[2]
output_dir = sys.argv[3]
#eedf_filename = 'EEDFs.dat'
#reactions_filename = 'aladdin.xml'

try:
	os.mkdir('results')
except OSError:
	print 'The directory ./results exists, skipping'

output_dir_full = 'results/' + output_dir + '/'
output_dir_full = output_dir_full.replace('//', '/')
try:
	os.mkdir(output_dir_full)
except OSError:
	print bcolors.OKBLUE + 'The directory ./' + output_dir_full + ' already exists!!!' + bcolors.ENDC
	choice = ''
	while choice != 'y' and choice != 'N':
		choice = raw_input(bcolors.FAIL + 'Do you want to rewrite the output directory? [y/N]: ' + bcolors.ENDC)
	if choice == 'y':
		shutil.rmtree(output_dir_full)
		os.mkdir(output_dir_full)
	else:
		print bcolors.OKGREEN + 'Nothing to do!' + bcolors.ENDC
		sys.exit()	

eedfs_str = open(eedf_filename).read()
eedfs = parseeedf(eedfs_str)


reactions = cross(reactions_filename)
num_reactions = len(reactions)
i = 1
for reaction in reactions:
	reaction.integrate(eedfs)
	
	plt.figure()
	plt.title(reaction.description + ' - reaction rate')
	plt.xlabel('Mean energy [eV]')
	plt.ylabel('Rate Coefficient [1/(m^3*s)]')
	plt.plot(reaction.rate_x, reaction.rate_y)
	plt.savefig(output_dir_full + reaction.description + '.png')
	
	tosave = reaction.get_rate_string()
	handle = open(output_dir_full + reaction.description + '.dat', 'w').write(tosave)
	print bcolors.OKBLUE + str(i) + '/'+ str(num_reactions)  +':\t' + str(reaction.description) + bcolors.ENDC
	i=i+1

print bcolors.OKGREEN + 'All OK!' + bcolors.ENDC
