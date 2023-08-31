import serial as pyserial
import time
import json

class SerialAPI:
    def __init__(self, baudrate=9600, timeout=1, ignore_ports=[]):
        self.baudrate = baudrate
        self.timeout = timeout
        self.ignore_ports = ignore_ports

    def detect_com_ports(self):
        com_ports = []
        for i in range(256):
            port_name = f"COM{i}"
            if port_name in self.ignore_ports:
                continue
            try:
                port = pyserial.Serial(port_name, baudrate=self.baudrate, timeout=self.timeout)
                port.close()
                com_ports.append(port_name)
            except pyserial.SerialException:
                pass
        return com_ports

    def send_hex_command(self, com_port, hex_command, wait_for_reply=False, delay_after_reply=0):
        ser = pyserial.Serial(com_port, baudrate=self.baudrate, timeout=self.timeout)
        hex_bytes = bytes.fromhex(hex_command.replace(" ", ""))
        ser.write(hex_bytes)
        time.sleep(0.005)

        if wait_for_reply:
            reply = ser.read_until()
            print(f"Received reply: {reply}")

            if delay_after_reply:
                time.sleep(delay_after_reply)
        ser.close()

    def send_ascii_command(self, com_port, ascii_command):
        ser = pyserial.Serial(com_port, baudrate=self.baudrate, timeout=self.timeout)
        data = ascii_command.encode()
        ser.write(data)
        time.sleep(0.5)
        ser.close()

# Sample code to use the SerialAPI
if __name__ == "__main__":
    api = SerialAPI(ignore_ports=["", ""])

    com_ports = api.detect_com_ports()
    if not com_ports:
        print("No COM ports detected")
    else:
        print(f"Detected COM ports: {com_ports}")

    # Suppose we have a JSON file commands.json with the commands
    # {
    #   "ascii_commands": ["ka 01 01\r"],
    #   "hex_commands": [
    #     {
    #       "command": "01 30 41 30 41 30 43 02 43 32 30 33 44 36 30 30 30 31 03 73 0D",
    #       "wait_for_reply": true,
    #       "delay_after_reply": 15
    #     }
    #   ]
    # }

    with open("commands.json", "r") as f:
        commands = json.load(f)

    for com_port in com_ports:
        for ascii_command in commands["ascii_commands"]:
            api.send_ascii_command(com_port, ascii_command)

        for hex_command_info in commands["hex_commands"]:
            hex_command = hex_command_info["command"]
            wait_for_reply = hex_command_info["wait_for_reply"]
            delay_after_reply = hex_command_info["delay_after_reply"]

            api.send_hex_command(com_port, hex_command, wait_for_reply, delay_after_reply)
