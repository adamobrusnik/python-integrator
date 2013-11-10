import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET
from scipy import interpolate
from scipy import integrate

class eedfClass:
	def __init__(self):
		self.x = []
		self.y = []
		self.x_unit = 'eV'
		self.y_unit = 'eV^-3/2'
		self.emean = 0.0
		self.desc = 'no EEDF description'
	def __repr__(self):
		return str(self.desc) + '(' + str(round(self.emean, 3)) +  ' eV)'

class sigmaClass:
	def __init__(self):
		self.reaction = ''
		self.description = ''
		self.reference = ''
		self.threshold = 0.0
		self.x = []
		self.x_unit = 'eV'
		self.y = []
		self.y_unit = 'm^2'
		self.rate_x = []
		self.rate_y = []
		self.rate_x_unit = 'eV'
		self.rate_y_unit = '1/(m^3*s)'
	def __repr__(self):
		return self.description + ' ' + self.reaction + ' [' + self.reference + ']' 
	def integrate(self, eedfs):
		emean = []
		rate = []
		for eedf in eedfs:
			eedf_x = np.array(eedf.x)
			eedf_y = np.array(eedf.y)
			sigma_x = np.array(self.x)
			sigma_y = np.array(self.y)

			f_eedf_interp = interpolate.interp1d(eedf_x, eedf_y, bounds_error=False, fill_value=0)
			eedf_x_new = f_eedf_interp(2.1)
			eedf_x_new = np.array(eedf_x_new)
			integrand = eedf_x_new * sigma_y
			i_rate = integrate.simps(integrand, sigma_x)
			rate.append(i_rate)
			emean.append(eedf.emean)
		self.rate_x = emean
		self.rate_y = rate
	def get_rate_string(self, delimiter='\t', comment='%'):
		final_string = ''
		final_string += comment + ' ' + self.description + '\n'
		final_string += comment + ' ' + self.rate_x_unit + delimiter + self.rate_y_unit + '\n'
		for i in xrange(0, len(self.rate_x)):
			final_string += str(self.rate_x[i]) + delimiter + str(self.rate_y[i]) + '\n'
		return final_string
