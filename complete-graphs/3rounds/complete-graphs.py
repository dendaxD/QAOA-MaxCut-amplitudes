import subprocess
from os import system, remove
from tabulate import tabulate


def edges(n):
	edges = []
	for i in range(n-1):
		for j in range(i+1,n):
			edges.append([i, j])
	return edges


def cut(l, n):
	l = int(l)
	return n*(n-1)/2 - 2*l*(n-l)


# label is used to unambiguously identify a group (set within the elements give the same results)
def label(state):
	label = state.count("1")
	return str(label) if (label <= len(state)/2) else str(len(state) - label)


#Here we group states into sets with the same label
def groupsOfStates(n):
	states = {}
	for i in range(2**(n-1)): #n-1 because we automaticaly add also NOT the generated state
		s = str(bin(i))[2:]
		s = (n-len(s))*"0" + s
		mynot = ''
		for znak in s:
			mynot += '0' if znak == '1' else '1'
		k = label(s)
		c = cut(k, n)
		if k in states.keys():
			states[k].append(s)
			states[k].append(mynot)
		else:
			states[k] = []
			states[k].append(s)
			states[k].append(mynot)
	return states


def compare(string1, string2):
	diff = 0
	for c1, c2 in zip(string1, string2):
		if c1 != c2:
			diff += 1
	return diff


#THE MOST IMPORTANT
def amplitudes(n, states):

	amplitudes = {} #label <-> amplitude
	cuts = {} #label <-> cut
	labels = states.keys()
	for l in labels:
		cuts[l] = cut(l, n)

	#MAIN FOR LOOP
	computation_constants = {} #{label -> {constants}}
	for l in labels:

		#constants - all information we need to create the amplitude
		constants = {} #cut to (exponents to coefficients)
		constants2 = {} #different group can have different cuts, therefore 

		representant = states[l][0]

		#find the constants
		for group in labels:
			constants2[group] = {}

			if cuts[group] not in constants.keys():
				constants[ cuts[group] ] = {}

			if cuts[group] not in constants2[group].keys():
				constants2[group][ cuts[group] ] = {}

			for state in states[group]:
				exponent = compare(representant, state)

				if exponent in constants[ cuts[group] ].keys():
					constants[ cuts[group] ][ exponent ] += 1
				else:
					constants[ cuts[group] ][ exponent ] = 1

				if exponent in constants2[group][ cuts[group] ].keys():
					constants2[group][ cuts[group] ][ exponent ] += 1
				else:
					constants2[group][ cuts[group] ][ exponent ] = 1
		
		#first round
		amplitude = ""
		for c in constants.keys():
			amplitude += f"Exp[{-c} I y1] ("
			for exponent, coefficient in constants[c].items():
				if exponent == n:
					amplitude += f"{coefficient} (-I Sin[x1])^{n}"
				elif exponent == 0:
					amplitude += f"{coefficient} Cos[x1]^{n}"
				else:
					amplitude += f"{coefficient} (-I Sin[x1])^{exponent} Cos[x1]^{n - exponent}"
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
				amplitude += f"Exp[{-c} I y2]*({amplitudes[l2]})*("
				for exponent, coefficient in computation_constants[l][l2][c].items():
					if exponent == n:
						amplitude += f"{coefficient} (-I Sin[x2])^{n}"
					elif exponent == 0:
						amplitude += f"{coefficient} Cos[x2]^{n}"
					else:
						amplitude += f"{coefficient} (-I Sin[x2])^{exponent} Cos[x2]^{n - exponent}"
					amplitude += " + "
				amplitude = amplitude[:-3] + ") + "
		amplitudes2[l] = amplitude[:-3] #[:-3] to remove additional ' + '

	#third round
	amplitudes = {}
	for l in labels:
		
		amplitude = ""
		for l2 in labels:
			for c in computation_constants[l][l2].keys():
				amplitude += f"Exp[{-c} I y3]*({amplitudes2[l2]})*("
				for exponent, coefficient in computation_constants[l][l2][c].items():
					if exponent == n:
						amplitude += f"{coefficient} (-I Sin[x3])^{n}"
					elif exponent == 0:
						amplitude += f"{coefficient} Cos[x3]^{n}"
					else:
						amplitude += f"{coefficient} (-I Sin[x3])^{exponent} Cos[x3]^{n - exponent}"
					amplitude += " + "
				amplitude = amplitude[:-3] + ") + "
		amplitudes[l] = amplitude[:-3] #[:-3] to remove additional ' + '	
	return amplitudes


def main():
	start = 3
	end = 18
	
	
	with open('result.txt', 'w') as f:#to delete any content
	    pass
	
	
	for numberOfQubits in range(start,end+1):
		states = groupsOfStates(numberOfQubits)
	
		for l, amplitude in amplitudes(numberOfQubits, states).items():
	
			#here we are creating mathematica file (for information gain) so that we could subsequently run it		
			with open(str(numberOfQubits) + "v" + l + ".nb", "w") as file, open("templates/results.nb", "r") as template:
	
				file.write	(	"nqubits = " + str(numberOfQubits) + ";\n" + 
						  		"name = \"" + str(numberOfQubits) + "v" + l + "\";\n" +
						  		"nstates = " + str(len(states[l])) + ";\n\n" +
						  		"amplitude[x1_,y1_,x2_,y2_,x3_,y3_] := (" + amplitude + ")/Sqrt[2^nqubits];\n" +
						  		"probability[x1_,y1_,x2_,y2_,x3_,y3_] := Abs[amplitude[x1,y1,x2,y2,x3,y3]]^2;\n\n"
				)
	
				for line in template:
					file.write(line)
	
			#Here we run the mathematica file. Then we remove it.
			subprocess.run(["math", "-script", str(numberOfQubits) + "v" + l + ".nb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			remove(str(numberOfQubits) + "v" + l + ".nb")
			
			#here we are creating useful mathematica file - sth to play with later		
			with open("mathematica-files/" + str(numberOfQubits) + "v" + l + ".nb", "w") as f, open("templates/useful.nb", "r") as template:
	
				f.write	(	"nqubits = " + str(numberOfQubits) + ";\n" + 
						  	"name = \"" + str(numberOfQubits) + "v" + l + "\";\n" +
						  	"nstates = " + str(len(states[l])) + ";\n\n" +

						  	"amplitude[x1_,y1_,x2_,y2_,x3_,y3_] := (" + amplitude + ")/Sqrt[2^nqubits];\n" +
						  	"probability[x1_,y1_,x2_,y2_,x3_,y3_] := Abs[amplitude[x1,y1,x2,y2,x3,y3]]^2;\n\n"
				)
				for line in template:
					f.write(line)
	
	#here we are creating result.txt: [type <-> Pmax] table
	with open('result.txt', 'r') as f:
	    x = f.readlines()
	
	remove("result.txt")
	results = []
	for line in x:
		line = line.replace("\"","").split()
		results.append(line)
	
	with open('result.txt', 'w') as f:
		f.write(tabulate(results, headers=['Name', 'Max Probability']))

if __name__ == "__main__":
	main()