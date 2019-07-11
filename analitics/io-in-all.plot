set title "Scheduler INPUT (bytes)"
set terminal pngcairo
set output "io-in-all.png"
set xrange [0:10000]

plot  "uRLLC-io.dat" using 1:2 with lines linetype rgb "black" lw 2 , \
     "eMBB-io.dat" using 1:2 with lines linetype 1 , \
     "mMTC-io.dat" using 1:2 with lines linetype 5  
