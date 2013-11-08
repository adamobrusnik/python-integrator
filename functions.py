import re, string
import numpy as np
import scipy.integrate as sp_int
import xml.etree.ElementTree as ET


from classes import *

def parseeedf(eedfs_str):
	eedfs_str = eedfs_str.replace('\n\r', '\n').replace('\r\n', '\n')
	eedfs = eedfs_str.split('\n\n')
	eedfs_array = []
	for eedf_str in eedfs:
		eedf_lines = eedf_str.split('\n')
		current_eedf = eedfClass()
		xs = []
		ys = []
		for i in xrange(2, len(eedf_lines)):
			line = eedf_lines[i]
			line_data = line.split('\t')
			try:
				x = float(line_data[0])
				y = float(line_data[1])
			except ValueError:
				pass
			else:
				xs.append(x)
				ys.append(y)

		if len(xs) > 0:
			current_eedf.x = xs
			current_eedf.y = ys
			emean = np.trapz(ys, xs)
			current_eedf.emean = emean
			if eedf_lines[0] != '':
				current_eedf.desc = eedf_lines[0]
			else:
				current_eedf.desc = eedf_lines[1]
			eedfs_array.append(current_eedf)
	return eedfs_array

def xsams_cross(reactions_filename):
	""" parses an XSAMS XML file to otain collisional cross-sections"""
	r_tree = ET.parse(reactions_filename)
	r_root = r_tree.getroot()
	remove_namespace(r_root)
	cross_sections = []
	i = 1
	for process in r_root.iter('CollisionalTransition'):
		dataset = process.find('DataSets/DataSet/TabulatedData')
		xdata = dataset.find('X/DataList').text
		ydata = dataset.find('Y/DataList').text
		desc = process.find('ProcessClass/UserDefinition').text
		desc = '[k' + str(i) + '] ' + desc
		i = i+1	
		#reactants = process.findall('Reactant')
		#for reactant in reactants:
		#	print reactant[0].text
		cross_section = sigmaClass()
				
		xs = str_to_data(xdata)
		ys = str_to_data(ydata)

		cross_section.x = xs
		cross_section.y = ys	
		cross_sections.append(cross_section)
	return cross_sections

def remove_namespace(doc, namespace=u'http://vamdc.org/xml/xsams/1.0'):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

def str_to_data(string, format = 'space-separated'):
	if format == 'space-separated':
		arr = string.split(' ')
		num_arr = []
		for ar in arr:
			if ar != '' and ar != ' ':
				num_arr.append(float(ar))
		return num_arr	

