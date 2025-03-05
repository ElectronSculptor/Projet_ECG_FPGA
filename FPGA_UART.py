# CREATION DATE 05/03/2025
# UART COMMUNICATION BETWEEN PC AND FPGA BOARD
# We gonna try to automatize that and add a class


import serial




class FPGA_UART:
    def __init__(self, port, baud_rate=115200, timeout=1):
        """
        Initialize the UART connection.
        :param port: Serial port name (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
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
        """Send a command to set the memory address."""
        if isinstance(address, int):
            self.serial_conn.write(f"SET_ADDR {address}\n".encode())
        else:
            print("Invalid address: Must be an integer.")

    def write_val_mem(self, value):
        """Write a value to the memory."""
        if isinstance(value, int):
            self.serial_conn.write(f"WRITE_MEM {value}\n".encode())
        else:
            print("Invalid value: Must be an integer.")

    def display_mem_vals_leds(self, value):
        """Send a command to display memory values on LEDs."""
        if isinstance(value, int):
            self.serial_conn.write(f"DISPLAY_LED {value}\n".encode())
        else:
            print("Invalid value: Must be an integer.")

    def read_mem_val(self):
        """Read a value from memory."""
        self.serial_conn.write(b"READ_MEM\n")
        response = self.serial_conn.readline().decode().strip()
        return response






"""
This module is responsible for implementing the class used to check object types.
It's implemented by the professor, Raphael VIERA.
"""

class CheckIf:
    """
    This class implements the methods responsible for checking object types
    """

    def __init__(self):
        pass

    @staticmethod
    def is_list(element):
        """
        Check if element is of type list.

        Args:
            - element: list

        Returns:
            - : bool
        """

        return isinstance(element, list)

    @staticmethod
    def is_set(element):
        """
        Check if element is of type set.

        Args:
            - element: set

        Returns:
            - : bool
        """

        return isinstance(element, set)

    @staticmethod
    def is_tuple(element):
        """
        Check if element is of type tuple.

        Args:
            - element: tuple

        Returns:
            - : bool
        """

        return isinstance(element, tuple)

    @staticmethod
    def is_string(element):
        """
        Check if element is of type string.

        Args:
            - element: str

        Returns:
            - : bool
        """

        return isinstance(element, str)

    @staticmethod
    def is_bool(element):
        """
        Check if element is of type bool.

        Args:
            - element: bool

        Returns:
            - : bool
        """

        try:
            if isinstance(element, bool):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def is_in_range(val, range):
        """
        Check if val is in range.

        Args:
            - val: float
            - range: list

        Returns:
            - : bool
        """

        try:
            if min(range) <= val <= max(range):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def is_hashable_type(obj):
        """
        Check if element is hashable.

        Args:
            - element: obj

        Returns:
            - : bool
        """

        import collections
        return isinstance(obj, collections.abc.Hashable)

    @staticmethod
    def is_value_in_enum(user_param_enum, user_param_value):
        try:
            get_verification_parameter = getattr(user_param_enum, user_param_value)
            temp = get_verification_parameter.value

            return True
        except:
            # exiting here because the parameter does not exist in the ENUM
            return False

    @staticmethod
    def is_number(to_check):
        """
        Check if element is of type number even if it's a string that can be converted to a number.

        Args:
            - to_check: str or int or float or bool

        Returns:
            - : bool
        """

        # int(False) = 0 but it is not a number.
        # 0 == False so checking if to_check is
        try:
            if isinstance(to_check, bool):
                return False
        except:
            pass

        try:
            float(to_check)
            return True
        except:  # ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(to_check)
            return True
        except:  # (TypeError, ValueError):
            pass

        return False
