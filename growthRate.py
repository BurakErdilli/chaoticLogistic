import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters for chaotic behavior
maxGrowthRate = 4
initialPopulation = 0.4
generations = 50
resolution = 0.001
CurrentGrowthRate = 0
growth_rates = []
equil = []

# Data collection for high-resolution points
data_points = []

# Simulation with chaotic tracking
while CurrentGrowthRate < maxGrowthRate - resolution:
    currentPopulation = initialPopulation
    
    # Evolve population over the generations
    for gen in range(generations):
        next_population = CurrentGrowthRate * currentPopulation * (1 - currentPopulation)
        currentPopulation = next_population

    # Collect population values and growth rates
    for gen in range(100):
        next_population = CurrentGrowthRate * currentPopulation * (1 - currentPopulation)
        currentPopulation = next_population
        equil.append(currentPopulation)
        growth_rates.append(CurrentGrowthRate)
        
        # Store every point with high resolution
        data_points.append((CurrentGrowthRate, currentPopulation))
    
    CurrentGrowthRate += resolution

# Convert the data points to a DataFrame for easy saving
df = pd.DataFrame(data_points, columns=['Growth Rate', 'Population'])

# Save the data points to a CSV file
df.to_csv('logistic_map_data.csv', index=False)

# Plotting the chaotic logistic map
plt.figure(figsize=(12, 8), dpi=300)  # High resolution

# Scatter plot for all points
plt.plot(growth_rates, equil, 'b.', markersize=0.5)  # Original points
plt.scatter(df['Growth Rate'], df['Population'], c='red', s=1, label='Data Points')  # New points in red

plt.title(f'Logistic Map: Population Equilibrium vs Growth Rate (Resolution = {resolution})')
plt.xlabel('Growth Rate')
plt.ylabel('Equilibrium Population')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot as an SVG file
plt.savefig('logistic_map.svg', format='svg', bbox_inches='tight')
# Save as PDF before showing the plot
plt.savefig('logistic_map.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()
