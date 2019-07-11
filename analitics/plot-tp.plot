set title "Average packet throughput"
set terminal pngcairo
set output "tp.png"

set yrange [0:500]

set key outside below height 2 center horizontal
set xlabel "Simulation time (s)"
set ylabel "Throughput (kbyte/s)"

plot "uRLLC.dat" using 1:4 with lines linetype rgb "#9BBB59" title "uRLLC", "uRLLC.dat" using 1:4:5 with errorbars linetype rgb "#9BBB59" notitle, \
     "eMBB.dat" using 1:4 with lines linetype rgb "#C0504D" title "eMBB", "eMBB.dat" using 1:4:5 with errorbars linetype rgb "#C0504D" notitle, \
     "mMTC.dat" using 1:4 with lines linetype rgb "#F79646" title "mMTC", "mMTC.dat" using 1:4:5 with errorbars linetype rgb "#F79646" notitle 
     
