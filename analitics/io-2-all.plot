set title "Scheduler IO eMBB (bytes)"
set terminal pngcairo
set output "io-2-all.png"
set xrange [0:10000]

plot "eMBB-io.dat" using 1:2 title "IN" with lines linetype 1, "eMBB-io.dat" using 1:3 title "OUT" with lines linetype 2 lw 2
