import json
import math

def custom_calculation(input_data):
    x0 = input_data['trip_duration_days']
    x1 = input_data['miles_traveled']
    x2 = input_data['total_receipts_amount']
    
    reimbursement = (
        0.44936344 * x1 - 0.44936344 * x2 +
        253.735503207516 * math.log(97518.23 * x0) +
        168.28207 * math.log((x2 + 145.86661)**3) +
        168.28207 * math.log((x2 - 404.10373)**2 + 16155.376) -
        7440.1996278269
    )
    return reimbursement

# Load the JSON data from the file
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

# For MAPE and percentage within 10%, consider only valid pairs where exp != 0
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

# Compute Pearson correlation coefficient
mean_calc = sum(calculated_outputs) / n
mean_exp = sum(expected_outputs) / n
cov = sum((calc - mean_calc) * (exp - mean_exp) for calc, exp in zip(calculated_outputs, expected_outputs)) / n
var_calc = sum((calc - mean_calc)**2 for calc in calculated_outputs) / n
var_exp = sum((exp - mean_exp)**2 for exp in expected_outputs) / n
if var_calc > 0 and var_exp > 0:
    correlation = cov / (var_calc ** 0.5 * var_exp ** 0.5)
else:
    correlation = None

# Print the statistics
print("Statistics:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
if mape is not None:
    print(f"MAPE: {mape:.2f}%")
else:
    print("MAPE: N/A (no valid data points)")
print(f"Min absolute difference: {min_abs_diff:.2f}")
print(f"Max absolute difference: {max_abs_diff:.2f}")
if percentage_within_10pct is not None:
    print(f"Percentage within 10% relative error: {percentage_within_10pct:.2f}%")
else:
    print("Percentage within 10% relative error: N/A")
if correlation is not None:
    print(f"Pearson correlation coefficient: {correlation:.4f}")
else:
    print("Pearson correlation coefficient: N/A")