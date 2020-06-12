set terminal pngcairo size 350,262 enhanced font 'Verdana,10'
set output 'even-cg.png'
set grid
set key off
set xlabel 'number of qubits (n)' 
set ylabel 'p₀₀...₀(π/8,π/4) + p₁₁...₁(π/8,π/4)'
set xrange[3:21]
set yrange[0.4:1]
plot "zeroes-parne.txt" pt 7 ps 0.5 lc rgb 'red'