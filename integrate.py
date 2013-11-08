import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET
import sys
from classes import *
from functions import *

if len(sys.argv) != 3:
	raise IOError('Wrong number of arguments!!')

eedf_filename = sys.argv[1]
reactions_filename = sys.argv[2]
#eedf_filename = 'EEDFs.dat'
#reactions_filename = 'aladdin.xml'

eedfs_str = open(eedf_filename).read()
eedfs = parseeedf(eedfs_str)

reactions = xsams_cross(reactions_filename)
print reactions
for reaction in reactions:
	reaction.integrate(eedfs)
