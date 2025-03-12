from FPGA_UART import *
from Check_if import *
from ascon_pcsn import *
import csv
import matplotlib.pyplot as plt

# Load NeuroKit and other useful packages
import neurokit2 as nk
import numpy as np
import pandas as pd


# We have 181 points in each waveform
number_of_points = 181
X_axis = [k for k in range(0, number_of_points)]




# Key
key_hexa="8A55114D1CB6A9A2BE263D4D7AECAAFF"
# Nonce
nonce_hexa="4ED0EC0B98C529B7C8CDDF37BCD0284A"

key = bytes.fromhex(key_hexa)
nonce = bytes.fromhex(nonce_hexa)
associateddata = b"A to B"




def load_curves(file_path):
    # On va charger les données dans 2 listes
    # Une qui sera en int pour plot avant ascon
    # Et une qui sera en string pour envoyer a ascon
    curves_int = []
    curves_str = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            curve = []
            for value in row:
                # Split the hex string into pairs of characters and convert to decimal
                curve.extend([int(value[i:i+2], 16) for i in range(0, len(value), 2)])
            curves_int.append(curve)
            curves_str.append(row)
    return curves_int, curves_str



def plot_curves(curves):
    for i, curve in enumerate(curves):
        plt.plot(curve, label=f'Waveform {i+1}')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title('ECG Waveforms')
    plt.legend()
    plt.show()

def convert_hex_to_decimal(hex_string):
    return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]



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
    
    curves_int , curves_str = load_curves("waveform_example_ecg.csv")
    #print(curves)

    for i in range(3):
        
        plaintext= bytes.fromhex(curves_str[i][0])

        # On a ici le cipher et le tag qui est sur les 16 derniers bits
        Cipher = ascon_encrypt(key, nonce, associateddata, plaintext, variant="Ascon-128")
        decrypted_plaintext = ascon_decrypt(key, nonce, associateddata, Cipher, variant="Ascon-128")

        decrypted_plaintext_decimal = convert_hex_to_decimal(decrypted_plaintext.hex())
        
        #demo_print([("Cipher", Cipher), ("Plaintext", decrypted_plaintext)])

        # plt.plot(X_axis,curves_int[i], label=f'Waveform {i+1}')
        # plt.plot(X_axis,decrypted_plaintext_decimal, label=f'Waveform decrypted{i+1}')
        # plt.xlabel('Sample')
        # plt.ylabel('Amplitude')
        # plt.title('ECG Waveforms')
        # plt.legend()
        


        ecg = nk.ecg_simulate(duration=10, noise=0.01, heart_rate=70)
        print(ecg) #numpy.ndarray
        decrypted_plaintext_array = np.array(decrypted_plaintext_decimal)


        # Extract R-peaks locations
        _, rpeaks = nk.ecg_peaks(decrypted_plaintext_array, sampling_rate=181)
        # Visualize R-peaks in ECG signal
        plot = nk.events_plot(rpeaks['ECG_R_Peaks'], decrypted_plaintext_array)
        plt.show()

        # Delineate the ECG signal and visualizing all peaks of ECG complexes
        #_, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=1000, method="peak", show=True, show_type='peaks')





