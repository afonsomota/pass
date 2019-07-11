set title "In-profile scheduled resources"
set terminal pngcairo
set output "rb-ip.png"
set xrange [1900:2100]

set key outside center bottom horizontal


plot "profiled.dat" using 1:($2+$3+$4+$5) title "Out-profile" with filledcurves y1=0 linetype rgb "grey", \
     "profiled.dat" using 1:($2+$3+$4) title "In-profile uRLLC"  with filledcurves y1=0  linetype 1, \
     "profiled.dat" using 1:($4+$3) title "In-profile eMBB" with filledcurves y1=0 linetype 2, \
     "profiled.dat" using 1:4 title "In-profile mMTC" with filledcurves y1=0 linetype 3
