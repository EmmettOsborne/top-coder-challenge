import sys
import math

# print(f"Received inputs: days={sys.argv[1]}, miles={sys.argv[2]}, receipts={sys.argv[3]}")

def calculate_reimbursement(days, miles, receipts):
    x0 = days
    x1 = miles
    x2 = receipts
    
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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>")
        sys.exit(1)
    
    try:
        days = float(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])
        reimbursement = calculate_reimbursement(days, miles, receipts)
        print(f"{reimbursement:.2f}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)