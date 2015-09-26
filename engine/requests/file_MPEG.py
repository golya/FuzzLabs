# =============================================================================
# Basic MPEG-1 Descriptor
# This file is part of the FuzzLabs Fuzzing Framework
# Author: FuzzLabs
#
# Based on:
#     http://andrewduncan.net/mpeg/mpeg-1.html
#
# NOTES: THIS NEEDS FURTHER PARSING AND IMPROVEMENT
#
# =============================================================================

from sulley import *

PACKET_START_CODE = "\x00\x00\x01"

s_initialize("MPEG")

# -----------------------------------------------------------------------------
# MPEG-1 Pack Header
# -----------------------------------------------------------------------------

if s_block_start("MPEG_PS_PH"):				# Program Stream Packet Header

    # -------------------------------------------------------------------------
    # Offset: 0x00
    # Value:  0x000001BA
    # -------------------------------------------------------------------------

    s_binary("\x00\x00")				# First 2 bytes of the Start Code
							# These are not used at all so
							# they will be static.
    s_byte(0x01, full_range=True)			# The used part of the Start Code
    s_byte(0xBA, full_range=True)			# Stream ID

    # -------------------------------------------------------------------------
    # System Clock Reference (SCR)
    # Offset: 0x04
    # Value:  0x2100010001
    # -------------------------------------------------------------------------

    s_bitfield(0x2100010001, length=5, fuzzable=True, fields=[
        {"start": 0,   "end": 4,   "name": "SCR_MARKER_1"},
        {"start": 4,   "end": 7,   "name": "SCR_SCR_1",      "fuzzable": True},
        {"start": 7,   "end": 8,   "name": "SCR_MARKER_2"},
        {"start": 8,   "end": 23,  "name": "SCR_SCR_2",      "fuzzable": True},
        {"start": 23,  "end": 24,  "name": "SCR_MARKER_3",   "fuzzable": True},
        {"start": 24,  "end": 39,  "name": "SCR_SCR_3",      "fuzzable": True},
        {"start": 39,  "end": 40,  "name": "SCR_MARKER_4"}
    ], name="MPEG_PACK_HEADER_SCR")

    # -------------------------------------------------------------------------
    # Multiplex Rate (MPR)
    # Offset: 0x09
    # Value:  0x80B8C5
    # -------------------------------------------------------------------------

    s_bitfield(0x80B8C5, length=3, fuzzable=True, fields=[
        {"start": 0,   "end": 1,   "name": "SCR_MARKER_5"},
        {"start": 1,   "end": 23,  "name": "SCR_MPR_4",      "fuzzable": True},
        {"start": 23,  "end": 24,  "name": "SCR_MARKER_6"}	
    ], name="MPEG_PACK_HEADER_MPR")

s_block_end("MPEG_PS_PH")

# -----------------------------------------------------------------------------
# MPEG-1 System Header
# -----------------------------------------------------------------------------

if s_block_start("MPEG_PS_SH"): 

    # -------------------------------------------------------------------------
    # Offset: 0x0C
    # Value:  0x000001BB
    # -------------------------------------------------------------------------

    s_binary("\x00\x00")                                # First 2 bytes of the Start Code
                                                        # These are not used at all so
                                                        # they will be static.
    s_byte(0x01)                                        # The used part of the Start Code
    s_byte(0xBB, full_range=True)                       # Stream ID

    # -------------------------------------------------------------------------
    # Offset: 0x10
    # -------------------------------------------------------------------------

    s_size("MPEG_PS_SH_DATA", length=2, endian=">", fuzzable=True)
    
    if s_block_start("MPEG_PS_SH_DATA"):

        # ---------------------------------------------------------------------
        # Rate Bound
        # Offset: 0x12
        # ---------------------------------------------------------------------

        s_bitfield(0x80B8C5, length=3, fuzzable=True, fields=[
            {"start": 0,   "end": 1,   "name": "RBM_MARKER_1"},
            {"start": 1,   "end": 23,  "name": "SH_RB",    "fuzzable": True},
            {"start": 23,  "end": 24,  "name": "RBM_MARKER_2"}
        ], name="MPEG_SYSTEM_HEADER_RATE_BOUND")

        # ---------------------------------------------------------------------
        # Audio and Video Details / Info
        # Offset: 0x15
        # ---------------------------------------------------------------------

        s_bitfield(0x0021FF, length=3, fuzzable=True, fields=[
            {"start": 0,   "end": 6,   "name": "SH_AUDIO_BOUND",       "fuzzable": True},
            {"start": 6,   "end": 7,   "name": "SH_AUDIO_FIX_BITRATE", "fuzzable": True},
            {"start": 7,   "end": 8,   "name": "SH_AUDIO_CSPS_FLAG",   "fuzzable": True},
            {"start": 8,   "end": 9,   "name": "SH_SYSAUD_LCK_FLAG",   "fuzzable": True},
            {"start": 9,   "end": 10,  "name": "SH_SYSVID_LCK_FLAG",   "fuzzable": True},
            {"start": 10,  "end": 11,  "name": "SH_AV_MARKER_1"},
            {"start": 11,  "end": 16,  "name": "SH_VIDEO_BOUND",       "fuzzable": True},
            {"start": 16,  "end": 24,  "name": "SH_AV_RESERVED",       "fuzzable": True}
        ], name="MPEG_SYSTEM_HEADER_AV")

        # ---------------------------------------------------------------------
        # Misc
        # Offset: 0x18
        # ---------------------------------------------------------------------

        s_bitfield(0xE0E0E6, length=3, fuzzable=True, fields=[
            {"start": 0,   "end": 1,   "name": "SH_MISC_SID_1"},
            {"start": 1,   "end": 3,   "name": "SH_MISC_SID_2",        "fuzzable": True},
            {"start": 3,   "end": 8,   "name": "SH_MISC_SID_3",        "fuzzable": True},
            {"start": 8,   "end": 10,  "name": "SH_MISC_ASET_1"},
            {"start": 10,  "end": 11,  "name": "SH_MISC_SBBS",         "fuzzable": True},
            {"start": 11,  "end": 24,  "name": "SH_MISC_STD_BUFSB",    "fuzzable": True},
        ], name="MPEG_SYSTEM_HEADER_MISC")

    s_block_end("MPEG_PS_SH_DATA")

s_block_end("MPEG_PS_SH")

# -----------------------------------------------------------------------------
# MPEG-1 Packet, Video Stream
# -----------------------------------------------------------------------------

if s_block_start("MPEG_PS_P_1"): 
    s_string(PACKET_START_CODE)
    s_byte(0xE0, full_range=True)

    s_size("MPEG_PS_P_1_DATA", length=2, endian=">", fuzzable=True)

    if s_block_start("MPEG_PS_P_1_DATA"): 

        s_bitfield(0x31, length=1, fuzzable=True, fields=[
            {"start": 0,   "end": 2,   "name": "F_P1D_FIX_1"},
            {"start": 2,   "end": 3,   "name": "F_P1D_PTS",         "fuzzable": True},
            {"start": 3,   "end": 4,   "name": "F_P1D_DTS",         "fuzzable": True},
            {"start": 4,   "end": 7,   "name": "F_P1D_PTS_1",       "fuzzable": True},
            {"start": 7,   "end": 8,   "name": "F_P1D_MARKER_1",    "fuzzable": True}
        ], name="MPEG_P1D_PTS")

        s_bitfield(0x0003, length=2, fuzzable=True, fields=[
            {"start": 0,   "end": 15,   "name": "F_P1D_PTS_2",      "fuzzable": True},
            {"start": 15,  "end": 16,   "name": "F_P1D_MARKER_2",   "fuzzable": True}
        ], name="MPEG_P1D_PTS_1")

        s_bitfield(0x7CDD, length=2, fuzzable=True, fields=[
            {"start": 0,   "end": 15,   "name": "F_P1D_PTS_3",      "fuzzable": True},
            {"start": 15,  "end": 16,   "name": "F_P1D_MARKER_3"}
        ], name="MPEG_P1D_PTS_2")

        s_bitfield(0x11, length=1, fuzzable=True, fields=[
            {"start": 0,   "end": 4,   "name": "F_P1D_FIX_2"},
            {"start": 4,   "end": 7,   "name": "F_P1D_DTS",         "fuzzable": True},
            {"start": 7,   "end": 8,   "name": "F_P1D_MARKER_4"}
        ], name="MPEG_P1D_DTS")

        s_bitfield(0x0003, length=2, fuzzable=True, fields=[
            {"start": 0,   "end": 15,   "name": "F_P1D_DTS_2",      "fuzzable": True},
            {"start": 15,  "end": 16,   "name": "F_P1D_MARKER_5",   "fuzzable": True}
        ], name="MPEG_P1D_DTS_1")

        s_bitfield(0x5F91, length=2, fuzzable=True, fields=[
            {"start": 0,   "end": 15,   "name": "F_P1D_DTS_3",      "fuzzable": True},
            {"start": 15,  "end": 16,   "name": "F_P1D_MARKER_6"}
        ], name="MPEG_P1D_DTS_2")

        # ---------------------------------------------------------------------
        # Video sequence - 1
        # ---------------------------------------------------------------------

        if s_block_start("MPEG_PS_P_1_DATA_VSEQ_1"):
            s_binary("\x00\x00\x01")                    # Start Code
            s_byte(0xB3, full_range=True)               # Stream ID

            # Horizontal and Vertical size, 3 bytes

            s_bitfield(0x014014, length=3, fuzzable=True, fields=[
                {"start": 0,   "end": 12,   "name": "VSEQ_1_HSIZE",  "fuzzable": True},
                {"start": 12,   "end": 24,  "name": "VSEQ_1_VSIZE",  "fuzzable": True},
            ], name="MPEG_PS_P_1_DATA_VSEQ_1_VHSIZE")

            # Pixel aspect ratio and picture rate

            s_bitfield(0x12, length=1, fuzzable=True, fields=[
                {"start": 0,   "end": 4,    "name": "VSEQ_1_PIXAR",  "fuzzable": True},
                {"start": 4,   "end": 8,    "name": "VSEQ_1_PICRA",  "fuzzable": True},
            ], name="MPEG_PS_P_1_DATA_VSEQ_1_PARPR")

            # Load intra Q matrix case (VSEQ_1_LOADQ) is not covered as there is no
            # decent doc. and the one I was working with was pretty confusing at this
            # point. Also, the sample file does not have the bit set.

            s_bitfield(0x15F92380, length=4, fuzzable=True, fields=[
                {"start": 0,   "end": 18,    "name": "VSEQ_1_BITRT",  "fuzzable": True},
                {"start": 18,  "end": 19,    "name": "VSEQ_1_MARK1",  "fuzzable": True},
                {"start": 19,  "end": 29,    "name": "VSEQ_1_YBYBS",  "fuzzable": True},
                {"start": 29,  "end": 30,    "name": "VSEQ_1_CONST",  "fuzzable": True},
                {"start": 30,  "end": 31,    "name": "VSEQ_1_LOADQ",  "fuzzable": True},
                {"start": 31,  "end": 32,    "name": "VSEQ_1_UNKNW",  "fuzzable": True}
            ], name="MPEG_PS_P_1_DATA_VSEQ_1_BRBS")

            # -----------------------------------------------------------------
            # Group of Pictures
            # -----------------------------------------------------------------

            if s_block_start("MPEG_PS_P_1_DATA_GOP"):

                s_binary("\x00\x00\x01")
                s_byte(0xB8, full_range=True)

                s_bitfield(0x00080000, length=4, fuzzable=True, fields=[
                    {"start": 0,   "end": 1,    "name": "GOP_DROPF",  "fuzzable": True},
                    {"start": 1,   "end": 6,    "name": "GOP_HOURS",  "fuzzable": True},
                    {"start": 6,   "end": 12,   "name": "GOP_MINS",   "fuzzable": True},
                    {"start": 12,  "end": 13,   "name": "GOP_MARK1",  "fuzzable": True},
                    {"start": 13,  "end": 19,   "name": "GOP_SECS",   "fuzzable": True},
                    {"start": 19,  "end": 25,   "name": "GOP_PICS",   "fuzzable": True},
                    {"start": 25,  "end": 26,   "name": "GOP_CLOSE",  "fuzzable": True},
                    {"start": 26,  "end": 27,   "name": "GOP_BRKLN",  "fuzzable": True},
                    {"start": 27,  "end": 32,   "name": "GOP_WHTVR",  "fuzzable": True}
                ], name="MPEG_PS_P_1_DATA_GOP_DSC")

                # -----------------------------------------------------------------
                # Picture
                # -----------------------------------------------------------------

                s_string("\x00\x00\x01")
                s_byte(0x00, full_range=True)

                s_binary([
                    0x00, 0x0F,
                    0xFF, 0xF8, 0x00, 0x00, 0x01, 0x01, 0x13, 0xF0, 0xD4, 0x94, 0x85, 0xC9,
                    0x98, 0x34, 0xA0, 0x0B, 0x4A, 0x03, 0x24, 0xC7, 0x01, 0x49, 0x4F, 0xF0,
                    0xD4, 0x1B, 0x9F, 0x37, 0xCF, 0x8D, 0xD6, 0x90, 0x18, 0x00, 0x3E, 0x21,
                    0x00, 0x60, 0x03, 0xB0, 0x10, 0xF0, 0x1D, 0x0D, 0xC4, 0x20, 0xD2, 0x6A,
                    0x79, 0x31, 0x09, 0x4A, 0x53, 0xF1, 0x43, 0x78, 0xC7, 0x1B, 0xFA, 0xD9,
                    0x9E, 0x22, 0xE8, 0xA5, 0x29, 0x11, 0x72, 0x94, 0xA4, 0x45, 0xCA, 0x52,
                    0x91, 0x10, 0x00, 0x00, 0x01, 0x00, 0x00, 0x57, 0xFF, 0xF8, 0x80, 0x00,
                    0x00, 0x01, 0x01, 0x12, 0xCC, 0x03, 0x83, 0x4D, 0x22, 0xEF, 0x8C, 0x80,
                    0x3D, 0x53, 0x91, 0x38, 0x99, 0x1C, 0x00, 0x00, 0x01, 0x00, 0x00, 0x97,
                    0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0xCC, 0x0E, 0xE0, 0x0F,
                    0x60, 0x60, 0xFF, 0x91, 0xC0, 0x00, 0x00, 0x01, 0x00, 0x00, 0xD7, 0xFF,
                    0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0xE0, 0x36, 0x80, 0xC8, 0xE0,
                    0x00, 0x00, 0x01, 0x00, 0x01, 0x17, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                    0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x01, 0x57, 0xFF, 0xF8,
                    0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00,
                    0x01, 0x97, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70,
                    0x00, 0x00, 0x01, 0x00, 0x01, 0xD7, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                    0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x02, 0x17, 0xFF, 0xF8,
                    0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00,
                    0x02, 0x57, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70,
                    0x00, 0x00, 0x01, 0x00, 0x02, 0x97, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                    0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x02, 0xD7, 0xFF, 0xF8,
                    0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00,
                    0x03, 0x17, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70,
                    0x00, 0x00, 0x01, 0x00, 0x03, 0x57, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                    0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x03, 0x97, 0xFF, 0xF8,
                    0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00,
                    0x03, 0xD7, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70,
                    0x00, 0x00, 0x01, 0x00, 0x04, 0x17, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                    0x01, 0x12, 0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x04, 0x57, 0xFF, 0xF8,
                    0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0x74, 0x70
                ])

            s_block_end("MPEG_PS_P_1_DATA_GOP")

        s_block_end("MPEG_PS_P_1_DATA_VSEQ_1")

        # ---------------------------------------------------------------------
        # Video sequence - 2
        # ---------------------------------------------------------------------

        if s_block_start("MPEG_PS_P_1_DATA_VSEQ_2"):
            s_binary(PACKET_START_CODE)
            s_byte(0xB3, full_range=True)               # Stream ID

            s_binary([
                0x01, 0x40, 0x14, 0x12, 0x15, 0xF9, 0x23, 0x80,
                0x00, 0x00, 0x01, 0xB8, 0x00, 0x08, 0x09, 0x00,
                0x00, 0x00, 0x01, 0x00, 0x00, 0x0F, 0xFF, 0xF8,
                0x00, 0x00, 0x01, 0x01, 0x13, 0xF0, 0xD4, 0x94,
                0x85, 0xC9, 0x98, 0x34, 0xA0, 0x0B, 0x4A, 0x03,
                0x24, 0xC7, 0x01, 0x49, 0x4F, 0xF0, 0xD4, 0x1B,
                0x9F, 0x37, 0xCF, 0x8D, 0xD6, 0x90, 0x18, 0x00,
                0x3E, 0x21, 0x00, 0x60, 0x03, 0xB0, 0x10, 0xF0,
                0x1D, 0x0D, 0xC4, 0x20, 0xD2, 0x6A, 0x79, 0x31,
                0x09, 0x4A, 0x53, 0xF1, 0x43, 0x78, 0xC7, 0x1B,
                0xFA, 0xD9, 0x9E, 0x22, 0xE8, 0xA5, 0x29, 0x11,
                0x72, 0x94, 0xA4, 0x45, 0xCA, 0x52, 0x91, 0x10,
                0x00, 0x00, 0x01, 0x00, 0x00, 0x57, 0xFF, 0xF8,
                0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0xCC, 0x03,
                0x83, 0x4D, 0x22, 0xEF, 0x8C, 0x80, 0x3D, 0x53,
                0x91, 0x38, 0x99, 0x1C, 0x00, 0x00, 0x01, 0x00,
                0x00, 0x97, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                0x01, 0x12, 0xCC, 0x0E, 0xE0, 0x0F, 0x60, 0x60,
                0xFF, 0x91, 0xC0, 0x00, 0x00, 0x01, 0x00, 0x00,
                0xD7, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01,
                0x12, 0xE0, 0x36, 0x80, 0xC8, 0xE0, 0x00, 0x00,
                0x01, 0x00, 0x01, 0x17, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x01, 0x57, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x01, 0x97, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x01, 0xD7, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x02, 0x17, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x02, 0x57, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x02, 0x97, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x02, 0xD7, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x03, 0x17, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x03, 0x57, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x03, 0x97, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x03, 0xD7, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x04, 0x17, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70, 0x00, 0x00,
                0x01, 0x00, 0x04, 0x57, 0xFF, 0xF8, 0x80, 0x00,
                0x00, 0x01, 0x01, 0x12, 0x74, 0x70
            ])
        s_block_end("MPEG_PS_P_1_DATA_VSEQ_2")

        # ---------------------------------------------------------------------
        # Video sequence - 3
        # ---------------------------------------------------------------------

        if s_block_start("MPEG_PS_P_1_DATA_VSEQ_3"):
            s_binary([
                0x00, 0x00, 0x01, 0xB3, 0x01, 0x40, 0x14, 0x12,
                0x15, 0xF9, 0x23, 0x80, 0x00, 0x00, 0x01, 0xB8,
                0x00, 0x08, 0x26, 0x00, 0x00, 0x00, 0x01, 0x00,
                0x00, 0x0F, 0xFF, 0xF8, 0x00, 0x00, 0x01, 0x01,
                0x13, 0xF0, 0xD4, 0x94, 0x85, 0xC9, 0x98, 0x34,
                0xA0, 0x0B, 0x4A, 0x03, 0x24, 0xC7, 0x01, 0x49,
                0x4F, 0xF0, 0xD4, 0x1B, 0x9F, 0x37, 0xCF, 0x8D,
                0xD6, 0x90, 0x18, 0x00, 0x3E, 0x21, 0x00, 0x60,
                0x03, 0xB0, 0x10, 0xF0, 0x1D, 0x0D, 0xC4, 0x20,
                0xD2, 0x6A, 0x79, 0x31, 0x09, 0x4A, 0x53, 0xF1,
                0x43, 0x78, 0xC7, 0x1B, 0xFA, 0xD9, 0x9E, 0x22,
                0xE8, 0xA5, 0x29, 0x11, 0x72, 0x94, 0xA4, 0x45,
                0xCA, 0x52, 0x91, 0x10, 0x00, 0x00, 0x01, 0x00,
                0x00, 0x57, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                0x01, 0x12, 0xCC, 0x03, 0x83, 0x4D, 0x22, 0xEF,
                0x8C, 0x80, 0x3D, 0x53, 0x91, 0x38, 0x99, 0x1C,
                0x00, 0x00, 0x01, 0x00, 0x00, 0x97, 0xFF, 0xF8,
                0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0xCC, 0x0E,
                0xE0, 0x0F, 0x60, 0x60, 0xFF, 0x91, 0xC0, 0x00,
                0x00, 0x01, 0x00, 0x00, 0xD7, 0xFF, 0xF8, 0x80,
                0x00, 0x00, 0x01, 0x01, 0x12, 0xE0, 0x36, 0x80,
                0xC8, 0xE0, 0x00, 0x00, 0x01, 0x00, 0x01, 0x17,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x01, 0x57,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x01, 0x97,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x01, 0xD7,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x02, 0x17,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x02, 0x57,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x02, 0x97,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x02, 0xD7,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x03, 0x17,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x03, 0x57,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x03, 0x97,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x03, 0xD7,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x04, 0x17,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x04, 0x57,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70
            ])
        s_block_end("MPEG_PS_P_1_DATA_VSEQ_3")

        # ---------------------------------------------------------------------
        # Video sequence - 4
        # NOTE: Not being fuzzed.
        # ---------------------------------------------------------------------

        if s_block_start("MPEG_PS_P_1_DATA_VSEQ_4"):
            s_binary([
                0x00, 0x00, 0x01, 0xB3, 0x01, 0x40, 0x14, 0x12,
                0x15, 0xF9, 0x23, 0x80, 0x00, 0x00, 0x01, 0xB8,
                0x00, 0x08, 0x43, 0x00, 0x00, 0x00, 0x01, 0x00,
                0x00, 0x0F, 0xFF, 0xF8, 0x00, 0x00, 0x01, 0x01,
                0x13, 0xF0, 0xD4, 0x94, 0x85, 0xC9, 0x98, 0x34,
                0xA0, 0x0B, 0x4A, 0x03, 0x24, 0xC7, 0x01, 0x49,
                0x4F, 0xF0, 0xD4, 0x1B, 0x9F, 0x37, 0xCF, 0x8D,
                0xD6, 0x90, 0x18, 0x00, 0x3E, 0x21, 0x00, 0x60,
                0x03, 0xB0, 0x10, 0xF0, 0x1D, 0x0D, 0xC4, 0x20,
                0xD2, 0x6A, 0x79, 0x31, 0x09, 0x4A, 0x53, 0xF1,
                0x43, 0x78, 0xC7, 0x1B, 0xFA, 0xD9, 0x9E, 0x22,
                0xE8, 0xA5, 0x29, 0x11, 0x72, 0x94, 0xA4, 0x45,
                0xCA, 0x52, 0x91, 0x10, 0x00, 0x00, 0x01, 0x00,
                0x00, 0x57, 0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01,
                0x01, 0x12, 0xCC, 0x03, 0x83, 0x4D, 0x22, 0xEF,
                0x8C, 0x80, 0x3D, 0x53, 0x91, 0x38, 0x99, 0x1C,
                0x00, 0x00, 0x01, 0x00, 0x00, 0x97, 0xFF, 0xF8,
                0x80, 0x00, 0x00, 0x01, 0x01, 0x12, 0xCC, 0x0E,
                0xE0, 0x0F, 0x60, 0x60, 0xFF, 0x91, 0xC0, 0x00,
                0x00, 0x01, 0x00, 0x00, 0xD7, 0xFF, 0xF8, 0x80,
                0x00, 0x00, 0x01, 0x01, 0x12, 0xE0, 0x36, 0x80,
                0xC8, 0xE0, 0x00, 0x00, 0x01, 0x00, 0x01, 0x17,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x01, 0x57,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70, 0x00, 0x00, 0x01, 0x00, 0x01, 0x97,
                0xFF, 0xF8, 0x80, 0x00, 0x00, 0x01, 0x01, 0x12,
                0x74, 0x70
            ])
        s_block_end("MPEG_PS_P_1_DATA_VSEQ_4")

    s_block_end("MPEG_PS_P_1_DATA")
    
s_block_end("MPEG_PS_P_1")

# -----------------------------------------------------------------------------
# MPEG-1 Padding Stream
# -----------------------------------------------------------------------------

if s_block_start("MPEG_PS_PAD"):
    s_binary(PACKET_START_CODE)
    s_byte(0xBE, full_range=True)
    s_size("MPEG_PS_PAD_DATA", length=2, endian=">", fuzzable=True)

    if s_block_start("MPEG_PS_PAD_DATA"): 
        s_byte(0x0F, full_range=True)
        s_string("\xFF" * 598)
    s_block_end("MPEG_PS_PAD_DATA")

s_block_end("MPEG_PS_PAD")
