# Set the title of the plot
set title "Temperature vs Magnetization"

# Label the axes
set xlabel "Temperature"
set ylabel "Magnetization"

set terminal pngcairo size 800,600 enhanced font 'Arial,12'
set output "temperature_vs_magnetization.png"
# Set the output terminal (optional, for better visuals or export)
# Uncomment below line for PNG output
# set terminal pngcairo size 800,600 enhanced font 'Arial,12'
# set output "plot.png"

# Plot data from the file
plot "energy.dat" using 1:2 with linespoints title "Magnetization"
