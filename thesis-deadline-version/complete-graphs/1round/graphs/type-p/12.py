from os import system, remove

states = []
n=15
for i in range(n//2 + 1):
	states.append(str(n)+"v"+str(i))

with open('../../result.txt','r') as f:
	x = f.readlines()

data = {}
for line in x:
	line = line.strip().split()
	if line[0] in states:
		data[line[0][line[0].find("v")+1:]] = line[1]

with open(str(n),'w') as f:
	for x, y in data.items():
		f.write(str(x) + "\t" + str(y) + "\n")

with open("graf1.gnuplot", "w") as graf: 
		graf.write	( "set terminal pngcairo size 350,262 enhanced font \'Verdana,10\'\n" +
					  "set output \""+str(n)+".png\"\n" +
					  "set title \"n = "+str(n)+" - all\"\n" +
					  "set grid\n" +
					  "set xlabel \"type\" \n" +
					  "set ylabel \"p\"\n" +
					  "set key off\n" +
					  "plot \""+str(n)+"\" with points pt 2"
					)


system('gnuplot graf1.gnuplot')
remove('graf1.gnuplot')