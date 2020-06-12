from os import system, remove

states = []
for i in range(4,13):
	a = ''
	for j in range(i-1):
		a += '1 '
	a += '1'
	states.append(str(i)+"v"+ a)

with open('../../result.txt','r') as f:
	x = f.readlines()

data = {}
for line in x:
	lastSpace = line.rfind(" ")
	line = [line[:lastSpace].strip(),line[lastSpace+1:].strip()]
	if line[0] in states:
		data[line[0][:line[0].find("v")]] = line[1]

with open('striedave.txt','w') as f:
	for x, y in data.items():
		f.write(str(x) + "\t" + str(y) + "\n")

with open("graf1.gnuplot", "w") as graf: 
		graf.write	( "set terminal pngcairo size 350,262 enhanced font \'Verdana,10\'\n" +
					  "set output \"x-y.png\"\n" +
					  "set grid\n" +
					  "set xlabel \"x\" \n" +
					  "set ylabel \"y\"\n" +
					  "plot \"striedave.txt\" with points pt 2"
					)

with open("graf2.gnuplot", "w") as graf: 
		graf.write	( "set terminal pngcairo size 350,262 enhanced font \'Verdana,10\'\n" +
					  "set output \"x-logy.png\"\n" +
					  "set grid\n" +
					  "set logscale y\n" +
					  "f(x) = (10**(a*x + b))\n" +
					  "fit f(x) \"striedave.txt\" via a,b\n" +
					  "set xlabel \"x\" \n" +
					  "set ylabel \"logy\"\n" +
					  "plot \"striedave.txt\" with points pt 2, f(x) w l"
					)

with open("graf3.gnuplot", "w") as graf: 
		graf.write	( "set terminal pngcairo size 350,262 enhanced font \'Verdana,10\'\n" +
					  "set logscale xy\n" +
					  "set output \"logx-logy.png\"\n" +
					  "set grid\n" +
					  "set xlabel \"logx\" \n" +
					  "set ylabel \"logy\"\n" +
					  "plot \"striedave.txt\" with points pt 2"
					)

system('gnuplot graf3.gnuplot')
system('gnuplot graf2.gnuplot')
system('gnuplot graf1.gnuplot')

for i in range(1,4):
	remove('graf'+str(i)+".gnuplot")