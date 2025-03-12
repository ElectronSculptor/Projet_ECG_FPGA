from FPGA_UART import *
from Check_if import *
from ascon_pcsn import *
import csv

import matplotlib.pyplot as plt

# We have 181 points in each waveform
number_of_points = 181
X_axis = [k for k in range(0, number_of_points)]


def load_curves(file_path):
    curves = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            curve = []
            for value in row:
                # Split the hex string into pairs of characters and convert to decimal
                curve.extend([int(value[i:i+2], 16) for i in range(0, len(value), 2)])
            curves.append(curve)
    return curves



def plot_curves(curves):
    for i, curve in enumerate(curves):
        plt.plot(curve, label=f'Waveform {i+1}')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title('ECG Waveforms')
    plt.legend()
    plt.show()



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
    
    #print(curves)

    plt.plot(X_axis,curves[18], label=f'Waveform {1}')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title('ECG Waveforms')
    plt.legend()
    plt.show()