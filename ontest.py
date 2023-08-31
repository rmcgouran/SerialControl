import serial as pyserial
import time

# Function to detect all COM ports, but ignore those specified in the ignore list
def detect_com_ports(ignore_ports=[]):
    com_ports = []
    for i in range(256):
        port_name = f"COM{i}"
        # Skip the port if it is in the ignore list
        if port_name in ignore_ports:
            continue
        try:
            # Try to open the port
            port = pyserial.Serial(port_name, baudrate=9600, timeout=1)
            port.close()
            com_ports.append(port_name)
        except pyserial.SerialException:
            pass
    return com_ports

# Function to send a HEX command to a COM port
def send_hex_command(com_port, hex_command, wait_for_reply=False, delay_after_reply=0):
    # Open the COM port
    ser = pyserial.Serial(com_port, baudrate=9600, timeout=1)
    # Convert the hex string to bytes
    hex_bytes = bytes.fromhex(hex_command.replace(" ", ""))
    # Send the command
    ser.write(hex_bytes)
    # Wait for 5ms as required
    time.sleep(0.005)

    # If a reply is expected
    if wait_for_reply:
        reply = ser.read_until()
        print(f"Received reply: {reply}")
        # If there is a delay after receiving the reply
        if delay_after_reply:
            time.sleep(delay_after_reply)

    ser.close()

# Function to send an ASCII command to a COM port
def send_ascii_command(com_port, ascii_command):
    # Open the COM port
    ser = pyserial.Serial(com_port, baudrate=9600, timeout=1)
    # Convert ASCII command to bytes
    data = ascii_command.encode()
    # Send the command
    ser.write(data)
    # Wait for half a second
    time.sleep(0.5)
    ser.close()

# Main function
def main():
    # List of COM ports to ignore
    ignore_ports = ["COM3", "COM4"]
    # Detect COM ports, excluding those in the ignore list
    com_ports = detect_com_ports(ignore_ports)

    # Check if any COM ports are detected
    if not com_ports:
        print("No COM ports detected")
        return
    else:
        print(f"Detected COM ports: {com_ports}")

    # List of HEX commands to send
    hex_commands = [
        ("01 30 41 30 41 30 43 02 43 32 30 33 44 36 30 30 30 31 03 73 0D", True, 15),
    ]
    
    # List of ASCII commands to send
    ascii_commands = [
        "ka 01 01\r",
    ]

    # Loop through each COM port and send each command
    for com_port in com_ports:
        # Send ASCII commands first
        for ascii_command in ascii_commands:
            send_ascii_command(com_port, ascii_command)

        # Send HEX commands
        for hex_command, wait_for_reply, delay_after_reply in hex_commands:
            while True:
                send_hex_command(com_port, hex_command, wait_for_reply, delay_after_reply)
                # Wait for 5ms between sending each command
                time.sleep(0.005)

                # Uncomment to exit loop
                # break

if __name__ == "__main__":
    main()
