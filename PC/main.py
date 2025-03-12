from FPGA_UART import *
from Check_if import *
from ascon_pcsn import *
import csv


def load_curves(file_name):
    Curves_List = []
    with open(file_name, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            Curves_List.append(row)
    return Curves_List



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
    # (TESTE ET CA MARCHE BIEN)
    # demo_aead("Ascon-128")
    # demo_hash("Ascon-Hash")


    # ------------------ON CHARGE LES COURBES .CSV---------------
    # (TESTE ET CA MARCHE BIEN)
    curves = load_curves("waveform_example_ecg.csv")
    print(curves)