import numpy as np
from scipy import stats
data = np.array([12, 15, 20, 20, 21, 18, 30, 25, 20, 15])

mean = np.mean(data)
median = np.median(data)
mode = stats.mode(data, keepdims=True)   # keepdims=True for new scipy versions

# Measures of Dispersion
variance = np.var(data, ddof=1)  # sample variance (ddof=1)
std_dev = np.std(data, ddof=1)   # sample standard deviation

# Display results
print("Data:", data)
print("\n--- Central Tendency ---")
print("Mean:", mean)
print("Median:", median)
print("Mode:", mode.mode[0], " (Count:", mode.count[0], ")")

print("\n--- Dispersion ---")
print("Variance:", variance)
print("Standard Deviation:", std_dev)
