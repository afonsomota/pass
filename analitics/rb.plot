set title "Scheduler IO (bytes)"
set terminal pngcairo
set output "rb.png"
set xrange [1900:2100]

set key outside center bottom


plot "scheduler.dat" using 1:($2+$3+$4) title "uRLLC"  with filledcurves y1=0  linetype 1, \
     "scheduler.dat" using 1:($4+$3) title "eMBB" with filledcurves y1=0 linetype 2, \
     "scheduler.dat" using 1:4 title "mMTC" with filledcurves y1=0 linetype 3
