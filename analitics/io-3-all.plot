set title "Scheduler IO mMTC (bytes)"
set terminal pngcairo
set output "io-3-all.png"
set xrange [0:10000]

plot "mMTC-io.dat" using 1:2 title "IN" with lines linetype 5, "mMTC-io.dat" using 1:3 title "OUT" with lines linetype 6 lw 2
