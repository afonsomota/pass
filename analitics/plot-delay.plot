set title "Average packet delay"
set terminal pngcairo
set output "delay.png"
set yrange [0:16]

set key outside below height 2 center horizontal
set xlabel "Simulation time (s)"
set ylabel "Delay (ms)"

plot "uRLLC.dat" with lines linetype rgb "#9BBB59" title "uRLLC", "uRLLC.dat" using 1:2:3 with errorbars linetype rgb "#9BBB59" notitle, \
     "eMBB.dat" with lines lt rgb "#C0504D" title "eMBB", "eMBB.dat" using 1:2:3 with errorbars linetype rgb "#C0504D" notitle, \
     "mMTC.dat" with lines linetype rgb "#F79646" title "mMTC", "mMTC.dat" using 1:2:3 with errorbars linetype rgb "#F79646" notitle
     
