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
	def integrate(eedf):
		eedf_x = eedf.x
		eedf_y = eedf.y
		sigma_x = self.x
		sigma_y = self.y	
		# TODO: integration to obtain rate coefficients	
