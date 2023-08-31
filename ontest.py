import serial as pyserial
import struct
import time

def detect_com_ports():
    """Returns a list of all connected COM ports."""
    com_ports = []
    for i in range(256):
        try:
            port = pyserial.Serial(f"COM{i}", baudrate=9600, timeout=1)
            port.close()
            com_ports.append(f"COM{i}")
        except pyserial.SerialException:
            pass
    return com_ports

def send_hex_command(com_port, hex_command, wait_for_reply=False, delay_after_reply=0):
    """Sends a HEX command to the specified COM port and waits for a reply if necessary."""
    ser = pyserial.Serial(com_port, baudrate=9600, timeout=1)
    
    # Converting the space-separated hex string into a bytes object
    hex_bytes = bytes.fromhex(hex_command.replace(" ", ""))
    ser.write(hex_bytes)
    
    time.sleep(0.005) # 5 ms delay

    if wait_for_reply:
        reply = ser.read_until() # Read until a termination character or timeout
        print(f"Received reply: {reply}")

        if delay_after_reply:
            time.sleep(delay_after_reply)
            
    ser.close()

def send_ascii_command(com_port, ascii_command):
    """Sends an ASCII command to the specified COM port."""
    ser = pyserial.Serial(com_port, baudrate=9600, timeout=1)
    data = ascii_command.encode()
    ser.write(data)
    time.sleep(0.5)
    ser.close()

def main():
    """Detects all connected COM ports and sends a list of ASCII commands first, then a list of HEX commands."""
    com_ports = detect_com_ports()
    hex_commands = [
        ("01 30 41 30 41 30 43 02 43 32 30 33 44 36 30 30 30 31 03 73 0D", True, 15), # Power On example, adjust as needed
        # Add more hex_commands as needed, with appropriate wait_for_reply and delay_after_reply values
    ]
    ascii_commands = [
        "ka 01 01\r",
    ]
    for com_port in com_ports:
        # Send ASCII commands first
        for ascii_command in ascii_commands:
            send_ascii_command(com_port, ascii_command)

        # Send Hex commands
        for hex_command, wait_for_reply, delay_after_reply in hex_commands:
            while True:  # Keep sending the power-on command
                send_hex_command(com_port, hex_command, wait_for_reply, delay_after_reply)
                time.sleep(0.005)  # 5 ms delay between each send
                
                # Uncomment the next line if you want to exit the loop after some time or condition
                # break  

if __name__ == "__main__":
    main()
