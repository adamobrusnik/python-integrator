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
		self.y = []
	def __repr__(self):
		return self.description + ' ' + self.reaction + ' [' + self.reference + ']' 
	def integrate(self, eedfs):
		emean = []
		rate = []
		for eedf in eedfs:
			eedf_x = eedf.x
			eedf_y = eedf.y
			emean.append(eedf.emean)
			sigma_x = self.x
			sigma_y = self.y	
			# TODO: integration to obtain rate coefficients	

			#eedf_x_new = np.interp(sigma_x, eedf_x, eedf_y, LEFT=eedf_y[0], RIGHT=eedf_y[-1])
			f_eedf_interp = interpolate.interp1d(eedf_x, eedf_y, bounds_error=False, fill_value=0)
			eedf_x_new = f_eedf_interp(2.7)
			print eedf_x_new
			integrand = [x*sigma_y for x in eedf_x_new]
			print sigma_x 
			i_rate = integrate.cumtrapz(integrand, sigma_x)	
			rate.append(i_rate)
		return emean, rate
