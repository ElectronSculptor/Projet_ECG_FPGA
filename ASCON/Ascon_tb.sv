// File: Ascon_tb.sv
// Written by: Gevorg ishkhanyan
// Date: 03/03/2025


`timescale 1ns / 1ps
// Testbecnh ASCON 
import ascon_pack::*;


module ascon_tb();
    // inputs, I added "_s" to all signals
    logic         clock_s,
    logic         reset_s,
    logic         init_s,
    logic         associate_data_s,
    logic         finalisation_s,
    logic [ 63:0] data_s,
    logic         data_valid_s,
    // Given key and nonce
    logic [127:0] key_s = 128'h8A55114D1CB6A9A2BE263D4D7AECAAFF,
    logic [127:0] nonce_s = 128'h4ED0EC0B98C529B7C8CDDF37BCD0284A,

    // outputs
    logic         end_associate_s,
    logic [ 63:0] cipher_s,
    logic         cipher_valid_s,
    logic [127:0] tag_s,
    logic         end_tag_s,
    logic         end_initialisation_s,
    logic         end_cipher_s


    // Signal Wiring
   ascon DUT (
				.clock_i(clock_s),
				.reset_i(reset_s),
				.init_i(init_s),
                .associate_data_i(associate_data_s),
                .finalisation_i(finalisation_s),
                .data_i(data_s),
                .data_valid_i(data_valid_s),
                .key_i(key_s),
                .nonce_i(nonce_s),
                .end_associate_o(end_associate_s),
                .cipher_o(cipher_s),
                .cipher_valid_o(cipher_valid_s),
                .tag_o(tag_s),
                .end_tag_o(end_tag_s),
                .end_initialisation_o(end_initialisation_s),
                .end_cipher_o(end_cipher_s)
    );

    // Clock generation
    always  begin
       #10;
       assign  clock_s = ~clock_s;  
    end


    // Enumeration for the state machine
    typedef enum {
        idle,
        initialisation,
        associate_data,
        finalisation
    } State_t;

    // Previous and current state
    State_t Ep, Ef

    always_ff @(posedge clock_s, negedge reset_s) begin
    if (reset_s == 1'b0) begin
      Ep <= idle;
        end else begin
        Ep <= Ef;
        end
    end
   


    always_comb begin
    case (Ep)
      idle:



      default: Ef = idle;
    endcase
  end



endmodule: ascon_tb