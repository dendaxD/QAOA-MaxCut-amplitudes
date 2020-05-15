from os import system, remove



with open("graf.gnuplot", "w") as graf: 
		graf.write	( "set terminal pngcairo size 350,262 enhanced font \'Verdana,10\'\n" +
					  "set output \"cg.png\"\n" +
					  # "f(x) = (10**(a*x + b))\n" +
					  # "fit f(x) \"striedave-parne.txt\" via a,b\n" +
					  "set grid\n" +
					  # "set key outside\n" +
					  "set title \"Complete graphs 2rounds\"\n" +
					  # "set xlabel \"n\" \n" +
					  # "set ylabel \"logp\"\n" +
					  "set key left bottom\n" +
					  "set key font \",7\"\n" +
					  "set key spacing 0.7\n" +
					  "set key box\n" +
					  "plot \"maxd\", \"0d\", \"1d\", \"2d\", \"3d\""
					)

system('gnuplot graf.gnuplot')
remove('graf.gnuplot')