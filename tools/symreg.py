import json
import numpy as np
from pysr import PySRRegressor

# Load JSON data from file
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Extract input features and target into NumPy arrays
X = np.array([[item['input']['trip_duration_days'], 
               item['input']['miles_traveled'], 
               item['input']['total_receipts_amount']] for item in data])
y = np.array([item['expected_output'] for item in data])

# Print data shape to confirm loading
print(f"Loaded {len(data)} data points with {X.shape[1]} features each.")

# Initialize PySRRegressor with basic configuration
model = PySRRegressor(
    maxsize=500,                    # Limit expression complexity
    niterations=2000,                # Number of search iterations
    binary_operators=["+", "*", "-", "/"],  # Basic arithmetic operators
    unary_operators=[
        "square(x) = x^2",         # Custom square function
        "cube(x) = x^3",           # Custom cube function
        "sqrt",                    # Square root (built-in Julia)
        "exp",                     # Exponential (built-in Julia)
        "log"                      # Natural logarithm (built-in Julia)
    ],
    extra_sympy_mappings={"square": lambda x: x**2, "cube": lambda x: x**3},  # SymPy mappings for custom operators
    elementwise_loss="loss(prediction, target) = (prediction - target)^2"     # Squared error loss
)

# Fit the model to the data
model.fit(X, y)

# Print the discovered equations
print("\nDiscovered Equations:")
print(model.equations_)

# Save equations to a CSV file for later inspection
model.equations_.to_csv('equations.csv', index=False)

# Print the selected equation in SymPy format
print("\nSelected Equation (SymPy format):")
print(model.sympy())