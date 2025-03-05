from FPGA_UART import *
from Check_if import *


if __name__ == "__main__":
    # Example usage
    fpga = FPGA_UART(port="COM16", baud_rate=115200, timeout=1)

    fpga.open_instrument()
    fpga.set_memory_addr(0x00)
    fpga.write_val_mem(0x55)
    fpga.display_mem_vals_leds(0xAA)
    
    mem_val = fpga.read_mem_val()
    print("Read memory value:", mem_val)
    
    fpga.close_instrument()
