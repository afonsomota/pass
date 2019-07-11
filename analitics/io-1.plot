set title "Scheduler IO uRLLC (bytes)"
set terminal pngcairo
set output "io-1.png"
set xrange [1900:2100]

plot "uRLLC-io.dat" using 1:2 title "IN" with lines linetype 3, "uRLLC-io.dat"  using 1:3 title "OUT" with lines linetype 4 lw 2
