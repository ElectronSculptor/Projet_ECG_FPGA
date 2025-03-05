from FPGA_UART import *


if __name__ == "__main__":
    # Example usage
    fpga = FPGA_UART(port="/dev/ttyUSB0", baud_rate=115200, timeout=1)
    fpga.open_instrument()
    fpga.set_memory_addr(0x10)
    fpga.write_val_mem(1234)
    fpga.display_mem_vals_leds(1234)
    mem_val = fpga.read_mem_val()
    print("Read memory value:", mem_val)
    fpga.close_instrument()
