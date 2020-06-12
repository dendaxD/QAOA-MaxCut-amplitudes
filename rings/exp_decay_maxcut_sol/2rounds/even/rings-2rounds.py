import subprocess
from os import system, remove
from tabulate import tabulate

def edges(n):
	location = 0
	edges = [[0,n-1]]
	for i in range(n-1):
		edges.append([location, location+1])
		location += 1
	return edges


def cut(state, edges):
	cut = 0
	for edge in edges:
		cut += 1 if state[edge[0]] == state[edge[1]] else -1
	return cut


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
		c = cut(s,e)
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


def compare(string1, string2):
	diff = 0
	for c1, c2 in zip(string1, string2):
		if c1 != c2:
			diff += 1
	return diff


def rotate(array, x):
	return array[-x:] + array[0:-x]



#THE MOST IMPORTANT
def amplitudes(n, states):

	amplitudes = {}
	cuts = {}
	labels = states.keys()
	for l in labels:
		cuts[l] = cut(states[l][0], edges(n))

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
				numOfSinuses = compare(representant, state)

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
			amplitude += "Exp[" + str(-c) + " I y/2" + "] ("
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
		amplitudes2[l] = amplitude[:-3] #[:-3] to remove additional ' + '
	return amplitudes2



# ^
# | FUNCTIONS
##########################################################################################################################
# | CODE
# v



start = 3
end = 6
for numberOfQubits in range(start,end+1):
	states = groupsOfStates(numberOfQubits)

	for label1, amplitude in amplitudes(numberOfQubits, states).items():
		with open(str(numberOfQubits) + "v" + label1 + ".nb", "w") as file, open("templates/results-template.nb", "r") as template:
			file.write	(	"$Conjugate[x_] := x /. Complex[a_, b_] :> a - I b;\n" +
					  		"function[x_, y_, x2_, y2_] := $Conjugate[" + amplitude + "]*(" + amplitude + ")\n" +
					  		"ammount = " + str(numberOfQubits) + ";\n" + 
					  		"name = \"" + str(numberOfQubits) + "v" + label1 + "\";\n" +
					  		"states = " + str(len(states[label1])) + ";\n\n"
			)
			for line in template:
				file.write(line)
		subprocess.run(["math", "-script", str(numberOfQubits) + "v" + label1 + ".nb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		if numberOfQubits < 7:
			with open("templates/amplitudes-probabilities.tex", "r") as probtemplate, open("amplitudes-probabilities.tex", "w") as prob, open("amplitudes.txt", "r") as am:
				for line in probtemplate:
					prob.write(line)
				x = am.readlines()
				for line in x:
					line = line.replace("\"","").replace("\\\\","\\").replace("\\\n", "")
					prob.write(line) 
				prob.write("\\end{document}")
		remove(str(numberOfQubits) + "v" + label1 + ".nb")

		
		with open("MathematicaFiles/" + str(numberOfQubits) + "v" + label1 + ".nb", "w") as f, open("templates/useful-template.nb", "r") as template:
			f.write	(	"$Conjugate[x_] := x /. Complex[a_, b_] :> a - I b;\n" +
					  		"function[x_, y_, x2_, y2_] := $Conjugate[" + amplitude + "]*(" + amplitude + ")\n" +
					  		"ammount = " + str(numberOfQubits) + ";\n" + 
					  		"name = \"" + str(numberOfQubits) + "v" + label1 + "\";\n" +
					  		"states = " + str(len(states[label1])) + ";\n\n"
			)
			for line in template:
				f.write(line)
			f.write("\nManipulate[Plot3D[function[x, y, v, w],{x,-n,n},{y,-n,n}, PlotRange -> All],{v,-n,n},{w,-n,n}]\n")
			f.write("\nClear[x,y,v,w]; n = Pi;\nManipulate[ContourPlot[function[x, y, v, w], {x, -n, n}, {y, -n, n}, PlotLegends -> Automatic, Contours -> 30],{v,-n,n},{w,-n,n}]\n")


with open('result.txt', 'r') as f:
    x = f.readlines()

remove("result.txt")
results = []
for line in x:
	line = line.replace("\"","").strip()
	lastSpace = line.rfind(" ")
	results.append([line[:lastSpace], line[lastSpace+1:]])

with open('result.txt', 'w') as f:
	f.write(tabulate(results, headers=['Name', 'Max Probability']))


system('make')
system('make cleanaux')
remove('amplitudes.txt') 
