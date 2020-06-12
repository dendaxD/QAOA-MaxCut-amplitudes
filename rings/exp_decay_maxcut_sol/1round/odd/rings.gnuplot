set terminal pngcairo size 350,262 enhanced font 'Verdana,10'
set output 'graphs/odd-rings.svg'
set grid
set key width -5
set xlabel 'number of qubits (n)' 
set ylabel 'probability of reaching 0101...01'
set xrange[3:19]
set yrange[0:0.5]
plot "data/upper bound" pt 7 ps 0.75 title 'upper bound', "data/maximizing p₀₁...₀₁₀"  pt 7 ps 0.75 lc rgb "red" title 'maximizing p₀₁...₀₁₀', "data/minimizing average energy"  pt 6 ps 0.75 lc rgb '#1c1044' title 'minimizing average energy'