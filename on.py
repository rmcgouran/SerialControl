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
    ser.write(hex_command.encode('latin-1')) # Send the bytes directly
    time.sleep(0.1) # Adjust as needed to meet the 100ms byte interval requirement

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
    """Detects all connected COM ports and sends a list of HEX commands to all attached ports, then a list of ASCII commands."""
    com_ports = detect_com_ports()
    hex_commands = [
        ("\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x31\x03\x73\x0D", True, 15), # Power On example, adjust as needed
        # Add more hex_commands as needed, with appropriate wait_for_reply and delay_after_reply values
    ]
    ascii_commands = [
        "ka 01 01\r",
    ]
    for com_port in com_ports:
        for hex_command, wait_for_reply, delay_after_reply in hex_commands:
            send_hex_command(com_port, hex_command, wait_for_reply, delay_after_reply)
            print(hex_command.encode('latin-1').hex())

        for ascii_command in ascii_commands:
            send_ascii_command(com_port, ascii_command)

if __name__ == "__main__":
    main()



