set title "Scheduler IO eMBB (bytes)"
set terminal pngcairo
set output "io-2.png"
set xrange [1900:2100]

plot "eMBB-io.dat" using 1:2 title "IN" with lines linetype 1, "eMBB-io.dat" using 1:3 title "OUT" with lines linetype 2 lw 2
