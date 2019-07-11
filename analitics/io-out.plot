set title "Scheduler Output (bytes)"
set terminal pngcairo
set output "io-out.png"
set xrange [1900:2100]

plot  "uRLLC-io.dat" using 1:3 with lines linetype rgb "black" lw 2 , \
     "eMBB-io.dat" using 1:3 with lines linetype 2 , \
     "mMTC-io.dat" using 1:3 with lines linetype 6  
