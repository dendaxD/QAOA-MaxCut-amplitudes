from os import system, remove



with open("graf.gnuplot", "w") as graf: 
		graf.write	( "set terminal pngcairo size 350,262 enhanced font \'Verdana,10\'\n" +
					  "set output \"cg-parne.png\"\n" +
					  # "f(x) = (10**(a*x + b))\n" +
					  # "fit f(x) \"striedave-parne.txt\" via a,b\n" +
					  "set grid\n" +
					  # "set key outside\n" +
					  "set title \"Complete graphs- parne\"\n" +
					  "set logscale y 2\n" +
					  "set xlabel \"n\" \n" +
					  "set ylabel \"logp\"\n" +
					  "set key bottom left\n" +
					  "set key font \",8\"\n" +
					  "set key spacing 1\n" +
					  "set key box\n" +
					  "plot \"maxd0\", \"0d0\", \"1d0\", \"2d0\""
					)

system('gnuplot graf.gnuplot')
remove('graf.gnuplot')