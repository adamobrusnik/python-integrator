import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET

class eedfClass:
	def __init__(self):
		self.x = []
		self.y = []
		self.x_unit = 'eV'
		self.y_unit = 'eV^-3/2'
		self.emean = 0.0
		self.desc = 'no EEDF description'
	def __repr__(self):
		return str(self.desc) + '(' + str(elf.emean) +  ' eV)'

class sigmaClass:
	def __init__(self):
		self.reaction = ''
		self.reference = ''
		self.threshold = 0.0
		self.x = []
		self.y = []
	def __repr__(self):
		return self.reaction + ' [' + self.reference + ']' 
	def integrate(eedfs):
		rate_y = []
		for eedf in eedfs:
			eedf_x = eedf.x
			eedf_y = eedf.y
			sigma_x = self.x
			sigma_y = self.y	
			# TODO: integration to obtain rate coefficients	

			eedf_x_new = numpy.interp(sigma_x, eedf_x, eedf_y, LEFT=eedf_y[0], RIGHT=eedf_y[-1])
			print eedf_x_new
