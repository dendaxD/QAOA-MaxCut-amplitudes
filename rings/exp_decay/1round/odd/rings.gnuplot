set terminal pngcairo size 350,262 enhanced font 'Verdana,10'
set output 'odd-rings.svg'
set grid
set key width -5
set xlabel 'number of qubits (n)' 
set ylabel 'probability of reaching 0101...01'
set xrange[3:19]
set yrange[0:0.5]
plot "upper bound" pt 7 ps 0.75 title 'upper bound', "maximizing p₀₀...₀"  pt 7 ps 0.75 lc rgb "red" title 'maximizing p₀₀...₀', "minimizing average energy"  pt 6 ps 0.75 lc rgb '#1c1044' title 'minimizing average energy'