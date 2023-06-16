import socket
import json
import hashlib
import random
import time
import threading
from datetime import datetime
import matplotlib.pyplot as plt
# Blockchain data storage
blockchain = []

# Users data storage
users = {}

# Production lines and sensors data storage
production_lines = {}
sensors = {}

highest_frequency = 0
average_elapsed_time = 0
cumulative_elapsed_time = 0
block_num = 0
q=0

tot_block_num = []
avg_elaps_time = []
curr_sensor_num = []

# Generate a random private/public key pair
def generate_key_pair():
    # Generate private key (random 16 characters)
    private_key = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=64))

    # Generate public key (hash of private key)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()

    return private_key, public_key

# Register a new user
def register_user(username):
    if username in users:
        return "Username already exists. Please choose a different username."

    private_key, public_key = generate_key_pair()

    users[username] = {
        'private_key': private_key,
        'public_key': public_key,
        'authenticated': False,
        'permissions': 'admin' if len(users) == 0 else 'normal'
    }

    return f"User '{username}' registered successfully!\nPublic key: {public_key}\nPrivate key: {private_key}"

# Login user and authenticate using public key
def login_user(username, private_key):
    if username not in users:
        return "User not found. Please register first."

    if users[username]['private_key'] != private_key:
        return "Invalid public key. Authentication failed."

    users[username]['authenticated'] = True
    return f"Welcome, {username}!"

# Add a new production line (admin only)
def add_production_line(line_id, username):
    if line_id in production_lines:
        return "Production line already exists. Please choose a different line ID."

    if users[username]['permissions'] != 'admin':
        return "Insufficient permissions. Only admins can add production lines."

    production_lines[line_id] = []
    return f"Production line '{line_id}' added successfully!"

# Add a new sensor to a production line (admin only)
def add_sensor(line_id, sensor_id, frequency, starting_pattern, username):
    global sensors
    if line_id not in production_lines:
        return "Production line not found. Please choose an existing line ID."

    if sensor_id in sensors:
        return "Sensor already exists. Please choose a different sensor ID."

    if users[username]['permissions'] != 'admin':
        return "Insufficient permissions. Only admins can add sensors."

    sensors[sensor_id] = {
        'line_id': line_id,
        'frequency': float(frequency),
        'last_update_time': time.time(),
        'values': [],
        'starting_pattern': starting_pattern
    }

    production_lines[line_id].append(sensor_id)
    return f"Sensor '{sensor_id}' added successfully to production line '{line_id}'!"

# Bulk add sensors
def add_sensor_bulk(common_line_id, num_of_sensors, common_frequency, common_starting_pattern, username):
    global q,sensors
    q = 0
    counter = 1
    while (counter < num_of_sensors):
        q = q + 1
        if q in sensors:
            continue
        else:
            add_sensor(common_line_id, q, common_frequency, common_starting_pattern, username)
            counter = counter + 1

# Bulk add production lines
def add_prod_line_bulk(num_of_prod_lines, username):
    for line_id in range(len(production_lines)+1,len(production_lines)+num_of_prod_lines):
        response = add_production_line(line_id, username)

# Generate random sensor values and save to blockchain
def generate_sensor_values_and_save(username):
    global cumulative_elapsed_time, block_num,tot_block_num,avg_elaps_time,curr_sensor_num

    current_time = time.time()
    values = {}
    
    for sensor_id, sensor_info in sensors.items():
        line_id = sensor_info['line_id']
        frequency = sensor_info['frequency']
        last_update_time = sensor_info['last_update_time']
        values_list = sensor_info['values']
        starting_pattern = sensor_info['starting_pattern']

        if current_time - last_update_time >= (1 / frequency):
            value = random.randint(0, 255)
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            block_id = ''
            nonce = 0
            start_calculation_time = time.time()
            block_data = str(blockchain[-1]) + str(values_list) + str(random.random())
            while not block_id.startswith(starting_pattern):
                block_data = str(block_data) + str(nonce)
                block_id = hashlib.sha256(block_data.encode()).hexdigest()
                nonce += 1
            elapsed_time = time.time() - start_calculation_time
            cumulative_elapsed_time = cumulative_elapsed_time + elapsed_time
            block_num = block_num + 1
            average_elapsed_time = cumulative_elapsed_time / block_num
            values_list.append({
                'block_id': block_id,
                'timestamp': timestamp,
                'line_id': line_id,
                'sensor_id': sensor_id,
                'value': value,
                'elapsed_time': elapsed_time
            })
            
            tot_block_num.append(block_num)
            avg_elaps_time.append(average_elapsed_time)
            curr_sensor_num.append(len(sensors.items()))
            sensor_info['last_update_time'] = current_time

        values[sensor_id] = {
            'line_id': line_id,
            'values': values_list
        }

    
    # Save values to the blockchain
    if values not in blockchain:
        blockchain.append(values)

    return values

# Plotting the data
def dataplot():
    fig, ax1 = plt.subplots()

    ax1.plot(tot_block_num, avg_elaps_time, label='Total Block Number', color='blue')
    ax1.set_xlabel('Block Number')
    ax1.set_ylabel('Average Elapsed Time in seconds', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(tot_block_num, curr_sensor_num, label='Current Sensor Number', color='red')
    ax2.set_ylabel('Current Sensor Number', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Average Elapsed Time and Current Sensor Number vs. Block Number')
    plt.savefig('graph.png')  # Save the plot as an image file
    plt.close()  # Close the plot

# Save blockchain to a local file
def save_blockchain():
    with open('blockchain.json', 'w') as file:
        json.dump(blockchain, file, indent=4)
    return "Blockchain saved successfully!"

# Display current blockchain contents
def display_blockchain():
    if len(blockchain) == 0:
        return "Blockchain is empty."

    output = ""
    for values in blockchain:
        for sensor_id, data in values.items():
            line_id = data['line_id']
            values_list = data['values']
            for value in values_list:
                timestamp = value['timestamp']
                sensor_value = value['value']
                elapsed_time = value['elapsed_time']
                output += f"Timestamp: {timestamp}\nLine Number: {line_id}\nSensor Number: {sensor_id}\nSensor value: {sensor_value}\nElapsed Time: {elapsed_time} seconds\n\n"

    return output

def find_highest_frequency():
    global highest_frequency
    for sensor_id,sensor_info in sensors.items():
        frequency = sensor_info['frequency']
        if frequency > highest_frequency:
            highest_frequency = frequency
    return highest_frequency

# Periodically generate sensor values and save to blockchain
def periodic_sensor_value_generation():
    global cumulative_elapsed_time, block_num,tot_block_num,avg_elaps_time,curr_sensor_num,highest_frequency

    while True:
        highest_frequency = find_highest_frequency()
        if highest_frequency == 0:
            # Handle case when no sensors present
            period = 1  # Set a default period of 1 second or adjust as needed
        else:
            period = 1 / highest_frequency
        
        if len(sensors) != 0:
            generate_sensor_values_and_save(username=None)
            save_blockchain()
            dataplot()
            print(highest_frequency)
            time.sleep(period)

# Delete a production line (admin only)
def delete_production_line(line_id, username):
    if line_id not in production_lines:
        return "Production line not found."

    if users[username]['permissions'] != 'admin':
        return "Insufficient permissions. Only admins can delete production lines."

    # Check if any sensors are associated with the production line
    if production_lines[line_id]:
        return "Cannot delete production line. Sensors are still attached to it."

    del production_lines[line_id]
    return f"Production line '{line_id}' deleted successfully!"

# Delete a sensor (admin only)
def delete_sensor(sensor_id, username):
    global highest_frequency
    if sensor_id not in sensors:
        return "Sensor not found."

    if users[username]['permissions'] != 'admin':
        return "Insufficient permissions. Only admins can delete sensors."

    line_id = sensors[sensor_id]['line_id']
    production_lines[line_id].remove(sensor_id)
    del sensors[sensor_id]
    highest_frequency = 0
    highest_frequency=find_highest_frequency()
    return f"Sensor '{sensor_id}' deleted successfully!"

# Server configuration
HOST = 'localhost'
PORT = 8000

# Start the server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server is running on {HOST}:{PORT}")

        # Start the periodic sensor value generation thread
        sensor_value_thread = threading.Thread(target=periodic_sensor_value_generation)
        sensor_value_thread.daemon = True
        sensor_value_thread.start()

        while True:
            client_socket, addr = server_socket.accept()
            print(f"New connection from {addr}")

            # Receive client request
            request = client_socket.recv(1024).decode()


            if request.startswith('REGISTER'):
                # Register a new user
                _, username = request.split(':')
                response = register_user(username)
                client_socket.sendall(response.encode())

            elif request.startswith('LOGIN'):
                # Login user
                _, username, private_key = request.split(':')
                response = login_user(username, private_key)
                client_socket.sendall(response.encode())

            elif not request.startswith('LOGIN') and not request.startswith('REGISTER'):
                # Check if user is logged in
                user_authenticated = False
                for username, user_info in users.items():
                    if 'authenticated' in user_info and user_info['authenticated']:
                        user_authenticated = True
                        break

                if not user_authenticated:
                    client_socket.sendall("You are not logged in. Please log in first.".encode())
                    continue

                if request.startswith('ADD_LINE'):
                    # Add a new production line
                    _, line_id = request.split(':')
                    response = add_production_line(line_id, username)
                    client_socket.sendall(response.encode())

                elif request.startswith('ADD_SENSOR'):
                    # Add a new sensor
                    _, line_id, sensor_id, frequency, starting_pattern = request.split(':')
                    response = add_sensor(line_id, sensor_id, frequency, starting_pattern, username)
                    client_socket.sendall(response.encode())

                elif request.startswith('SAVE_BLOCKCHAIN'):
                    # Save blockchain to a local file
                    response = save_blockchain()
                    client_socket.sendall(response.encode())

                elif request.startswith('DISPLAY_BLOCKCHAIN'):
                    # Display current blockchain contents
                    response = display_blockchain()
                    client_socket.sendall(response.encode())
                # Handle admin actions for deleting production lines and sensors
                if request.startswith('DELETE_LINE'):
                    # Delete a production line
                    _, line_id = request.split(':')
                    response = delete_production_line(line_id, username)
                    client_socket.sendall(response.encode())

                elif request.startswith('DELETE_SENSOR'):
                    # Delete a sensor
                    _, sensor_id = request.split(':')
                    response = delete_sensor(sensor_id, username)
                    client_socket.sendall(response.encode())
                
                elif request.startswith('ADD_SENSOR_BULK'):
                    # Bulk add sensors
                    _, common_line_id, num_of_sensors, common_frequency, common_starting_pattern = request.split(':')
                    num_of_sensors = int(num_of_sensors)
                    add_sensor_bulk(common_line_id, num_of_sensors, common_frequency, common_starting_pattern, username)
                    client_socket.sendall("Bulk sensor addition completed.".encode())

                elif request.startswith('ADD_PROD_LINE_BULK'):
                    # Bulk add production lines
                    _, num_of_prod_lines = request.split(':')
                    num_of_prod_lines = int(num_of_prod_lines)
                    add_prod_line_bulk(num_of_prod_lines, username)
                    client_socket.sendall("Bulk production line addition completed.".encode())

            else:
                client_socket.sendall("Invalid request.".encode())

# Start the server
start_server()
