import serial as pyserial
import time

def detect_com_ports(ignore_ports=[]):
    """Returns a list of all connected COM ports, ignoring those in the ignore_ports list."""
    com_ports = []
    for i in range(256):
        port_name = f"COM{i}"
        if port_name in ignore_ports:
            continue
        try:
            port = pyserial.Serial(port_name, baudrate=9600, timeout=1)
            port.close()
            com_ports.append(port_name)
        except pyserial.SerialException:
            pass
    return com_ports

def send_hex_command(com_port, hex_command, wait_for_reply=False, delay_after_reply=0):
    """Sends a HEX command to the specified COM port and waits for a reply if necessary."""
    ser = pyserial.Serial(com_port, baudrate=9600, timeout=1)
    hex_bytes = bytes.fromhex(hex_command.replace(" ", ""))
    ser.write(hex_bytes)
    time.sleep(0.005)

    if wait_for_reply:
        reply = ser.read_until()
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
    """Detects all connected COM ports, ignoring specified ports, and then sends a list of ASCII commands first, followed by a list of HEX commands."""
    
    ignore_ports = ["COM3", "COM4"]  # Add the COM ports you want to ignore here
    com_ports = detect_com_ports(ignore_ports)
    
    if not com_ports:
        print("No COM ports detected")
        return
    hex_commands = [
        ("01 30 41 30 41 30 43 02 43 32 30 33 44 36 30 30 30 31 03 73 0D", True, 15),
    ]
    
    ascii_commands = [
        "ka 01 01\r",
    ]

    for com_port in com_ports:
        for ascii_command in ascii_commands:
            send_ascii_command(com_port, ascii_command)

        for hex_command, wait_for_reply, delay_after_reply in hex_commands:
            while True:
                send_hex_command(com_port, hex_command, wait_for_reply, delay_after_reply)
                time.sleep(0.005)

                # Uncomment to exit loop
                # break

if __name__ == "__main__":
    main()
