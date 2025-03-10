`timescale 1ns / 1ps

module top_level

  import uart_pkg::*;
(
    input  logic       clock_i,  //main clock
    input  logic       reset_i,  //asynchronous reset active low
    input  logic       Rx_i,     //RX to RS232
    input  logic [2:0] Baud_i,   //baud selection
    output logic       Tx_o,     //Tx to RS 232
    output logic [2:0] Baud_o,
    output logic       RTS_o
);

  logic RXErr_s;
  logic RXRdy_s;
  logic TxBusy_s;
  logic rdata_ld_s;
  logic [NDBits-1:0] rdata_s;
  logic [NDBits-1:0] Dout_s;
  logic clock_s;
  logic resetb_s;

  assign Baud_o   = ~Baud_i;
  assign resetb_s = ~reset_i;
  assign RTS_o    = RXRdy_s;  //from Nathan improve UART behavior (pin 1sur USB SERIAL)

  //internal signals for UART part
  logic [127:0] tag_s;
  logic [1471:0] wave_to_send_s;
  logic cipherRdy_s;
  logic [127:0] key_s;
  logic [127:0] nonce_s;
  logic [63:0] ad_s;
  logic [1471:0] wave_received_s;
  logic start_ascon_s;
  logic init_cpt_mux_s;
  logic en_cpt_mux_s;
  logic en_reg_ascon_s;
  logic cipher_valid_s;
  //internal signals for Ascon part
  //signals
  logic associate_data_s;
  logic finalisation_s;
  logic data_valid_s;
  logic end_associate_s;
  logic end_tag_s;
  logic end_initialisation_s;
  logic end_cipher_s;

  //mux for injected data in ascon
  logic [63:0] data_s, cipher_s;
  logic [4:0] cpt_s;  //cpt 5 bits
  logic [0:23][63:0] wave_s;  //1472
  //logic [0:22][63:0] wave_o_s;  //1472+64 packed


  assign clock_s = clock_i;
 

  uart_core uart_core_0 (
      .clock_i(clock_s),
      .resetb_i(resetb_s),
      .Din_i(rdata_s),
      .LD_i(rdata_ld_s),
      .Rx_i(Rx_i),
      .Baud_i(Baud_i),
      .RXErr_o(RXErr_s),
      .RXRdy_o(RXRdy_s),
      .Dout_o(Dout_s),
      .Tx_o(Tx_o),
      .TxBusy_o(TxBusy_s)
  );

  fsm_uart fsm_uart_0 (
      .clock_i(clock_s),
      .resetb_i(resetb_s),
      .RXErr_i(RXErr_s),
      .RXRdy_i(RXRdy_s),
      .TxBusy_i(TxBusy_s),
      .RxData_i(Dout_s),
      .Tag_i(tag_s),
      .Cipher_i(wave_to_send_s),
      .CipherRdy_i(end_tag_s),
      .TxByte_o(rdata_s),
      .Key_o(key_s),
      .Nonce_o(nonce_s),
      .Ad_o(ad_s),
      .Wave_o(wave_received_s),
      .Start_ascon_o(start_ascon_s),
      .Load_o(rdata_ld_s)
  );

  //instance de ascon
  
  ascon ascon_0 (
      .clock_i(clock_s),
      .resetb_i(resetb_s),
      .start_i(start_ascon_s),
      .key_i(key_s),
      .nonce_i(nonce_s),
      .data_i(data_s),
      .cipher_o(cipher_s),
      .cipher_valid_o(cipher_valid_s),
      .tag_o(tag_s),
      .end_tag_o(end_tag_s),
      .end_initialisation_o(end_initialisation_s),
      .end_cipher_o(end_cipher_s),
      .init_o(init_cpt_mux_s),
      .associate_data_o(associate_data_s),
      .finalisation_o(finalisation_s),
      .data_valid_o(data_valid_s),
      .end_associate_o(end_associate_s)
  );

  //instanciate drive ascon here
  
  fsm_ascon fsm_ascon_0 (
      .clock_i(clock_s),
      .reset_i(resetb_s),
      .start_i(start_ascon_s),
      .data_i(wave_received_s),
      .end_associate_i(end_associate_s),
      .cipher_i(cipher_s),
      .cipher_valid_i(cipher_valid_s),
      .tag_i(tag_s),
      .end_tag_i(end_tag_s),
      .end_initialisation_i(end_initialisation_s),
      .end_cipher_i(end_cipher_s),
      .init_o(init_cpt_mux_s),
      .associate_data_o(associate_data_s),
      .finalisation_o(finalisation_s),
      .data_o(data_s),
      .data_valid_o(data_valid_s),
      .key_o(key_s),
      .nonce_o(nonce_s)
  );
  

  //counter to select the correct word from wavereceived and drive it to data_s


  assign data_s     = wave_s[cpt_s];
  assign en_reg_ascon_s = cipher_valid_s;
//register to store cipher result 8 bytes
  ascon_reg u_ascon_reg (
      .clock_i (clock_s),
      //main clock
      .resetb_i(resetb_s),
      //asynchronous reset active low
      .data_i  (cipher_s),
      .en_i    (en_reg_ascon_s),
      .init_i  (init_cpt_mux_s),
      //wave register storing 8 bytes by the right hand side. (23*64bits)
      .wave_o  (wave_to_send_s)   //wave_o_s
  );

endmodule : top_level
