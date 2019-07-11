set title "Scheduler IO (bytes)"
set terminal pngcairo
set output "io-all.png"
set xrange [0:10000]

plot "uRLLC-io.dat" using 1:2 with lines linetype 1, "uRLLC-io.dat" using 1:3 with lines linetype 1 lw 2, \
     "eMBB-io.dat" using 1:2 with lines linetype 2, "eMBB-io.dat" using 1:3 with lines linetype 2 lw 2, \
     "mMTC-io.dat" using 1:2 with lines linetype 3, "mMTC-io.dat" using 1:3 with lines linetype 3 lw 2 
