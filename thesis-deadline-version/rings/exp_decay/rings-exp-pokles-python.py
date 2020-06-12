import subprocess
from os import system, remove,  chdir
from tabulate import tabulate
from sympy import *
import numpy as np
from math import pi


def edges(n):
	location = 0
	edges = [[0,n-1]]
	for i in range(n-1):
		edges.append([location, location+1])
		location += 1
	return edges


def cut(label):
	return sum(map(int, label.split())) - 2*len(label.split()) if len(label.split())>1 else sum(map(int, label.split()))


# label is used to unambiguously identify a group
def label(state):
	label = []
	value = state[0]
	repetition = 0
	for i in range(len(state)+1):
		if state[i%len(state)] == value:
			if i == len(state):
				if len(label) == 0:
					label.append('0') 
				label[0] = str( int(label[0]) + repetition)
			repetition += 1
		else:
			label.append(str(repetition))
			repetition = 1
			value = state[i%len(state)]
	return label


def groupsOfStates(n):
	states = {}
	for i in range(2**(n-1)): #n-1 because we automaticaly add also NOT the generated state
		s = str(bin(i))[2:]
		s = (n-len(s))*"0" + s
		mynot = ''
		for znak in s:
			mynot += '0' if znak == '1' else '1'
		e = edges(n)
		k = label(s)
		used = False
		for i in range(n):
			temp = rotate(k,i)
			k1 = " ".join(temp)
			temp.reverse()
			k2 = " ".join(temp)
			if k1 in states.keys():
				states[k1].append(s)
				states[k1].append(mynot)
				used = True
				break
			elif k2 in states.keys():
				states[k2].append(s)
				states[k2].append(mynot)
				used = True
				break
		if used == False:
			k1 = " ".join(k)
			states[k1] = []
			states[k1].append(s)
			states[k1].append(mynot)
	return states


def hamming_distance(string1, string2):
	diff = 0
	for c1, c2 in zip(string1, string2):
		if c1 != c2:
			diff += 1
	return diff


def rotate(array, x):
	return array[-x:] + array[0:-x]


def create_cut_to_amplitude_dict(n):
	l = str(n)
	states = groupsOfStates(n)

	amplitudes = {}
	labels = states.keys()

	constants = {} #cut to (number of sinuses to how many times repeated) - all we need to construct the amplitude
	#it's enough to compute the amplitude for representant of the group
	representant = states[l][0]

	#here we fill the constants directory - gain all informations needed for amplitude creation
	for label in labels:

		if cut(label) not in constants.keys():
			constants[ cut(label) ] = {}

		for state in states[label]:
			numOfSinuses = hamming_distance(representant, state)

			if numOfSinuses in constants[ cut(label) ].keys():
				constants[ cut(label) ][ numOfSinuses ] += 1
			else:
				constants[ cut(label) ][ numOfSinuses ] = 1

	cut_to_amplitude = {}
	x = Symbol('x', real=True)
	for c in constants.keys():
		amplitude = 0
		for numOfSin in constants[c].keys():
			coef = constants[c][numOfSin]
			if numOfSin == n:
				amplitude += coef*(1j*sin(x))**n
			elif numOfSin == 0:
				amplitude += coef*cos(x)**n
			else:
				amplitude += coef*(1j*sin(x))**numOfSin * cos(x)**(n - numOfSin)
		cut_to_amplitude[c] = amplitude/sqrt(2**n)
	return cut_to_amplitude

for n in range(4,20,2):
	x = Symbol('x', real=True)
	lengths = []
	for ecut, ampl in create_cut_to_amplitude_dict(n).items():
		# print(ecut, ':\n', ampl)
		max_value_of_ampl = 0
		for b in np.arange(0, pi, 0.001):
			new_value = abs(ampl.subs(x,b))
			max_value_of_ampl = max(max_value_of_ampl, new_value)
		print(ecut,': ', max_value_of_ampl)
		lengths.append(max_value_of_ampl)
	print(n, ' ', sum(lengths), " ", sum(lengths)^2)
