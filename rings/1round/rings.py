import subprocess
from os import system, remove,  chdir
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
	for l in labels:

		constants = {} #cut to (number of sinuses to how many times repeated) - all we need to construct the amplitude
		#it's enough to compute the amplitude for representant of the group
		representant = states[l][0]

		#here we fill the constants directory - gain all informations needed for amplitude creation
		for group in labels:

			if cuts[group] not in constants.keys():
				constants[ cuts[group] ] = {}

			for state in states[group]:
				numOfSinuses = compare(representant, state)

				if numOfSinuses in constants[ cuts[group] ].keys():
					constants[ cuts[group] ][ numOfSinuses ] += 1
				else:
					constants[ cuts[group] ][ numOfSinuses ] = 1
		
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
	return amplitudes


start = 3
end = 16


with open('result.txt', 'w') as f:#to delete any content
    pass
with open('amplitudes.txt', 'w') as f:#to create the file
    pass


for numberOfQubits in range(start, end+1):
	states = groupsOfStates(numberOfQubits)

	for l, amplitude in amplitudes(numberOfQubits, states).items():
		print(l)


		#here we are creating result mathematica file so that we could run it
		with open(str(numberOfQubits) + "v" + str(l) + ".nb", "w") as file, open("templates/results.nb", "r") as template:

			file.write	(	"$Conjugate[x_] := x /. Complex[a_, b_] :> a - I b;\n" +
					  		"function[x_, y_] := $Conjugate[" + amplitude + "]*\n(" + amplitude + ")\n\n" +
					  		"amplitude[x_,y_] := " + amplitude + "\n" + 
					  		"amount = " + str(numberOfQubits) + ";\n" + 
					  		"name = \"" + str(numberOfQubits) + "v" + l + "\";\n" +
					  		"states = " + str(len(states[l])) + ";\n\n"
						)

			for line in template:
				file.write(line)

			file.write("\nExport[\"images/plots/" + str(numberOfQubits) + "v" + l + ".jpg\", Plot3D[f, {c, 0, n/2},{d, 0, n}, PlotRange -> All]];\n")
			file.write("\nExport[\"images/contour-plots/" + str(numberOfQubits) + "v" + l + " c.jpg\", ContourPlot[function[x, y]/2^amount, {x, 0, n/2}, {y, 0, n/2}, PlotLegends -> Automatic, Contours -> 30, FrameLabel -> {\\[Beta],\\[Gamma]}, FrameTicks ->{Range[0, Pi/2, Pi/8],Range[0, Pi/2, Pi/8]}]];\n")

		#here we run the mathematica file and then we remove it
		while True:
			try:
				cpi = subprocess.run(
					["math", "-script", str(numberOfQubits) + "v" + l + ".nb"],
					stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
					check=True
				)
				if "ok" in cpi.stdout.decode().split('\n'):
					break
				else:
					print("retrying")
			except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
				print(e)
				print("retrying") 

		remove(str(numberOfQubits) + "v" + l + ".nb")


		#here we are creating amplitudes.pdf
		if numberOfQubits < 7:

			with open("templates/amplitudes.tex", "r") as template, open("amplitudes/amplitudes.tex", "w") as file, open("amplitudes.txt", "r") as ampl:

				for line in template:
					file.write(line)

				x = ampl.readlines()

				for line in x:
					line = line.replace("\"","").replace("\\\\","\\").replace("\\\n", "")
					file.write(line) 
				file.write("\\end{document}")

		#here we are creating useful mathematica file - sth to play later with
		with open("mathematica-files/" + str(numberOfQubits) + "v" + l + ".nb", "w") as f, open("templates/useful.nb", "r") as template:

			f.write	(	"$Conjugate[x_] := x /. Complex[a_, b_] :> a - I b;\n" +
					  		"function[x_, y_] := $Conjugate[" + amplitude + "]*\n(" + amplitude + ")\n\n" +
					  		"amplitude[x_,y_] := " + amplitude + "\n\n" + 
					  		"amount = " + str(numberOfQubits) + ";\n" + 
					  		"name = \"" + str(numberOfQubits) + "v" + l + "\";\n" +
					  		"states = " + str(len(states[l])) + ";\n\n"
			)

			for line in template:
				f.write(line)

			f.write("\nPlot3D[f,{c,0,n},{d,0,n}, PlotRange -> All]\n")
			f.write("\nContourPlot[function[x, y], {x, 0, n}, {y, 0, n}, PlotLegends -> Automatic, Contours -> 30]\n")

#here we are creating result.txt: type - Pmax table
with open('result.txt', 'r') as f:
    x = f.readlines()

remove("result.txt")
results = []
for line in x:
	line = line.replace("\"","").strip()
	g = line.rfind(" ")
	b = line[:g].rfind(" ")
	p = line[:b].rfind(" ")
	results.append([line[:p], line[p+1:b], line[b+1:g], line[g+1:]])

with open('result.txt', 'w') as f:
	f.write(tabulate(results, headers=['Name', 'Max Probability', "beta (X)", "gamma (ZZ)"]))


#just to really have the amplitudes.pdf file
chdir('./amplitudes')
system('make')
system('make cleanaux')
remove('../amplitudes.txt')