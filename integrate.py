import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET

from classes import *
from functions import *

if len(sys.argv) != 2:
	raise IOError('Wrong number of arguments!!')

eedf_filename = 'EEDFs.dat'
eedfs_str = open(eedf_filename).read()
eedfs = parseeedf(eedfs_str)

reactions_filename = 'aladdin.xml'
reactions = xsams_cross(reactions_filename)




