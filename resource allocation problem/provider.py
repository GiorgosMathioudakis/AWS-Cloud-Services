from flask import Flask, request, jsonify
import requests  

app = Flask(__name__)

# Original execution time matrix
EXECUTION_TIME_MATRIX = [
    [6, 5, 4, 3.5, 3],    # Task 1 subtasks' times on resources
    [5, 4.2, 3.6, 3, 2.8],  # Task 2 subtasks' times on resources
    [4, 3.5, 3.2, 2.8, 2.4]   # Task 3 subtasks' times on resources
]

PRICE_VECTOR = [1, 1.2, 1.5, 1.8, 2]

@app.route('/receive-matrix', methods=['POST'])
def receive_matrix():
    # Retrieve allocation matrix and IPs from the request
    data = request.get_json()
    allocation_matrix = data.get('allocation_matrix')
    ips = data.get('ips')

    # Print the allocation matrix and IPs
    print("Received Allocation Matrix:")
    for row in allocation_matrix:
        print(row)

    print("\nReceived IPs:")
    for ip in ips:
        print(ip)

    # Reorder the allocation matrix based on the number of non-zero elements
    sorted_indices = sorted(range(len(allocation_matrix)), key=lambda i: sum(1 for x in allocation_matrix[i] if x != 0))
    allocation_matrix = [allocation_matrix[i] for i in sorted_indices]
    ips = [ips[i] for i in sorted_indices]

    # Update the execution time matrix using the reordered allocation matrix
    new_execution_time_matrix = update_execution_time_matrix(allocation_matrix, EXECUTION_TIME_MATRIX)

    # Calculate the expense matrix using the reordered allocation matrix
    expense_matrix = calculate_expense_matrix(new_execution_time_matrix, allocation_matrix, PRICE_VECTOR)

    # Print the reordered allocation matrix and the matrices
    print("\nReordered Allocation Matrix:")
    for row in allocation_matrix:
        print(row)

    print("\nUpdated Execution Time Matrix:")
    for row in new_execution_time_matrix:
        print(row)

    print("\nExpense Matrix:")
    for row in expense_matrix:
        print(row)

    # Send the updated matrices to the respective users
    send_updated_matrices_to_users(ips, new_execution_time_matrix, expense_matrix)

    return jsonify({
        "status": "success",
        "message": "Data received and processed successfully.",
        "allocation_matrix": allocation_matrix,
        "new_execution_time_matrix": new_execution_time_matrix,
        "expense_matrix": expense_matrix
    })

def update_execution_time_matrix(allocation_matrix, execution_time_matrix):
    # Number of rows (tasks) and columns (resources)
    num_tasks = len(execution_time_matrix)
    num_resources = len(execution_time_matrix[0])

    # Initialize a new execution time matrix with the same structure
    new_matrix = [[0] * num_resources for _ in range(num_tasks)]

    # Process each resource (column in the allocation matrix)
    for resource_idx in range(num_resources):
        # Count the number of users sharing the resource (number of 1's in the column)
        shared_count = sum(row[resource_idx] for row in allocation_matrix)

        for task_idx in range(num_tasks):
            if allocation_matrix[task_idx][resource_idx] == 1:
                # Multiply original execution time by the number of users sharing the resource
                new_matrix[task_idx][resource_idx] = (
                    execution_time_matrix[task_idx][resource_idx] * shared_count
                )
            else:
                # If the resource is not used by the task, set time to 0
                new_matrix[task_idx][resource_idx] = 0

    return new_matrix

def calculate_expense_matrix(execution_time_matrix, allocation_matrix, price_vector):
    # Number of rows (tasks) and columns (resources)
    num_tasks = len(execution_time_matrix)
    num_resources = len(execution_time_matrix[0])

    # Initialize the expense matrix with the same structure
    expense_matrix = [[0] * num_resources for _ in range(num_tasks)]

    # Process each resource (column in the allocation matrix)
    for resource_idx in range(num_resources):
        # Count the number of users sharing the resource (number of 1's in the column)
        shared_count = sum(row[resource_idx] for row in allocation_matrix)

        for task_idx in range(num_tasks):
            if execution_time_matrix[task_idx][resource_idx] != 0:
                # Multiply execution time by price and divide by shared count
                expense_matrix[task_idx][resource_idx] = (
                    execution_time_matrix[task_idx][resource_idx] * price_vector[resource_idx] / shared_count
                )
            else:
                # If the resource is not used, set expense to 0
                expense_matrix[task_idx][resource_idx] = 0

    return expense_matrix

def send_updated_matrices_to_users(ips, execution_time_matrix, expense_matrix):
    for i, ip in enumerate(ips):
        # Send only the i-th row of T and E to the user
        user_data = {
            "execution_time_row": execution_time_matrix[i],
            "expense_row": expense_matrix[i]
        }
        try:
            response = requests.post(f"http://{ip}:5000/update-matrix", json=user_data)
            print(f"Data sent to User {i + 1} ({ip}). Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error sending data to User {i + 1} ({ip}): {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
