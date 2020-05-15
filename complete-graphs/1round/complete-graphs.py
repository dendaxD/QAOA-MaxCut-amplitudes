import subprocess
from os import system, remove, chdir
from tabulate import tabulate
import time

# the set of edges in a complete graph given by the number of the vertices
def edges(n):
	edges = []
	for i in range(n-1):
		for j in range(i+1,n):
			edges.append([i,j])
	return edges

def hamming_distance(string1, string2):
	diff = 0
	for c1, c2 in zip(string1, string2):
		if c1 != c2:
			diff += 1
	return diff

def cut(l, n):
	l = int(l)
	return n*(n-1)/2 - 2*l*(n-l)

# LABEL is used to unambiguously identify a group
# GROUP is a set within the elements give the same results
def label(state):
	label = state.count("1")
	return str(label) if (label <= len(state)/2) else str(len(state) - label)


# group the states into sets with the same label
def createLabelToStatesDict(n):
	labelToStatesDict = {}

	#iterate through all the states
	#(actually, only those that start with 0, the rest is included by "mynot")
	for i in range(2**(n-1)):
		#transform i into a string of its binary representation (e.g. i=4 with n=5 gives "00100")
		s = str(bin(i))[2:]
		s = (n-len(s))*"0" + s

		mynot = ''
		for znak in s:
			mynot += '0' if znak == '1' else '1'

		l = label(s)
		c = cut(l, n)

		if l in labelToStatesDict.keys():
			labelToStatesDict[l].append(s)
			labelToStatesDict[l].append(mynot)
		else:
			labelToStatesDict[l] = []
			labelToStatesDict[l].append(s)
			labelToStatesDict[l].append(mynot)
	return labelToStatesDict

def createLabelToAmplitudeDict(n, labelToStatesDict):

	labelToAmplitudeDict = {}
	labels = labelToStatesDict.keys()

	labelToCutDict = {}
	for l in labels:
		labelToCutDict[l] = cut(l, n)

	for l in labels:
		amplitude_info = {} #cut to {numberOfSinuses to coefficients}
		representant = labelToStatesDict[l][0] #it's enough to compute the amplitude for the representant of the group

		for group in labels:
			if labelToCutDict[group] not in amplitude_info.keys():
				amplitude_info[ labelToCutDict[group] ] = {}

			for state in labelToStatesDict[group]:
				numberOfSinuses = hamming_distance(representant, state)

				if numberOfSinuses in amplitude_info[ labelToCutDict[group] ].keys():
					amplitude_info[ labelToCutDict[group] ][ numberOfSinuses ] += 1
				else:
					amplitude_info[ labelToCutDict[group] ][ numberOfSinuses ] = 1
		
		amplitude = ""
		for c in amplitude_info.keys(): #c for cut
			amplitude += f"Exp[{-c} I y] ("
			for numberOfSinuses, coefficient in amplitude_info[c].items():
				if numberOfSinuses == n:
					amplitude += f"{coefficient} (I Sin[x])^{n}"
				elif numberOfSinuses == 0:
					amplitude += f"{coefficient} Cos[x]^{n}"
				else:
					amplitude += f"{coefficient} (I Sin[x])^{numberOfSinuses} Cos[x]^{n - numberOfSinuses}"
				amplitude += " + "
			amplitude = amplitude[:-3] + ") + "
		labelToAmplitudeDict[l] = amplitude[:-3] #[:-3] to remove additional ' + '
	return labelToAmplitudeDict


def main():
	start = 6
	end = 6


	with open('result.txt', 'w') as f:#to delete any content
	    pass
	with open('amplitudes.txt', 'w') as f:#to create the file
	    pass


	for numberOfQubits in range(start, end+1):
		labelToStatesDict = createLabelToStatesDict(numberOfQubits)

		for l, amplitude in createLabelToAmplitudeDict(numberOfQubits, labelToStatesDict).items():
			print(numberOfQubits, "v", l)


			#here we are creating mathematica file (for information gain) so that we could subsequently run it
			with open(str(numberOfQubits) + "v" + str(l) + ".nb", "w") as file, open("templates/results.nb", "r") as template:
		  							  		
				file.write	(	"nqubits = " + str(numberOfQubits) + ";\n" + 
						  		"name = \"" + str(numberOfQubits) + "v" + l + "\";\n" +
						  		"nstates = " + str(len(labelToStatesDict[l])) + ";\n"

								"amplitude[x_, y_] := (" + amplitude + ")/Sqrt[2^nqubits];\n" +
								"amplitude2[x_, y_] := (" + amplitude + ");\n" + 
						  		"probability[x_, y_] := Abs[amplitude[x, y]]^2;\n\n"
							)

				for line in template:
					file.write(line)

				file.write("\nExport[\"images/plots/" + str(numberOfQubits) + "v" + l + ".jpg\", Plot3D[f, {c, 0, n/2},{d, 0, n}, PlotRange -> All]];\n")
				file.write("Export[\"images/contour-plots/" + str(numberOfQubits) + "v" + l + " c.jpg\", ContourPlot[probability[x, y], {x, -n, n}, {y, -n, n}, PlotLegends -> Automatic, Contours -> 30, PlotPoints -> 300, FrameLabel -> {\[Beta],\[Gamma]}, FrameTicks ->{Range[-Pi, Pi, Pi/2],Range[-Pi, Pi, Pi/2]}]];\n")

			#Here we run the mathematica file. Then we remove it.
			t_init = time.perf_counter()
			subprocess.run(["math", "-script", str(numberOfQubits) + "v" + l + ".nb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			print(time.perf_counter() - t_init)
			remove(str(numberOfQubits) + "v" + l + ".nb")

			#here we are creating useful mathematica file - sth to play with later
			with open("mathematica-files/" + str(numberOfQubits) + "v" + l + ".nb", "w") as file, open("templates/useful.nb", "r") as template:

				file.write	(	"nqubits = " + str(numberOfQubits) + ";\n" + 
						  	"name = \"" + str(numberOfQubits) + "v" + l + "\";\n" +
						  	"nstates = " + str(len(labelToStatesDict[l])) + ";\n\n"

							"amplitude[x_,y_] := (" + amplitude + ")/Sqrt[2^nqubits];\n" +
							"amplitude2[x_,y_] := (" + amplitude + ");\n" + 
						  	"probability[x_, y_] := Abs[amplitude[x, y]]^2;\n\n"
				)

				for line in template:
					file.write(line)

				file.write("\nPlot3D[f, {c, 0, n/2}, {d, -n, n}, PlotRange -> All]\n")
				file.write("ContourPlot[probability[x, y], {x, 0, n/2}, {y, 0, n}, PlotLegends -> Automatic, Contours -> 30]\n")


	#here we are creating the result.txt file: [type <-> Pmax <-> beta <-> gamma] table
	with open('result.txt', 'r') as file:
	    x = file.readlines()

	results = []
	for line in x:
		line = line.replace("\"","").split()
		results.append(line)

	with open('result.txt', 'w') as f:
		f.write(tabulate(results, headers=['Name', 'Max Probability', "beta (X)", "gamma (ZZ)"]))


	#create the amplitudes.pdf file
	with open("templates/amplitudes.tex", "r") as template, open("amplitudes/amplitudes.tex", "w") as file, open("amplitudes.txt", "r") as data:

		for line in template:
			file.write(line)

		for line in data:
			line = line.replace("\"","").replace("\\\\","\\").replace("\\\n", "")
			file.write(line) 
		file.write("\\end{document}")



	chdir('./amplitudes')
	system('make')
	system('make cleanaux')
	chdir('../')
	remove('amplitudes.txt')


if __name__ == "__main__":
	main()