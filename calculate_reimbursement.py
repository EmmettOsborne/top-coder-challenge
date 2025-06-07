import sys
import math

# print(f"Received inputs: days={sys.argv[1]}, miles={sys.argv[2]}, receipts={sys.argv[3]}")

def calculate_reimbursement(days, miles, receipts):
    if days <= 0:
        raise ValueError("trip_duration_days must be greater than 0")
    if receipts < 0:
        raise ValueError("total_receipts_amount cannot be negative")
    
    term1 = 0.44936344 * miles
    term2 = -0.44936344 * receipts
    term3 = 253.735503207516 * math.log(97518.23 * days)
    term4 = 168.28207 * math.log((receipts + 145.86661)**3)
    term5 = 168.28207 * math.log((receipts - 404.10373)**2 + 16155.376)
    constant = -7440.1996278269
    
    reimbursement = term1 + term2 + term3 + term4 + term5 + constant
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