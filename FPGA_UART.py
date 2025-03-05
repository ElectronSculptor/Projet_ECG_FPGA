# CREATION DATE 05/03/2025
# UART COMMUNICATION BETWEEN PC AND FPGA BOARD
# We gonna try to automatize that and add a class

import serial

def int_to_bytes(value):
    """
    Transform an integer into a bytestring.
    Example: int_to_bytes(10) -> b'10'
    Example: int_to_bytes(2552256) -> b'2552256'
    :param value: Integer value
    :return: Bytestring

    """
    if isinstance(value, int):
        return bytes(f'{value:02}', 'utf-8')
    else:
        raise ValueError("Value must be an integer.")


class FPGA_UART:
    def __init__(self, port, baud_rate=115200, timeout=1):
        """
        Initialize the UART connection.
        :param port: Serial port name (e.g., 'COM3' on Windows))
        :param baud_rate: Communication speed
        :param timeout: Read timeout
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_conn = None

    def open_instrument(self):
        """Open the UART connection."""
        try:
            self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print("UART connection opened.")
        except serial.SerialException as e:
            print(f"Error opening UART: {e}")

    def close_instrument(self):
        """Close the UART connection."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("UART connection closed.")


    
    
    
    def set_memory_addr(self, address):
        """Send a command to set the memory address in bytestring format."""
        if isinstance(address, int):
            self.serial_conn.write(b'W' + int_to_bytes(address))
        else:
            print("Invalid address: Must be an integer.")

    def write_val_mem(self, value):
        """Write a value to the memory in bytestring format."""
        if isinstance(value, int):
            self.serial_conn.write(bytes([value]))
        else:
            print("Invalid value: Must be an integer.")

    def display_mem_vals_leds(self):
        """Send a command to display memory values on LEDs"""
        self.serial_conn.write(b'G')

    def read_mem_val(self):
        """Read a value from memory and return as a bytestring."""
        self.serial_conn.write(b"\x01")  # Example read command as a single byte
        response = self.serial_conn.read(1)  # Read single byte
        return response