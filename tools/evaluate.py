# Import necessary libraries
import json

def differs_in_one_field(item1, item2):
    input1 = item1['input']
    input2 = item2['input']
    diff_fields = []
    if input1['trip_duration_days'] != input2['trip_duration_days']:
        diff_fields.append('trip_duration_days')
    if input1['miles_traveled'] != input2['miles_traveled']:
        diff_fields.append('miles_traveled')
    if input1['total_receipts_amount'] != input2['total_receipts_amount']:
        diff_fields.append('total_receipts_amount')
    if len(diff_fields) == 1:
        return diff_fields[0]
    else:
        return None

def print_data_point(item):
    print(f"trip_duration_days: {item['input']['trip_duration_days']}, miles_traveled: {item['input']['miles_traveled']}, total_receipts_amount: {item['input']['total_receipts_amount']}, expected_output: {item['expected_output']}")

def evaluate_data(data):
    print(f"Number of data points: {len(data)}")
    print("Finding pairs that differ in only one input field...")
    pair_count = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            differing_field = differs_in_one_field(data[i], data[j])
            if differing_field:
                pair_count += 1
                print(f"Pair {pair_count}:")
                print("Data point 1:")
                print_data_point(data[i])
                print("Data point 2:")
                print_data_point(data[j])
                print(f"Differs in: {differing_field}")
                print()
    print(f"Total number of pairs that differ in only one input field: {pair_count}")

if __name__ == '__main__':
    # Load the JSON data from the file
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    # Call the evaluation function
    evaluate_data(data)