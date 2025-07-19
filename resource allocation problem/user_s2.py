from flask import Flask, request, jsonify
import itertools
import boto3
import json

# Initialize Flask app
app = Flask(__name__)

# Hardcoded inputs for all users
PRICE_VECTOR = [1, 1.2, 1.5, 1.8, 2]
EXECUTION_TIME_MATRIX = [
    [6, 5, 4, 3.5, 3],    # Task 1 subtasks' times on resources
    [5, 4.2, 3.6, 3, 2.8],  # Task 2 subtasks' times on resources
    [4, 3.5, 3.2, 2.8, 2.4]   # Task 3 subtasks' times on resources
]

# User-specific variables
user = 2  # Task ID (user 1, user 2, or user 3)
subtasks = 3  # Number of subtasks for this user

# AWS SQS setup
sqs = boto3.client('sqs', region_name='us-east-1')
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/089781853604/SubmissionsQueue'

updated_execution_time_row = []
updated_expense_row = []


# Utility function
def calculate_utility(allocation, execution_time_matrix, price_vector, task_idx):
    # Translate binary allocation vector into indices of selected resources
    selected_resources = [i for i, val in enumerate(allocation) if val == 1]

    # Ensure the number of selected resources matches the number of subtasks
    if len(selected_resources) != subtasks:
        return -1  # Invalid allocation

    # Calculate max execution time and total cost
    max_time = max(execution_time_matrix[task_idx][resource_idx] for resource_idx in selected_resources)
    total_cost = sum(price_vector[resource_idx] for resource_idx in selected_resources)

    # Utility calculation
    wt = 0.5  # Weight for time
    we = 0.5  # Weight for cost
    return 1 / (wt * max_time + we * total_cost)

# Generate all possible allocations for a task
def generate_valid_allocations(num_subtasks, num_resources):
    # Generate all binary vectors of length num_resources with num_subtasks 1's
    return [list(allocation) for allocation in itertools.permutations([1] * num_subtasks + [0] * (num_resources - num_subtasks), num_resources) if sum(allocation) == num_subtasks]

# Find optimal allocation for this user
def find_optimal_allocation():
    task_idx = user - 1  # Convert 1-based user index to 0-based task index
    num_resources = len(PRICE_VECTOR)  # Number of resources

    all_allocations = generate_valid_allocations(subtasks, num_resources)
    best_utility = -1
    best_allocation = None

    for allocation in all_allocations:
        utility = calculate_utility(allocation, EXECUTION_TIME_MATRIX, PRICE_VECTOR, task_idx)
        if utility > best_utility:
            best_utility = utility
            best_allocation = allocation
        
    print(f"User {user} - Best Allocation Vector: {best_allocation}, Utility: {best_utility}")
    return best_allocation, best_utility

# Send data to SQS
def send_to_sqs(allocation, ip):
    message = {
        'user': user,
        'allocation_vector': allocation,
        'public_ip': ip
    }
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    print("Message sent to SQS:", response)
    return response

# Flask endpoint to calculate and submit optimal allocation for this user
@app.route('/calculate-allocation', methods=['POST'])
def calculate_allocation():
    # Find the best allocation for this user
    best_allocation, best_utility = find_optimal_allocation()

    # Simulating user's public IP address (would be fetched dynamically in real implementation)
    public_ip = request.json.get('public_ip', '172.31.86.79')

    # Send to SQS
    send_to_sqs(best_allocation, public_ip)

    return jsonify({
        "status": "success",
        "user": user,
        "best_allocation": best_allocation,
        "utility": best_utility
    })



# Flask endpoint to update the execution time matrix
@app.route('/update-matrix', methods=['POST'])
def update_matrix():
    global EXECUTION_TIME_MATRIX, PRICE_VECTOR
    
    # Get the new execution time and expense rows from the provider
    data = request.get_json()
    updated_execution_time_row = data.get('execution_time_row')
    updated_expense_row = data.get('expense_row')

    best_allocation_vector, some_best_utility = find_optimal_allocation()

    # Print the updated rows for debugging
    print("Updated Execution Time Row:", updated_execution_time_row)
    print("Updated Expense Row:", updated_expense_row)

    # Update the user's execution time matrix and price vector
    task_idx = user - 1  # Task index (user-specific)
    EXECUTION_TIME_MATRIX[task_idx] = updated_execution_time_row
    PRICE_VECTOR = updated_expense_row

    # Recalculate the utility using the updated data
    new_utility = calculate_utility(best_allocation_vector, EXECUTION_TIME_MATRIX, PRICE_VECTOR, task_idx)

    print(f"New Utility for User {user}: {new_utility}")

    return jsonify({
        "status": "success",
        "new_utility": new_utility,
        "updated_execution_time_row": updated_execution_time_row,
        "updated_expense_row": updated_expense_row
    })


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Listen on all network interfaces, port 5000
