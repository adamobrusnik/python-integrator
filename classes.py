# -*- coding: utf-8 -*-
import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET
from scipy import interpolate
from scipy import integrate

from constants import *
import matplotlib.pyplot as plt

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

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
		""" integrates the cross section with the given EEDF. Takes an eedfClass object as input"""
		gamma = np.sqrt(2*QE/ME)
		emean = []
		rate = []
		i = 0
		
		for eedf in eedfs:
			i=i+1
			eedf_x = np.array(eedf.x)
			eedf_y = np.array(eedf.y)
			t = np.arange(0, eedf_x[-1], 0.01) # new x-points for interpolation of both sigma and the eedf
			sigma_x = np.array(self.x)
			sigma_y = np.array(self.y)
			idx = sigma_x.searchsorted(eedf_x[-1])
		
			sigma_x = sigma_x[0:idx]
			sigma_y = sigma_y[0:idx]
			if len(sigma_x) > 2:
				f_sigma_interp = interpolate.UnivariateSpline(sigma_x, sigma_y, bbox=[sigma_x[0], sigma_x[-1]], k=1, s=0)
				f_eedf_interp = interpolate.UnivariateSpline(eedf_x, eedf_y, bbox=[eedf_x[0], eedf_x[-1]], k=1, s=0)
       				sigma_interpolated = f_sigma_interp(t).clip(min=0)
				eedf_interpolated = f_eedf_interp(t).clip(min=0)
				"""	
				if i == len(eedfs)-1:
					plt.figure()
					plt.plot(sigma_x, sigma_y, 'ro')
					t = np.arange(0, eedf_x[-1], 0.01)
					vals = f_sigma_interp(t).clip(min=0)
					if sigma_y[0] == 0.0:
						idxx = t.searchsorted(eedf_x[0])
						vals[0:idxx] = 0		
					plt.plot(t, vals)
					plt.yscale('log')
					plt.xscale('log')
					plt.axis()
					plt.show()
				"""	
				integrand = sigma_interpolated 
				integrand = eedf_interpolated * t * sigma_interpolated
				i_rate = integrate.simps(integrand, t)
				rate.append(gamma*i_rate)
				emean.append(eedf.emean)
			else:
				#print 'Cross section out of range'
				rate.append(0)
				emean.append(eedf.emean)
		self.rate_x = emean
		self.rate_y = rate
		"""
		plt.figure()
		plt.plot(emean, rate, 'ro')
		plt.show()
		"""
	def mb_integrate(self, T):
		E = self.sigma_x
		MBDF = 2*np.sqrt(E/pi) * np.power(kb*T, -1.5) * exp(-E/(kb*T))
		

	def get_rate_string(self, delimiter='\t', comment='%'):
		final_string = ''
		final_string += comment + ' ' + self.description + '\n'
		final_string += comment + ' ' + self.rate_x_unit + delimiter + self.rate_y_unit + '\n'
		for i in xrange(0, len(self.rate_x)):
			final_string += str(self.rate_x[i]) + delimiter + str(self.rate_y[i]) + '\n'
		return final_string
