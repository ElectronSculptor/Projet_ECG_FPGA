// File: Ascon_tb.sv
// Written by: Gevorg ishkhanyan
// Date: 03/03/2025


`timescale 1ns / 1ps
// Testbecnh ASCON 
import ascon_pack::*;


// We're gonna implement a FSM to control the ASCON module


module ascon_tb();
    // inputs
    logic         clock_s;
    logic         reset_s;
    logic         init_s;
    logic         associate_data_s; //0: plain text; 1: DA
    logic         finalisation_s;
    logic [ 63:0] data_s;
    logic         data_valid_s;
    logic [127:0] key_s;
    logic [127:0] nonce_s;
    // outputs
    logic         end_associate_s;
    logic [ 63:0] cipher_s;
    logic         cipher_valid_s;
    logic [127:0] tag_s;
    logic         end_tag_s;
    logic         end_initialisation_s;
    logic         end_cipher_s;

    // other signals
    logic [1447:0] data_i_s;
    assign data_i_s = 1448'h5A_5B_5B_5A_5A_5A_5A_5A_59_55_4E_4A_4C_4F_54_55_53_51_53_54_56_57_58_57_5A_5A_59_57_56_59_5B_5A_55_54_54_52_52_50_4F_4F_4C_4C_4D_4D_4A_49_44_44_47_47_46_44_42_43_41_40_3B_36_38_3E_44_49_49_47_47_46_46_44_43_42_43_45_47_45_44_45_46_47_4A_49_47_45_48_4F_58_69_7C_92_AE_CE_ED_FF_FF_E3_B4_7C_47_16_00_04_17_29_36_3C_3F_3E_40_41_41_41_40_3F_3F_40_3F_3E_3B_3A_3B_3E_3D_3E_3C_39_3C_41_46_46_46_45_44_47_46_4A_4C_4F_4C_50_55_55_52_4F_51_55_59_5C_5A_59_5A_5C_5C_5B_59_59_57_53_51_50_4F_4F_53_57_5A_5C_5A_5B_5D_5E_60_60_61_5F_60_5F_5E_5A_58_57_54_52_52;
    assign key_s = 128'h8A_55_11_4D_1C_B6_A9_A2_BE_26_3D_4D_7A_EC_AA_FF;
    assign nonce_s = 128'h4E_D0_EC_0B_98_C5_29_B7_C8_CD_DF_37_BC_D0_28_4A;


    // Signal Wiring
   ascon DUT (
				.clock_i(clock_s),
				.reset_i(reset_s),
				.init_i(init_s),
                .associate_data_i(associate_data_s), //0: plain text; 1: DA
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
        reset,
        init,
        wait_end_initialisation,
        wait_end_associate,
        pt_set_data,
        wait_cipher_valid,
        pt_get_cipher,
        pt_wait_end_cipher,
        wait_cipher_valid,
        wait_end_tag,
        get_tag,
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