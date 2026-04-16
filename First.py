import statistics
# List of elements
data = [2, 4, 4, 4, 5, 5, 7, 9]
# Central Tendency Measures
mean = statistics.mean(data)
median = statistics.median(data)
mode = statistics.mode(data)
# Measure of Dispersion
variance = statistics.variance(data)
std_deviation = statistics.stdev(data)
print ("Mean:", mean)
print ("Median:", median)
print ("Mode:", mode)
print ("Variance:", variance)
print ("Standard Deviation:", std_deviation)