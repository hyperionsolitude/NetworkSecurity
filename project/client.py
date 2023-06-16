import socket
import json

# Server configuration
HOST = 'localhost'
PORT = 8000

# Function to send requests to the server and receive responses
def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(request.encode())
        response = client_socket.recv(1024).decode()
        print(response)

# User registration
def register_user(username):
    request = f"REGISTER:{username}"
    send_request(request)

# User login
def login_user(username, private_key):
    request = f"LOGIN:{username}:{private_key}"
    send_request(request)

# Add a new production line
def add_production_line(line_id):
    request = f"ADD_LINE:{line_id}"
    send_request(request)

# Add a new sensor to a production line
def add_sensor(line_id, sensor_id, frequency, starting_pattern):
    request = f"ADD_SENSOR:{line_id}:{sensor_id}:{frequency}:{starting_pattern}"
    send_request(request)

# Generate sensor values and save to blockchain
def generate_sensor_values():
    request = "GENERATE_DATA"
    send_request(request)

# Save blockchain to a local file
def save_blockchain():
    request = "SAVE_BLOCKCHAIN"
    send_request(request)

# Display current blockchain contents
def display_blockchain():
    request = "DISPLAY_BLOCKCHAIN"
    send_request(request)

# Delete a production line
def delete_production_line(line_id):
    request = f"DELETE_LINE:{line_id}"
    send_request(request)

# Delete a sensor
def delete_sensor(sensor_id):
    request = f"DELETE_SENSOR:{sensor_id}"
    send_request(request)
    
# Send bulk sensor addition request
def bulk_sensor_addition(common_line_id, num_of_sensors, common_frequency, common_starting_pattern):
    request = f"ADD_SENSOR_BULK:{common_line_id}:{num_of_sensors}:{common_frequency}:{common_starting_pattern}"
    send_request(request)

# Send bulk production line addition request
def bulk_prod_line_addition(num_of_prod_lines):
    request = f"ADD_PROD_LINE_BULK:{num_of_prod_lines}"
    send_request(request)

# Main program loop
while True:
    print("Welcome to the Production Line Management System!")
    print("1. Register User")
    print("2. Login User")
    print("3. Add Production Line")
    print("4. Add Sensor")
    print("5. Generate Sensor Values")
    print("6. Save Blockchain")
    print("7. Display Blockchain")
    print("8. Remove Production Line")
    print("9. Remove Sensor")
    print("10. Add Production Line in Bulk")
    print("11. Add Sensor in Bulk")
    print("12. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username: ")
        register_user(username)

    elif choice == '2':
        username = input("Enter username: ")
        private_key = input("Enter private key: ")
        login_user(username, private_key)

    elif choice == '3':
        line_id = input("Enter production line ID: ")
        add_production_line(line_id)

    elif choice == '4':
        line_id = input("Enter production line ID: ")
        sensor_id = input("Enter sensor ID: ")
        frequency = input("Enter sensor data frequency (in Hz): ")
        starting_pattern = input("Enter the starting pattern for block ID: ")
        add_sensor(line_id, sensor_id, frequency, starting_pattern)

    elif choice == '5':
        generate_sensor_values()

    elif choice == '6':
        save_blockchain()

    elif choice == '7':
        display_blockchain()

    elif choice == '8':
        line_id = input("Enter production line ID to delete: ")
        delete_production_line(line_id)

    elif choice == '9':
        sensor_id = input("Enter sensor ID to delete: ")
        delete_sensor(sensor_id)
    
    elif choice == '10':
        num_of_prod_lines = int(input("Enter the number of production lines to add: "))
        bulk_prod_line_addition(num_of_prod_lines)
    
    elif choice == '11':
        common_line_id = input("Enter the common line ID for the sensors: ")
        num_of_sensors = int(input("Enter the number of sensors to add: "))
        common_frequency = input("Enter the common frequency for the sensors: ")
        common_starting_pattern = input("Enter the common starting pattern for the sensors: ")
        bulk_sensor_addition(common_line_id, num_of_sensors, common_frequency, common_starting_pattern)
        
    elif choice == '12':
        print("Exiting...")
        break
    
    else:
        print("Invalid choice. Please try again.")
