#! /usr/bin/python2
import csv
import numpy as np
import matplotlib.pyplot as plt
import re
from math import log

# DataSet TODO = finish this.
# This class is designed to hold an entire dataset for easy manipulation
class DataSet:
	def __init__(self):
		self.axis = []
		self.data = np.array([])
	
	def add(self,dat):
		self.axis = [fixString(dat[0,0]),fixString(dat[0,1])]
		self.data = dat[1:,:]

# importCSV
# This function imports CSV files that have been written by HFSS.
def readCSV(fn): # fn = file name
	fread = csv.reader(open(fn),delimiter=',')
	data = []
	for row in fread:
		newCol = []
		for col in row:
			try:
				newCol.extend([float(col)])
			except:
				#newCol.extend([col])
				pass
		if (newCol != []):
			data.extend([newCol])

	return np.array(data)


def fixString(s):
	s = re.sub('_',' ',s) # Change underscores to spaces
	s = re.sub('\[\]','',s) # Empty units are removed
	s = s.strip() # Remove extra whitespace
	return s

# Number of valid data values
def numValid(A):
	Valid = 0 # number of valid entries
	for i in A:
		if (i != ''):
			Valid += 1
	return Valid

# Return the valid value
def getValid(A):
	for i in A:
		if (i != ''):
			return float(i)

# collapseArray(A)
# This function takes an array that has redundant columns that contain
# non-contradictory data and merges the redundant columns. It does this by
# finding the unique column names and then creating a mapping between the
# column name and the redundant column numbers. For each 
def collapseArray(A):
	Out = []
	# Find Unique Columns
	Cols = []
	for val in set(A[0,:]):
		Cols.extend([str(val)])
	Out.extend([Cols])
	# Find Mappings
	Map = {}	# Create values
	for val in Cols: # For each column name
		mapping = [] # create a mapping list
		for i in range(len(A[0,:])): # for each column in A
			if (A[0,i] == val): # If the top row is the current unique value
				mapping.extend([i]) # add the column number to the map.
		Map[val]=mapping # store the complete mapping in the dictionary
	
	# Copy correct values from A to Out
	for row in range(1,len(A[:,0])): # for each row in the input vector
		newRow = []
		for col in Cols:	# for each unique column
			data = [] # Create temp data vector
			for d in Map[col]: # copy data in to data vector
				data.extend([A[row,d]])
			#print(str(data))	
			newRow.extend([getValid(data)])
		Out.extend([newRow])
	
	return np.array(Out)
################################################################################