from FPGA import *
from ascon_pcsn import *
import csv
import matplotlib.pyplot as plt
import serial
from time import sleep


# Load NeuroKit and other useful packages
import neurokit2 as nk
import numpy as np
import pandas as pd

port = "COM5" 
baudrate = 115200


# We have 181 points in each waveform
number_of_points = 181
X_axis = [k for k in range(0, number_of_points)]



# Variable globale pour choisir le nombre d'ECGs affichés
NUM_ECGS_DISPLAYED = 10
# Variable globale pour choisir le nombre d'ECGs utilisés pour le calcul du BPM
NUM_ECGS_FOR_BPM = 20


# -----      DEFINITION DES COMMADNDES      ------

# ---- Send encryption parameters over UART
# Key (L=0x4C): 128-bit (16 bytes), on a ajouté 4C au début
# Nonce (O=0x4F): 16-byte hexadecimal value, on a ajouté 4F au début
# Associated Data (B=0x42): 8 bytes + padding, on a ajouté 42 au début, et 80 00 a la fin
# Initiate encryption with the "go" (H=0x48) command.
# Retrieve Data
# Ciphertext (D=0x44): 181 bytes + 3 bytes of padding + OK response.
# Tag (U=0x55): 128-bit (16 bytes) + OK response.


KEY     = bytes.fromhex("8A55114D1CB6A9A2BE263D4D7AECAAFF")
NONCE   = bytes.fromhex("4ED0EC0B98C529B7C8CDDF37BCD0284A")
DA      = b"A to B"


FPGA_ACK = b'OK\n'
GO =    bytes.fromhex('47')
CIPHER =bytes.fromhex('43')
TAG =   bytes.fromhex('54')


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


def convert_hex_to_decimal(hex_string):
    return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]



if __name__ == "__main__":

    curves_int , curves_str = load_curves("./PC/waveform_example_ecg.csv")
    
    # ECG waveform (X=0x58): 181 bytes, on a ajouté 58 au début, et 80 00 00 a la fin 
    plaintext= bytes.fromhex('42'+ curves_str[0][0]+'800000')
    plaintext_a_la_main = bytes.fromhex('425A5B5B5A5A5A5A5A59554E4A4C4F545553515354565758575A5A595756595B5A5554545252504F4F4C4C4D4D4A49444447474644424341403B36383E4449494747464644434243454745444546474A494745484F58697C92AECEEDFFFFE3B47C471600041729363C3F3E40414141403F3F403F3E3B3A3B3E3D3E3C393C41464646454447464A4C4F4C505555524F5155595C5A595A5C5C5B5959575351504F4F53575A5C5A5B5D5E6060615F605F5E5A5857545252800000')
    print(plaintext_a_la_main)



    

    # ------------------ANCIEN CODE AVEC LE FPGA ------------------------
    # ----The provided bitstream does not accept lowercase letters.
    # ----All characters must be represented in hexadecimal (e.g., 'B' = 0x42).

    fpga = FPGA(port, baudrate)
    fpga.open_instrument()

    fpga.send_key(KEY)
    fpga.send_nonce(NONCE)
    fpga.send_associated_data(DA)
    fpga.send_waveform(plaintext_a_la_main)
    fpga.start_encryption()
    cipher = fpga.get_cipher()
    tag = fpga.get_tag()
    fpga.close_instrument()


    # AVEC FPGA_UART
    # fpga.serial_conn.write(KEY)
    # fpga.serial_conn.read(4)
    # fpga.serial_conn.write(NONCE)
    # fpga.serial_conn.read(4)
    # fpga.serial_conn.write(DA)
    # fpga.serial_conn.read(4)
    # fpga.serial_conn.write(plaintext)
    # fpga.serial_conn.read(4)

    # fpga.serial_conn.write(GO)
    # fpga.serial_conn.write(CIPHER)
    # tag = fpga.serial_conn.read(16)
    # print(tag)
    # fpga.serial_conn.write(TAG)
    # cyphertext = fpga.serial_conn.read(181)
    # print(cyphertext)






    # ser = serial.Serial(port, 115200, timeout=1)    

    # # On envvoie les données de chiffrement, et on lit les 'ok' du fpga
    # print("Sending Data to FPGA ...")
    # ser.write(key)
    # print("Key : ", ser.read(3))
    # ser.write(nonce)
    # print("Nonce : " , ser.read(3))
    # ser.write(a_data)
    # print("Ass. Data : " , ser.read(3))
    # ser.write(plaintext_a_la_main)
    # print("Plaintext : " , ser.read(3))
    # print("Sending commands to crypt with ASCON ...")

    # ser.write(Go)
    # print("Go : ", ser.read(3))
    # sleep(1)

    # ser.write(D)
    # tag = ser.read(16)
    # tag_hex = tag.hex()
    # print(tag_hex)
    # print(ser.read(3))

    # ser.write(U)
    # cyphertext = ser.read(181+3)
    # cyphertext_hex = cyphertext.hex()
    # print(cyphertext_hex)
    # print(ser.read(3))

    
    # ser.close()