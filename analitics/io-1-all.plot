set title "Scheduler IO uRLLC (bytes)"
set terminal pngcairo
set output "io-1-all.png"
set xrange [0:10000]

plot "uRLLC-io.dat" using 1:2 title "IN" with lines linetype 3, "uRLLC-io.dat"  using 1:3 title "OUT" with lines linetype 4 lw 2
