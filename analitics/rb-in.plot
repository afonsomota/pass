#set title "Scheduled resources with input"
set terminal pdfcairo size 4.5,3
set output "rb-in.pdf"
set xrange [1950:2030]

set y2label "Bytes"
set y2tics
set ylabel "Resources"
set xlabel "Simulation time (ms)

set key outside below height 2 center horizontal


plot "scheduler.dat" using 1:($2+$3+$4) title "uRLLC"  with filledcurves y1=0  linetype rgb "#D7E4BD", \
     "scheduler.dat" using 1:($4+$3) title "eMBB" with filledcurves y1=0 linetype rgb "#E6B9B8", \
     "scheduler.dat" using 1:4 title "mMTC" with filledcurves y1=0 linetype rgb "#FCD5B5", \
     "mMTC-io.dat"  using 1:2 title "eMBB input traffic" with lines axes x1y2 lt rgb "#F79646" lw 2, \
     "eMBB-io.dat"  using 1:2 title "eMBB input traffic" with lines axes x1y2 lt rgb "#C0504D" lw 2, \
     "uRLLC-io.dat"  using 1:2 title "uRLLC input traffic" with lines axes x1y2 lt rgb "#8BAB49" lw 2, \
