set terminal pngcairo size 500,320 enhanced font 'Verdana,10'
set output 'parne-kruhy-logscale.png'
set grid
set key box width -2
set key font ",8"
set logscale y 2
set xrange [3:19]
set xlabel 'number of qubits (n)' 
set ylabel 'probability of reaching 01...01'
plot "upper bound" pt 7 ps 1 title 'upper bound', "maximizing p₀₀...₀"  pt 7 ps 1 lc rgb "red" title 'maximizing p₀₀...₀', "minimizing average energy"  pt 6 ps 1 lc rgb '#1c1044' title 'minimizing average energy'