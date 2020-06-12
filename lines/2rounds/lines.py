import subprocess
from os import system, remove
from tabulate import tabulate

def edges(n):
	location = 0
	edges = []
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
	numberOfValues = 0 #0 because in iteration we start with state[0]
	for i in range(len(state)):
		if state[i] == value:
			numberOfValues += 1
		else:
			value = state[i]
			label.append(str(numberOfValues))
			numberOfValues = 1
	label.append(str(numberOfValues))
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
		k1 = " ".join(k)
		k.reverse()
		k2 = " ".join(k)
		c = cut(s,e)
		if k1 in states.keys():
			states[k1].append([s,c,""])
			states[k1].append([mynot,c,""])
		elif k2 in states.keys():
			states[k2].append([s,c,""])
			states[k2].append([mynot,c,""])
		else:
			states[k1] = []
			states[k1].append([s,c,""])
			states[k1].append([mynot,c,""])
	return states

def compare(string1, string2):
	diff = 0
	for c1, c2 in zip(string1, string2):
		if c1 != c2:
			diff += 1
	return diff

def listCutsAmplitudes(states):
	labels = states.keys()
	cuts_amplitudes = []
	for group in labels:
			cut_amplitude = [str(states[group][0][1]),states[group][0][2]]
			if cut_amplitude not in cuts_amplitudes:
				cuts_amplitudes.append(cut_amplitude)
	return cuts_amplitudes


def amplitudes(states, round = ""): #=ROUND
	amplitudes = {}
	labels = states.keys()
	cuts_amplitudes = listCutsAmplitudes(states)
	n = len(states[list(states)[0]][0][0])
	for label1 in labels:
		temp = {} 
		state = states[label1][0][0]
		for group in labels:
			cut = str(states[group][0][1])
			ampl = states[group][0][2]
			for i in range(len(states[group])):
				numOfSin = compare(state,states[group][i][0])
				if numOfSin in temp.keys():
					temp[numOfSin].append([cut,ampl])
				else:
					temp[numOfSin] = []
					temp[numOfSin].append([cut,ampl])
		amplitude = ""
		constantsForAmplitude = {}
		for c_a in cuts_amplitudes:
			constantsForAmplitude[c_a[0] + "&" + c_a[1]] = {}
			for numOfSin in temp.keys():
				constantsForAmplitude[c_a[0] + "&" + c_a[1]][numOfSin] = 0
		for c_a in cuts_amplitudes:
			for numOfSin in temp.keys():
				constantsForAmplitude[c_a[0] + "&" + c_a[1]][numOfSin] += temp[numOfSin].count([c_a[0],c_a[1]])
			amplitude += "Exp[" + c_a[0] + " I y"+round+"] " + c_a[1]+"(" if amplitude == "" else " + Exp[" + c_a[0] + " I y"+round+"] " + c_a[1]+"("
			for nOS in constantsForAmplitude[c_a[0] + "&" + c_a[1]].keys():
				if constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS] != 0:
					if constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS] != 1:
						if nOS == n:
							amplitude += (str(constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS]) + " (I Sin[x"+round+"])^" + str(n)) if amplitude[-1:] == "(" else (" + " + str(constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS]) + " (I Sin[x"+round+"])^" + str(n))							
						elif nOS == 0:
							amplitude += (str(constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS]) + " Cos[x"+round+"]^" + str(n)) if amplitude[-1:] == "(" else (" + " + str(constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS]) + " Cos[x"+round+"]^" + str(n))							
						else:
							amplitude += (str(constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS]) + " (I Sin[x"+round+"])^" + str(nOS) + " Cos[x"+round+"]^" + str(n-nOS)) if amplitude[-1:] == "(" else (" + " + str(constantsForAmplitude[c_a[0] + "&" + c_a[1]][nOS]) + " (I Sin[x"+round+"])^" + str(nOS) + " Cos[x"+round+"]^" + str(n-nOS))
					else:
						if nOS == n:	
							amplitude += ("(I Sin[x"+round+"])^" + str(n)) if amplitude[-1:] == "(" else (" + (I Sin[x"+round+"])^" + str(n))
						elif nOS == 0:	
							amplitude += ("Cos[x"+round+"]^" + str(n)) if amplitude[-1:] == "(" else (" + Cos[x"+round+"]^" + str(n))						
						else:
							amplitude += ("(I Sin[x"+round+"])^" + str(nOS) + " Cos[x"+round+"]^" + str(n-nOS)) if amplitude[-1:] == "(" else (" + (I Sin[x"+round+"])^" + str(nOS) + " Cos[x"+round+"]^" + str(n-nOS))						
			amplitude += ")"
		amplitudes[label1] = amplitude
	for label1 in labels:
		for state in states[label1]:
			state[2] = "(" + amplitudes[label1] + ") "
	return amplitudes, states




start = 2
end = 10
with open('result.txt', 'w') as f:#to delete any content
    pass
with open('amplitudes.txt', 'w') as f:#to create the file
    pass
for numberOfQubits in range(start,end+1):
	states = groupsOfStates(numberOfQubits)
	ampls = amplitudes(amplitudes(states)[1])[0]
	for label1, amplitude in ampls.items():
		with open(str(numberOfQubits) + "v" + label1 + ".nb", "w") as file, open("templates/results-template.nb", "r") as template:
			file.write	(	"$Conjugate[x_] := x /. Complex[a_, b_] :> a - I b;\n" +
					  		"function[x_, y_] := $Conjugate[" + amplitude + "]*(" + amplitude + ")\n" +
					  		"ammount = " + str(numberOfQubits) + ";\n" + 
					  		"name = \"" + str(numberOfQubits) + "v" + label1 + "\";\n" +
					  		"states = " + str(len(states[label1])) + ";\n\n"
			)
			for line in template:
				file.write(line)
			file.write("\nExport[\"images/" + str(numberOfQubits) + "v" + label1 + ".jpg\", Plot3D[f,{c,-n,n},{d,-n,n}, PlotRange -> All]];\n")
			file.write("\nExport[\"images/" + str(numberOfQubits) + "v" + label1 + " c.jpg\", ContourPlot[function[x, y], {x, -n, n}, {y, -n, n}, PlotLegends -> Automatic, Contours -> 30]];\n")
		if numberOfQubits < 7:
			with open("templates/amplitudes-probabilities.tex", "r") as probtemplate, open("amplitudes-probabilities.tex", "w") as prob, open("amplitudes.txt", "r") as am:
				for line in probtemplate:
					prob.write(line)
				x = am.readlines()
				for line in x:
					line = line.replace("\"","").replace("\\\\","\\").replace("\\\n", "")
					 prob.write(line) 
				prob.write("\\end{document}")
		subprocess.run(["math", "-script", str(numberOfQubits) + "v" + label1 + ".nb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		remove(str(numberOfQubits) + "v" + label1 + ".nb")
		with open("MathematicaFiles/" + str(numberOfQubits) + "v" + label1 + ".nb", "w") as f, open("templates/useful-template.nb", "r") as template:
			f.write	(	"$Conjugate[x_] := x /. Complex[a_, b_] :> a - I b;\n" +
					  		"function[x_, y_] := $Conjugate[" + amplitude + "]*(" + amplitude + ")\n" +
					  		"ammount = " + str(numberOfQubits) + ";\n" + 
					  		"name = \"" + str(numberOfQubits) + "v" + label1 + "\";\n" +
					  		"states = " + str(len(states[label1])) + ";\n\n"
			)
			for line in template:
				f.write(line)
			f.write("\nPlot3D[f,{c,-n,n},{d,-n,n}, PlotRange -> All]\n")
			f.write("\nContourPlot[function[x, y], {x, -n, n}, {y, -n, n}, PlotLegends -> Automatic, Contours -> 30]\n")

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