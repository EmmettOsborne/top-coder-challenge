# Import necessary libraries
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the JSON data from the file
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Extract input values and expected outputs
trip_durations = [item['input']['trip_duration_days'] for item in data]
miles_traveled = [item['input']['miles_traveled'] for item in data]
receipts_amount = [item['input']['total_receipts_amount'] for item in data]
expected_outputs = [item['expected_output'] for item in data]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points with grayscale color based on expected_output
scatter = ax.scatter(trip_durations, miles_traveled, receipts_amount, c=expected_outputs, cmap='gray')

# Add a colorbar to indicate the expected output scale
fig.colorbar(scatter, label='Expected Output')

# Label the axes
ax.set_xlabel('Trip Duration (days)')
ax.set_ylabel('Miles Traveled')
ax.set_zlabel('Total Receipts Amount')

# Set a title for the plot
ax.set_title('3D Plot of Input Data with Grayscale Gradient')

# Display the plot
plt.show()