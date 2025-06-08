import json
import math

def custom_calculation(input_data):
    x0 = input_data['trip_duration_days']
    x1 = input_data['miles_traveled']
    x2 = input_data['total_receipts_amount']
    
    # Constants
    A = 22.757409493611178  # Coefficient for x0
    B = 0.35684298303001777  # Coefficient for x1
    C = 379.6973286153752    # Threshold for x2
    D = 1331.322873040726    # Cap value for PW1
    E = 48.039398955855596   # Coefficient for x0 in PW2
    F = 293.2196305720263    # Constant in PW2
    G = -34.32244823213331   # Cap value for PW2
    
    # Compute intermediate term S = x0 * sqrt(x1)
    S = x0 * math.sqrt(x1)
    
    # PW1: min(x0 * sqrt(x1) + max(x2, C), D)
    PW1 = min(S + max(x2, C), D)
    
    # PW2: min(E * x0 - F, G)
    PW2 = min(E * x0 - F, G)
    
    # Total reimbursement
    reimbursement = A * x0 + B * x1 + PW1 + PW2
    return reimbursement

# Load JSON data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

calculated_outputs = []
expected_outputs = []

for item in data:
    calc = custom_calculation(item['input'])
    calculated_outputs.append(calc)
    expected_outputs.append(item['expected_output'])

# Compute statistics
absolute_diffs = [abs(calc - exp) for calc, exp in zip(calculated_outputs, expected_outputs)]
n = len(calculated_outputs)

mae = sum(absolute_diffs) / n
mse = sum((calc - exp)**2 for calc, exp in zip(calculated_outputs, expected_outputs)) / n
rmse = mse ** 0.5

# MAPE and percentage within 10% for non-zero expected outputs
valid_pairs = [(calc, exp) for calc, exp in zip(calculated_outputs, expected_outputs) if exp != 0]
if valid_pairs:
    mape = (sum(abs(calc - exp) / exp for calc, exp in valid_pairs) / len(valid_pairs)) * 100
    count_within_10pct = sum(1 for calc, exp in valid_pairs if abs(calc - exp) / exp <= 0.1)
    percentage_within_10pct = (count_within_10pct / len(valid_pairs)) * 100
else:
    mape = None
    percentage_within_10pct = None

min_abs_diff = min(absolute_diffs) if absolute_diffs else None
max_abs_diff = max(absolute_diffs) if absolute_diffs else None

# Pearson correlation coefficient
mean_calc = sum(calculated_outputs) / n
mean_exp = sum(expected_outputs) / n
cov = sum((calc - mean_calc) * (exp - mean_exp) for calc, exp in zip(calculated_outputs, expected_outputs)) / n
var_calc = sum((calc - mean_calc)**2 for calc in calculated_outputs) / n
var_exp = sum((exp - mean_exp)**2 for exp in expected_outputs) / n
correlation = cov / (var_calc ** 0.5 * var_exp ** 0.5) if var_calc > 0 and var_exp > 0 else None

# Print statistics
print("Statistics:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%" if mape is not None else "MAPE: N/A (no valid data points)")
print(f"Min absolute difference: {min_abs_diff:.2f}")
print(f"Max absolute difference: {max_abs_diff:.2f}")
print(f"Percentage within 10% relative error: {percentage_within_10pct:.2f}%" if percentage_within_10pct is not None else "Percentage within 10% relative error: N/A")
print(f"Pearson correlation coefficient: {correlation:.4f}" if correlation is not None else "Pearson correlation coefficient: N/A")