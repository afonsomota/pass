set title "CDF for delay"
set terminal pngcairo
set output "cdf-tp.png"

set key outside below height 2 center horizontal
set xlabel "Throughput (kbyte/s)"
set yrange [0:1]

plot "cdf-tps-0.dat" using 1:(1./$2) smooth cumulative title "uRLLC" with lines linetype rgb "#9BBB59", \
     "cdf-tps-1.dat" using 1:(1./$2) smooth cumulative title "eMBB" with lines  linetype rgb "#C0504D", \
     "cdf-tps-2.dat" using 1:(1./$2) smooth cumulative title "mMTC" with lines  linetype rgb "#F79646"
     
