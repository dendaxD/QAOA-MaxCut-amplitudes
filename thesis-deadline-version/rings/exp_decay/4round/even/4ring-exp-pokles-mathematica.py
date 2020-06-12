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


def create_amplitude(n):
	states = groupsOfStates(n)
	amplitudes = {}
	cuts = {}
	labels = states.keys()
	for l in labels:
		cuts[l] = cut(l)

	#MAIN FOR LOOP
	computation_constants = {} #{label -> {constants}}
	for l in labels:

		constants = {} #cut to (number of sinuses to how many times repeated) - all we need to construct the amplitude
		#it's enough to compute the amplitude for representant of the group
		constants2 = {}
		representant = states[l][0]

		#here we fill the constants directory - gain all informations needed for amplitude creation
		for group in labels:
			constants2[group] = {}

			if cuts[group] not in constants.keys():
				constants[ cuts[group] ] = {}

			if cuts[group] not in constants2[group].keys():
				constants2[group][ cuts[group] ] = {}

			for state in states[group]:
				numOfSinuses = hamming_distance(representant, state)

				if numOfSinuses in constants[ cuts[group] ].keys():
					constants[ cuts[group] ][ numOfSinuses ] += 1
				else:
					constants[ cuts[group] ][ numOfSinuses ] = 1

				if numOfSinuses in constants2[group][ cuts[group] ].keys():
					constants2[group][ cuts[group] ][ numOfSinuses ] += 1
				else:
					constants2[group][ cuts[group] ][ numOfSinuses ] = 1
		
		#here we create the amplitude for l
		amplitude = ""
		for c in constants.keys():
			amplitude += "Exp[" + str(-c) + " I y" + "] ("
			for numOfSin in constants[c].keys():
				m = str( constants[ c ][ numOfSin ] )
				if numOfSin == n:
					amplitude += ( m + " (I Sin[x])^" + str(n) )
				elif numOfSin == 0:
					amplitude += ( m + " Cos[x]^" + str(n) )
				else:
					amplitude += ( m + " (I Sin[x])^" + str(numOfSin) + " Cos[x]^" + str(n - numOfSin) )
				amplitude += " + "
			amplitude = amplitude[:-3] + ") + "
		amplitudes[l] = amplitude[:-3] #[:-3] to remove additional ' + '
		computation_constants[l] = constants2

	#second round
	amplitudes2 = {}
	for l in labels:	
		amplitude = ""
		for l2 in labels:
			for c in computation_constants[l][l2].keys():
				amplitude += "Exp[" + str(-c) + " I y2" + "]*(" + amplitudes[l2] + ")*("
				for numOfSin in computation_constants[l][l2][c].keys():
					m = str( computation_constants[l][l2][ c ][ numOfSin ] )
					if numOfSin == n:
						amplitude += ( m + " (I Sin[x2])^" + str(n) )
					elif numOfSin == 0:
						amplitude += ( m + " Cos[x2]^" + str(n) )
					else:
						amplitude += ( m + " (I Sin[x2])^" + str(numOfSin) + " Cos[x2]^" + str(n - numOfSin) )
					amplitude += " + "
				amplitude = amplitude[:-3] + ") + "
		#[:-3] to remove additional ' + '
		amplitudes2[l] = amplitude[:-3]

	#third round
	amplitudes3 = {}
	for l in labels:	
		amplitude = ""
		for l2 in labels:
			for c in computation_constants[l][l2].keys():
				amplitude += "Exp[" + str(-c) + " I y3" + "]*(" + amplitudes2[l2] + ")*("
				for numOfSin in computation_constants[l][l2][c].keys():
					m = str( computation_constants[l][l2][ c ][ numOfSin ] )
					if numOfSin == n:
						amplitude += ( m + " (I Sin[x3])^" + str(n) )
					elif numOfSin == 0:
						amplitude += ( m + " Cos[x3]^" + str(n) )
					else:
						amplitude += ( m + " (I Sin[x3])^" + str(numOfSin) + " Cos[x3]^" + str(n - numOfSin) )
					amplitude += " + "
				amplitude = amplitude[:-3] + ") + "
		#[:-3] to remove additional ' + '
		amplitudes3[l] = amplitude[:-3]


	#fourth round
	l = str(n)	
	amplitude = ""
	for l2 in labels:
		for c in computation_constants[l][l2].keys():
			amplitude += "Exp[" + str(-c) + " I y4" + "]*(" + amplitudes3[l2] + ")*("
			for numOfSin in computation_constants[l][l2][c].keys():
				m = str( computation_constants[l][l2][ c ][ numOfSin ] )
				if numOfSin == n:
					amplitude += ( m + " (I Sin[x4])^" + str(n) )
				elif numOfSin == 0:
					amplitude += ( m + " Cos[x4]^" + str(n) )
				else:
					amplitude += ( m + " (I Sin[x4])^" + str(numOfSin) + " Cos[x4]^" + str(n - numOfSin) )
				amplitude += " + "
			amplitude = amplitude[:-3] + ") + "
	 #[:-3] to remove additional ' + '
	return f'({amplitude[:-3]})/Sqrt[2^{n}]'


#MAXIMIZING P₀₀...₀
with open('maximizing p₀₀...₀', 'w') as data, open('minimizing average energy', 'w') as data2:
	for n in range(8,9,2):
		with open('maxima.txt', 'w') as f:#to create the files
			pass

		# amplitude = ''
		# for ecut, ampl in create_cut_to_amplitude_dict(n).items():
		# 	amplitude += f' + Exp[-I {ecut} γ]({ampl})'
		# amplitude = amplitude[3:]
		amplitude = create_amplitude(n)
		print(amplitude)

		with open(f'maximize{n}.nb', 'w') as mathematica, open('template.txt', 'r') as template:
			mathematica.write(	'amplitude[x_, y_, x2_, y2_, x3_, y3_, x4_, y4_] := ' + amplitude + '\n\n' +
						  		'magnitude[x_, y_, x2_, y2_, x3_, y3_, x4_, y4_] := Abs[amplitude[x, y, x2, y2, x3, y3, x4, y4]]^2\n')
			for line in template:
				mathematica.write(line)
		#here we run the mathematica file and then we remove it
		subprocess.run(['math', '-script', f'maximize{n}.nb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# remove('maximize.nb')

		with open('maxima.txt', 'r') as f:
			prob1 = sum(map(lambda x: float(x.strip().replace('*^','e')),f.readlines()))
		data.write(f'{n}\t{prob1}\n')
		remove('maxima.txt')


system('gnuplot rings.gnuplot')