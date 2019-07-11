set title "Scheduler IO (bytes)"
set terminal pdfcairo size 4.5,2
set output "io.pdf"
set xrange [1900:2100]
set key outside below height 2 center horizontal
set xlabel "Simulation time (ms)"

set multiplot layout 1,2 
set ylabel "Input traffic (bytes)"

plot "uRLLC-io.dat" using 1:2 with lines linetype 1 title "uRLLC" ,\
     "eMBB-io.dat"  using 1:2 with lines linetype 2 title "eMBB" ,\
     "mMTC-io.dat"  using 1:2 with lines linetype 3 title "mMTC"

set ylabel "Output traffic (bytes)"
plot "uRLLC-io.dat" using 1:3 with lines linetype 1 title "uRLLC", \
     "eMBB-io.dat" using 1:3 with lines linetype 2 title "eMBB" , \
     "mMTC-io.dat" using 1:3 with lines linetype 3 title "mMTC"

unset multiplot
