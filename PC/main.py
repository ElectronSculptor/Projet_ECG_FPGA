from FPGA_UART import *
from Check_if import *
from ascon_pcsn import *


if __name__ == "__main__":
    # ------------------ANCIEN CODE AVEC LE FPGA ------------------------

    # fpga = FPGA_UART(port="COM16", baud_rate=115200, timeout=1)

    # fpga.open_instrument()
    # fpga.set_memory_addr(00)
    # fpga.write_val_mem(0xFA)
    # fpga.display_mem_vals_leds()
    
    # mem_val = fpga.read_mem_val()
    # print("Read memory value:", mem_val)
    
    # fpga.close_instrument()

    # ------------------DEMO SANS LE FPGA------------------------
    # demo_aead("Ascon-128")
    # demo_hash("Ascon-Hash")


    # ------------------ON CHARGE LES COURBES .CSV---------------
    curves = load_curves("waveform_example_ecg.csv")