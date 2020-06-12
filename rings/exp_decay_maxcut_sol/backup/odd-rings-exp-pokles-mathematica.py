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
		s = (n-len(s))*'0' + s
		mynot = ''
		for znak in s:
			mynot += '0' if znak == '1' else '1'
		e = edges(n)
		k = label(s)
		used = False
		for i in range(n):
			temp = rotate(k,i)
			k1 = ' '.join(temp)
			temp.reverse()
			k2 = ' '.join(temp)
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
			k1 = ' '.join(k)
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
		
	#here we create the amplitude for l
	cut_to_amplitude = {}
	for c in constants.keys():
		amplitude = ''
		for numOfSin in constants[c].keys():
			coef = str(constants[c][numOfSin])
			if coef != '1':
				amplitude += coef + ' '
			if numOfSin == n:
				amplitude += f'(I Sin[β])^{n}'
			elif numOfSin == 0:
				amplitude += f'Cos[β]^{n}'
			else:
				amplitude += f'(I Sin[β])^{numOfSin} Cos[β]^{n - numOfSin}'
			amplitude += ' + '
		cut_to_amplitude[c] = '(' + amplitude[:-3] + f')/Sqrt[2]^{n}' #[:-3] to remove additional ' + '
	return cut_to_amplitude

# #UPPER BOUND
# with open('upper bound', 'w') as data:
# 	for n in range(3,21,2):
# 		with open('maxima.txt', 'w') as f:#to create the file
# 			pass

# 		for ecut, ampl in create_cut_to_amplitude_dict(n).items():
# 			# print(ecut, ':\n', ampl)

# 			with open('maximize.nb', 'w') as mathematica, open('template.txt', 'r') as template:
# 				mathematica.write(	'amplitude[β_] := ' + ampl + '\n\n' +
# 							  		'magnitude[x_] := Abs[amplitude[x]]^2 // ComplexExpand\n')
# 				for line in template:
# 					mathematica.write(line)

# 			#here we run the mathematica file and then we remove it
# 			subprocess.run(['math', '-script', 'maximize.nb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 			remove('maximize.nb')

# 		with open('maxima.txt', 'r') as f:
# 			bound = sum(map(lambda x: float(x.strip().replace('*^','e')),f.readlines()))
# 		print(n, ' ', bound, ' ', bound**2)
# 		data.write(f'{n}\t{bound**2}\n')
# 		remove('maxima.txt')

#MAXIMIZING P₀₀...₀
with open('maximizing p₀₀...₀', 'w') as data, open('minimizing average energy', 'w') as data2:
	for n in range(3,21,2):
		with open('maxima.txt', 'w') as f, open('maxima2.txt', 'w') as f2:#to create the files
			pass

		amplitude = ''
		for ecut, ampl in create_cut_to_amplitude_dict(n).items():
			amplitude += f' + Exp[-I {ecut} γ]({ampl})'
		amplitude = amplitude[3:]
		print(f'{n}:',amplitude)

		with open('maximize.nb', 'w') as mathematica, open('template2.txt', 'r') as template:
			mathematica.write(	'amplitude[β_, γ_] := ' + amplitude + '\n\n' +
						  		'magnitude[x_, y_] := Abs[amplitude[x, y]]^2 // ComplexExpand\n')
			for line in template:
				mathematica.write(line)
		#here we run the mathematica file and then we remove it
		subprocess.run(['math', '-script', 'maximize.nb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		remove('maximize.nb')

		with open('maxima.txt', 'r') as f, open('maxima2.txt', 'r') as f2:
			prob1 = sum(map(lambda x: float(x.strip().replace('*^','e')),f.readlines()))
			prob2 = sum(map(lambda x: float(x.strip().replace('*^','e')),f2.readlines()))
		data.write(f'{n}\t{prob1}\n')
		data2.write(f'{n}\t{prob2}\n')
		remove('maxima.txt')
		remove('maxima2.txt')

system('gnuplot rings.gnuplot')