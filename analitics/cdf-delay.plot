set title "CDF for delay"
set terminal pngcairo
set output "cdf-delay.png"

set key outside below height 2 center horizontal
set xlabel "Delay (ms)"
set yrange [0:1]

plot "cdf-delays-0.dat" using 1:(1./$2) smooth cumulative title "uRLLC" with lines lt rgb "#9BBB59", \
     "cdf-delays-1.dat" using 1:(1./$2) smooth cumulative title "eMBB" with lines lt rgb "#C0504D", \
     "cdf-delays-2.dat" using 1:(1./$2) smooth cumulative title "mMTC" with lines lt rgb "#F79646"
     
