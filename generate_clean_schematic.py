import uuid
import re

# ==============================================================================
# GENERATOR FOR MODULAR LED MATRIX 6x6 SCHEMATIC (HUMANLIKE WIRING)
# ==============================================================================

wires = []
junctions = []
labels = []
symbols = []
texts = []

def add_wire(x1, y1, x2, y2):
    wires.append(f"""\t(wire
\t\t(pts
\t\t\t(xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)""")

def add_junc(x, y):
    junctions.append(f"""\t(junction
\t\t(at {x:.2f} {y:.2f})
\t\t(diameter 0)
\t\t(color 0 0 0 0)
\t\t(uuid "{uuid.uuid4()}")
\t)""")

def add_global_label(name, x, y, rot, shape="input"):
    just = "right" if rot in (180, 270) else "left"
    labels.append(f"""\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {x:.2f} {y:.2f} {rot})
\t\t(fields_autoplaced yes)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {just})
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Intersheet References" "${{INTERSHEET_REFS}}"
\t\t\t(at {x:.2f} {y:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t)""")

def add_text(text, x, y, size=1.5, bold=False):
    bold_str = "\n\t\t\t\t(bold yes)" if bold else ""
    texts.append(f"""\t(text "{text}"
\t\t(at {x:.2f} {y:.2f} 0)
\t\t(effects
\t\t\t(font
\t\t\t\t(size {size:.2f} {size:.2f}){bold_str}
\t\t\t)
\t\t\t(justify left top)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)""")

def make_sym(ref, x, y, rot=0, ref_ox=2.54, ref_oy=-1.27, ref_just="left", val_ox=2.54, val_oy=1.27, val_just="left", hide_val=False, font_size=1.27):
    # Lookup symbol info
    if ref.startswith("C"):
        lib_id = "Device:C"
        val = "100n"
        fp = "Capacitor_SMD:C_0603_1608Metric"
        desc = "Unpolarized capacitor"
    elif ref.startswith("R"):
        lib_id = "Device:R"
        val = "470R"
        fp = "Resistor_SMD:R_0603_1608Metric"
        desc = "Resistor"
    elif ref == "U69":
        lib_id = "MCU_Microchip_ATtiny:ATtiny1604-SS"
        val = "ATtiny1604-SS"
        fp = "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm"
        desc = "20MHz, 16kB Flash, 1kB SRAM, 256B EEPROM, SOIC-14"
    elif ref in ["SW1", "SW2"]:
        lib_id = "Switch:SW_Push"
        val = "SW_Push"
        fp = "Library:SMD_ButtonC354946"
        desc = "Push button switch, generic, two pins"
    elif ref in ["J1", "J2"]:
        lib_id = "Connector_Generic:Conn_02x04_Odd_Even"
        val = "Conn_02x04_Odd_Even"
        fp = "Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical_SMD"
        desc = "Generic connector, double row, 02x04"
    elif ref in ["U26", "U27"]:
        lib_id = "New_Library:fakeMag4pinFemale"
        val = "fakeMag4pinFemale"
        fp = "Library:fakemag4pin90degFemale"
        desc = "Magnetic connector female 4-pin"
    elif ref in ["U28", "U29"]:
        lib_id = "New_Library:fakeMag4pinMale"
        val = "fakeMag4pinMale"
        fp = "Library:fakemag4pin90degMale"
        desc = "Magnetic connector male 4-pin"
    elif ref.startswith("U"):
        lib_id = "New_Library:WS2812D"
        val = "WS2812D"
        fp = "Library:WS2812DwideC"
        desc = "WS2812D Addressable RGB LED"
    elif ref.startswith("#FLG"):
        lib_id = "power:PWR_FLAG"
        val = "PWR_FLAG"
        fp = ""
        desc = "Power flag symbol"
    else:
        raise ValueError(f"Unknown component: {ref}")

    hide_val_str = "\n\t\t\t(hide yes)" if hide_val else ""
    ref_just_str = f"\n\t\t\t\t(justify {ref_just})" if ref_just else ""
    val_just_str = f"\n\t\t\t\t(justify {val_just})" if val_just else ""

    rx = x + ref_ox
    ry = y + ref_oy
    vx = x + val_ox
    vy = y + val_oy

    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:.2f} {y:.2f} {rot})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {rx:.2f} {ry:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size {font_size:.2f} {font_size:.2f})
\t\t\t\t){ref_just_str}
\t\t\t)
\t\t)
\t\t(property "Value" "{val}"
\t\t\t(at {vx:.2f} {vy:.2f} 0){hide_val_str}
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size {font_size:.2f} {font_size:.2f})
\t\t\t\t){val_just_str}
\t\t\t)
\t\t)
\t\t(property "Footprint" "{fp}"
\t\t\t(at {x:.2f} {y:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x:.2f} {y:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" "{desc}"
\t\t\t(at {x:.2f} {y:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1" (uuid "{uuid.uuid4()}"))
\t\t(pin "2" (uuid "{uuid.uuid4()}"))
\t)"""

# ==============================================================================
# 1. SECTION 1: MICROCONTROLLER & CONTROLS (ATtiny1604)
# ==============================================================================
# MCU U69 at (80.00, 75.00)
symbols.append(make_sym("U69", 80.00, 75.00, 0, -12.70, -16.51, "left", 2.54, 16.51, "left"))

# MCU Pin 1 (VCC) at (80.00, 57.22)
# MCU Pin 14 (GND) at (80.00, 92.78)
# C63 bypass capacitor placed beside MCU at (60.00, 50.00)
symbols.append(make_sym("C63", 60.00, 50.00, 0, 2.54, -1.27, "left", 2.54, 1.27, "left"))

# C63 Pin 1 (top, 5V) at (60.00, 46.19)
# C63 Pin 2 (bottom, GND) at (60.00, 53.81)
# Wire MCU Pin 1 up to 46.19, left to C63 Pin 1, and left to 5V global label
add_wire(80.00, 57.22, 80.00, 46.19)
add_wire(80.00, 46.19, 60.00, 46.19)
add_wire(60.00, 46.19, 45.00, 46.19)
add_junc(80.00, 46.19)
add_junc(60.00, 46.19)
add_global_label("5V", 45.00, 46.19, 180)

# C63 Pin 2 to GND
add_wire(60.00, 53.81, 60.00, 57.15)
add_global_label("GND", 60.00, 57.15, 270)

# MCU Pin 14 to GND
add_wire(80.00, 92.78, 80.00, 99.06)
add_global_label("GND", 80.00, 99.06, 270)

# Resistor R1 (470R) on Pin 11 (PA1) leading to DIN
# MCU Pin 11 is at (95.24, 67.38)
symbols.append(make_sym("R1", 112.00, 67.38, 90, 0, -3.00, "center", 0, 3.00, "center"))
# R1 Pin 1 is at (108.19, 67.38), Pin 2 is at (115.81, 67.38)
add_wire(95.24, 67.38, 108.19, 67.38)
add_wire(115.81, 67.38, 138.00, 67.38)
add_global_label("DIN", 138.00, 67.38, 0)

# MCU Right Bus Pins
# Pin 10 (PA0/RESET/UPDI) at (95.24, 64.84)
add_wire(95.24, 64.84, 138.00, 64.84)
add_global_label("/RESET/UPDI", 138.00, 64.84, 0)

# Pin 12 (PA2/D00) at (95.24, 69.92)
add_wire(95.24, 69.92, 138.00, 69.92)
add_global_label("D00", 138.00, 69.92, 0)

# Pin 13 (PA3/D01) at (95.24, 72.46)
add_wire(95.24, 72.46, 138.00, 72.46)
add_global_label("D01", 138.00, 72.46, 0)

# Pin 2 (PA4/D10) at (95.24, 75.00)
add_wire(95.24, 75.00, 138.00, 75.00)
add_global_label("D10", 138.00, 75.00, 0)

# Pin 3 (PA5/D11) at (95.24, 77.54)
add_wire(95.24, 77.54, 138.00, 77.54)
add_global_label("D11", 138.00, 77.54, 0)

# Pin 4 (PA6/D21) at (95.24, 80.08)
add_wire(95.24, 80.08, 138.00, 80.08)
add_global_label("D21", 138.00, 80.08, 0)

# Pin 5 (PA7/D20) at (95.24, 82.62)
add_wire(95.24, 82.62, 138.00, 82.62)
add_global_label("D20", 138.00, 82.62, 0)

# MCU Left Bus Pins
# Pin 7 (PB2/D30) at (64.76, 69.92)
add_wire(64.76, 69.92, 25.00, 69.92)
add_global_label("D30", 25.00, 69.92, 180)

# Pin 6 (PB3/D31) at (64.76, 72.46)
add_wire(64.76, 72.46, 25.00, 72.46)
add_global_label("D31", 25.00, 72.46, 180)

# SW1 (Brightness Dimmer) at (45.00, 115.00)
symbols.append(make_sym("SW1", 45.00, 115.00, 0, -2.54, -3.81, "center", -2.54, 3.81, "center"))
add_text("SW1: Brightness Dimmer", 30.00, 107.00, size=1.27)

# SW2 (Mode Selector) at (95.00, 115.00)
symbols.append(make_sym("SW2", 95.00, 115.00, 0, -2.54, -3.81, "center", -2.54, 3.81, "center"))
add_text("SW2: Mode Selector", 80.00, 107.00, size=1.27)

# Connect MCU Pin 9 (PB0) to SW1 Pin 1 (at 39.92, 115.00)
# MCU Pin 9 is at (64.76, 64.84)
add_wire(64.76, 64.84, 39.92, 64.84)
add_wire(39.92, 64.84, 39.92, 115.00)
add_junc(39.92, 64.84)
add_wire(39.92, 64.84, 25.00, 64.84)
add_global_label("B0/SCL", 25.00, 64.84, 180)

# SW1 Pin 2 to GND
add_wire(50.08, 115.00, 60.00, 115.00)
add_global_label("GND", 60.00, 115.00, 0)

# Connect MCU Pin 8 (PB1) to SW2 Pin 1 (at 89.92, 115.00)
# MCU Pin 8 is at (64.76, 67.38)
add_wire(64.76, 67.38, 55.00, 67.38)
add_wire(55.00, 67.38, 55.00, 103.00)
add_wire(55.00, 103.00, 89.92, 103.00)
add_wire(89.92, 103.00, 89.92, 115.00)
add_junc(55.00, 67.38)
add_wire(55.00, 67.38, 25.00, 67.38)
add_global_label("B1/SDA", 25.00, 67.38, 180)

# SW2 Pin 2 to GND
add_wire(100.08, 115.00, 110.00, 115.00)
add_global_label("GND", 110.00, 115.00, 0)


# ==============================================================================
# 2. SECTION 2: 4-WAY MAGNETIC SNAP BUS CONNECTORS
# ==============================================================================
symbols.append(make_sym("U26", 55.00, 180.00, 0, -2.54, -6.00, "center", -2.54, 6.00, "center"))
symbols.append(make_sym("U28", 115.00, 180.00, 0, -2.54, -6.00, "center", -2.54, 6.00, "center"))
symbols.append(make_sym("U27", 55.00, 240.00, 0, -2.54, -6.00, "center", -2.54, 6.00, "center"))
symbols.append(make_sym("U29", 115.00, 240.00, 0, -2.54, -6.00, "center", -2.54, 6.00, "center"))

add_text("NORTH EDGE (Female)", 35.00, 168.00, size=1.27, bold=True)
add_text("EAST EDGE (Male)", 95.00, 168.00, size=1.27, bold=True)
add_text("SOUTH EDGE (Female)", 35.00, 228.00, size=1.27, bold=True)
add_text("WEST EDGE (Male)", 95.00, 228.00, size=1.27, bold=True)

# U26 (Female)
add_wire(52.46, 176.19, 30.00, 176.19)
add_global_label("5V", 30.00, 176.19, 180)
add_wire(52.46, 178.73, 30.00, 178.73)
add_global_label("D00", 30.00, 178.73, 180)
add_wire(52.46, 181.27, 30.00, 181.27)
add_global_label("D01", 30.00, 181.27, 180)
add_wire(52.46, 183.81, 30.00, 183.81)
add_global_label("GND", 30.00, 183.81, 180)

# U28 (Male)
add_wire(112.46, 176.19, 90.00, 176.19)
add_global_label("GND", 90.00, 176.19, 180)
add_wire(112.46, 178.73, 90.00, 178.73)
add_global_label("D21", 90.00, 178.73, 180)
add_wire(112.46, 181.27, 90.00, 181.27)
add_global_label("D20", 90.00, 181.27, 180)
add_wire(112.46, 183.81, 90.00, 183.81)
add_global_label("5V", 90.00, 183.81, 180)

# U27 (Female)
add_wire(52.46, 236.19, 30.00, 236.19)
add_global_label("5V", 30.00, 236.19, 180)
add_wire(52.46, 238.73, 30.00, 238.73)
add_global_label("D10", 30.00, 238.73, 180)
add_wire(52.46, 241.27, 30.00, 241.27)
add_global_label("D11", 30.00, 241.27, 180)
add_wire(52.46, 243.81, 30.00, 243.81)
add_global_label("GND", 30.00, 243.81, 180)

# U29 (Male)
add_wire(112.46, 236.19, 90.00, 236.19)
add_global_label("GND", 90.00, 236.19, 180)
add_wire(112.46, 238.73, 90.00, 238.73)
add_global_label("D31", 90.00, 238.73, 180)
add_wire(112.46, 241.27, 90.00, 241.27)
add_global_label("D30", 90.00, 241.27, 180)
add_wire(112.46, 243.81, 90.00, 243.81)
add_global_label("5V", 90.00, 243.81, 180)


# ==============================================================================
# 3. SECTION 3: 6x6 WS2812D ADDRESSABLE RGB LED MATRIX
# ==============================================================================
# 6 rows of 6 LEDs
rows_leds = [
    ("ROW 0", ["U15", "U14", "U13", "U12", "U11", "U10"]),
    ("ROW 1", ["U23", "U22", "U21", "U20", "U19", "U18"]),
    ("ROW 2", ["U35", "U34", "U33", "U32", "U31", "U30"]),
    ("ROW 3", ["U43", "U42", "U41", "U40", "U39", "U38"]),
    ("ROW 4", ["U51", "U50", "U49", "U48", "U47", "U46"]),
    ("ROW 5", ["U59", "U58", "U57", "U56", "U55", "U54"])
]

lx_cols = [168.00, 193.40, 218.80, 244.20, 269.60, 295.00]
y_rows = [38.10, 76.20, 114.30, 152.40, 190.50, 228.60]

for r, (r_name, led_list) in enumerate(rows_leds):
    y_row = y_rows[r]
    add_text(r_name, 154.00, y_row - 10.00, size=1.27, bold=True)
    
    # 5V Rail (y_row - 1.27)
    y_vdd = y_row - 1.27
    add_wire(158.00, y_vdd, 295.00, y_vdd)
    add_global_label("5V", 158.00, y_vdd, 180)
    
    # GND Rail (y_row + 1.27)
    y_gnd = y_row + 1.27
    add_wire(158.00, y_gnd, 295.00, y_gnd)
    add_global_label("GND", 158.00, y_gnd, 180)

    for c in range(6):
        led_ref = led_list[c]
        lx = lx_cols[c]
        symbols.append(make_sym(led_ref, lx, y_row, 0, 4.50, -6.50, "left", 4.50, 6.50, "left", hide_val=True))
        
        # Connect VDD (Pin 3) and GND (Pin 2)
        add_junc(lx - 2.54, y_vdd)
        add_junc(lx - 2.54, y_gnd)

    # In-row data wires (col 0 to 4)
    # Loop neatly over the top of the LED body without obstruction!
    for c in range(5):
        x_dout = lx_cols[c] - 2.54
        y_dout = y_row - 3.81
        x_din_next = lx_cols[c+1] - 2.54
        y_din_next = y_row + 3.81
        
        # Route: out of DOUT -> up to y_row - 6.35 -> across to x_din_next - 5.08 -> down to y_din_next -> into DIN
        y_top_route = y_row - 6.35
        x_drop = x_din_next - 5.08
        add_wire(x_dout, y_dout, x_dout, y_top_route)
        add_wire(x_dout, y_top_route, x_drop, y_top_route)
        add_wire(x_drop, y_top_route, x_drop, y_din_next)
        add_wire(x_drop, y_din_next, x_din_next, y_din_next)

# Serpentine inter-row data loops!
# Row 0 DIN:
add_wire(154.94, y_rows[0] + 3.81, lx_cols[0] - 2.54, y_rows[0] + 3.81)
add_global_label("DIN", 154.94, y_rows[0] + 3.81, 180)

# Loops between rows 0->1, 1->2, 2->3, 3->4, 4->5
for r in range(5):
    y_row_curr = y_rows[r]
    y_row_next = y_rows[r+1]
    
    x_dout_end = lx_cols[5] - 2.54  # 292.46
    y_dout_end = y_row_curr - 3.81
    
    x_din_start = lx_cols[0] - 2.54 # 165.46
    y_din_start = y_row_next + 3.81
    
    x_right_turn = 312.00
    y_channel = y_row_curr + 19.05  # halfway between row r and row r+1
    x_left_turn = 158.00
    
    # 1. Out from end DOUT to right margin
    add_wire(x_dout_end, y_dout_end, x_right_turn, y_dout_end)
    # 2. Down along right margin to channel
    add_wire(x_right_turn, y_dout_end, x_right_turn, y_channel)
    # 3. Across channel all the way left
    add_wire(x_right_turn, y_channel, x_left_turn, y_channel)
    # 4. Down to next row's DIN level
    add_wire(x_left_turn, y_channel, x_left_turn, y_din_start)
    # 5. Right into next row's DIN
    add_wire(x_left_turn, y_din_start, x_din_start, y_din_start)

# Row 5 DOUT exits to global label DOUT
x_last_dout = lx_cols[5] - 2.54
y_last_dout = y_rows[5] - 3.81
add_wire(x_last_dout, y_last_dout, 315.00, y_last_dout)
add_global_label("DOUT", 315.00, y_last_dout, 0)


# ==============================================================================
# 4. SECTION 4: PROGRAMMING & MIRROR HEADERS
# ==============================================================================
symbols.append(make_sym("J1", 350.00, 50.00, 0, -2.54, -6.50, "center", -2.54, 6.50, "center"))
symbols.append(make_sym("J2", 390.00, 50.00, 0, -2.54, -6.50, "center", -2.54, 6.50, "center"))

add_text("J1 (UPDI & EXPANSION)", 335.00, 38.00, size=1.27, bold=True)
add_text("J2 (MIRROR BUS)", 380.00, 38.00, size=1.27, bold=True)

# J1 & J2 Pins:
# J1 Odd pins at 344.92, Even pins at 357.62
# J2 Odd pins at 384.92, Even pins at 397.62
headers = [
    (350.00, 344.92, 357.62),
    (390.00, 384.92, 397.62)
]

for center_x, odd_x, even_x in headers:
    # Pin 1: /RESET/UPDI
    add_wire(odd_x, 46.19, odd_x - 10.00, 46.19)
    add_global_label("/RESET/UPDI", odd_x - 10.00, 46.19, 180)
    
    # Pin 3: GND
    add_wire(odd_x, 48.73, odd_x - 10.00, 48.73)
    add_global_label("GND", odd_x - 10.00, 48.73, 180)
    
    # Pin 5: B0/SCL
    add_wire(odd_x, 51.27, odd_x - 10.00, 51.27)
    add_global_label("B0/SCL", odd_x - 10.00, 51.27, 180)
    
    # Pin 7: B1/SDA
    add_wire(odd_x, 53.81, odd_x - 10.00, 53.81)
    add_global_label("B1/SDA", odd_x - 10.00, 53.81, 180)

    # Pin 2: 5V
    add_wire(even_x, 46.19, even_x + 10.00, 46.19)
    add_global_label("5V", even_x + 10.00, 46.19, 0)
    
    # Pin 4: DIN
    add_wire(even_x, 48.73, even_x + 10.00, 48.73)
    add_global_label("DIN", even_x + 10.00, 48.73, 0)
    
    # Pin 6: GND
    add_wire(even_x, 51.27, even_x + 10.00, 51.27)
    add_global_label("GND", even_x + 10.00, 51.27, 0)
    
    # Pin 8: DOUT
    add_wire(even_x, 53.81, even_x + 10.00, 53.81)
    add_global_label("DOUT", even_x + 10.00, 53.81, 0)

# Power Flags
symbols.append(make_sym("#FLG01", 345.00, 75.00, 0, 0, -2.54, "center", 0, 2.54, "center", hide_val=True))
add_wire(345.00, 75.00, 335.00, 75.00)
add_global_label("5V", 335.00, 75.00, 180)

symbols.append(make_sym("#FLG02", 385.00, 75.00, 0, 0, -2.54, "center", 0, 2.54, "center", hide_val=True))
add_wire(385.00, 75.00, 375.00, 75.00)
add_global_label("GND", 375.00, 75.00, 180)


# ==============================================================================
# 5. SECTION 5: DECOUPLING CAPACITORS (36x 100nF)
# ==============================================================================
# 36 decoupling caps arranged in a clean, spacious 6x6 bank!
caps_bank = [
    ['C2',  'C3',  'C4',  'C6',  'C8',  'C9'],
    ['C10', 'C11', 'C12', 'C14', 'C15', 'C16'],
    ['C17', 'C20', 'C22', 'C23', 'C27', 'C29'],
    ['C30', 'C31', 'C33', 'C34', 'C38', 'C41'],
    ['C43', 'C44', 'C47', 'C48', 'C51', 'C52'],
    ['C54', 'C55', 'C56', 'C57', 'C58', 'C62']
]

cx_bank = [338.00, 351.00, 364.00, 377.00, 390.00, 403.00]
cy_bank = [112.00, 130.00, 148.00, 166.00, 184.00, 202.00]

for r in range(6):
    cy = cy_bank[r]
    # Horizontal 5V rail at cy - 3.81
    y_rail_5v = cy - 3.81
    add_wire(333.00, y_rail_5v, 405.00, y_rail_5v)
    add_global_label("5V", 333.00, y_rail_5v, 180)
    
    # Horizontal GND rail at cy + 3.81
    y_rail_gnd = cy + 3.81
    add_wire(333.00, y_rail_gnd, 405.00, y_rail_gnd)
    add_global_label("GND", 333.00, y_rail_gnd, 180)

    for c in range(6):
        cx = cx_bank[c]
        cap_ref = caps_bank[r][c]
        symbols.append(make_sym(cap_ref, cx, cy, 0, 2.00, -1.27, "left", 2.00, 1.27, "left", font_size=1.0))
        
        # Connect Pin 1 (top, 5V) to 5V rail
        add_junc(cx, y_rail_5v)
        # Connect Pin 2 (bottom, GND) to GND rail
        add_junc(cx, y_rail_gnd)


# ==============================================================================
# SECTION BOXES & DOCUMENTATION
# ==============================================================================
rectangles = """\t(rectangle
\t\t(start 16.00 16.00)
\t\t(end 146.00 142.00)
\t\t(stroke
\t\t\t(width 0.3)
\t\t\t(type dash)
\t\t\t(color 0 0 150 1)
\t\t)
\t\t(fill
\t\t\t(type none)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(rectangle
\t\t(start 16.00 146.00)
\t\t(end 146.00 282.00)
\t\t(stroke
\t\t\t(width 0.3)
\t\t\t(type dash)
\t\t\t(color 0 0 150 1)
\t\t)
\t\t(fill
\t\t\t(type none)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(rectangle
\t\t(start 150.00 16.00)
\t\t(end 326.00 282.00)
\t\t(stroke
\t\t\t(width 0.3)
\t\t\t(type dash)
\t\t\t(color 0 0 150 1)
\t\t)
\t\t(fill
\t\t\t(type none)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(rectangle
\t\t(start 330.00 16.00)
\t\t(end 408.00 90.00)
\t\t(stroke
\t\t\t(width 0.3)
\t\t\t(type dash)
\t\t\t(color 0 0 150 1)
\t\t)
\t\t(fill
\t\t\t(type none)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(rectangle
\t\t(start 330.00 95.00)
\t\t(end 408.00 216.00)
\t\t(stroke
\t\t\t(width 0.3)
\t\t\t(type dash)
\t\t\t(color 0 0 150 1)
\t\t)
\t\t(fill
\t\t\t(type none)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(rectangle
\t\t(start 330.00 220.00)
\t\t(end 408.00 252.00)
\t\t(stroke
\t\t\t(width 0.3)
\t\t\t(type dash)
\t\t\t(color 0 0 150 1)
\t\t)
\t\t(fill
\t\t\t(type none)
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)"""

# Add section titles
add_text("1. MICROCONTROLLER & CONTROLS (ATtiny1604)", 20.00, 20.00, size=2.0, bold=True)
add_text("20MHz AVR Core | Dual User Buttons | In-Line R1 Protection | C63 Bypass Cap", 20.00, 25.00, size=1.2)

add_text("2. 4-WAY MAGNETIC SNAP BUS CONNECTORS", 20.00, 150.00, size=2.0, bold=True)
add_text("Self-Aligning Edge Pogo Connectors with Instant Hardware Detection", 20.00, 155.00, size=1.2)

add_text("3. 6x6 WS2812D ADDRESSABLE RGB LED MATRIX", 154.00, 20.00, size=2.0, bold=True)
add_text("Continuous Visible Serpentine Chain (Row 0 -> Row 5) | 36x WS2812D Pixels", 154.00, 25.00, size=1.2)

add_text("4. PROGRAMMING & EXPANSION HEADERS", 334.00, 20.00, size=1.8, bold=True)
add_text("Dual 2x4 SMD Headers for 1-Wire UPDI Flashing & Bus Mirroring", 334.00, 25.00, size=1.2)

add_text("5. DECOUPLING CAPACITORS (36x 100nF)", 334.00, 99.00, size=1.8, bold=True)
add_text("Dedicated 100nF 0603 Ceramic Bypass per WS2812D LED (Pin 1=5V, Pin 2=GND)", 334.00, 103.00, size=1.1)

add_text("6. SYSTEM ARCHITECTURE & TOPOLOGY", 334.00, 223.00, size=1.8, bold=True)
add_text("* Complementary Pogo Gender: North/South Female, East/West Male", 334.00, 228.00, size=1.1)
add_text("* Neighbor Detection: D00..D31 form complementary pairs across tiles", 334.00, 233.00, size=1.1)
add_text("* Firmware: megaTinyCore in Arduino IDE (ATtiny1604, 20MHz, 800kHz)", 334.00, 238.00, size=1.1)


with open('pristine_lib_symbols.sexpr', 'r') as f:
    lib_symbols_block = f.read()

# Also ensure lib_symbols includes "New_Library:WS2812D" without _2
if 'symbol "New_Library:WS2812D"' not in lib_symbols_block and 'symbol "New_Library:WS2812D_2"' in lib_symbols_block:
    lib_symbols_block = lib_symbols_block.replace('symbol "New_Library:WS2812D_2"', 'symbol "New_Library:WS2812D"')
    lib_symbols_block = lib_symbols_block.replace('symbol "WS2812D_2_0_1"', 'symbol "WS2812D_0_1"')
    lib_symbols_block = lib_symbols_block.replace('symbol "WS2812D_2_1_1"', 'symbol "WS2812D_1_1"')

# Build final schematic
full_sch = f"""(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{uuid.uuid4()}")
\t(paper "A3")
\t(title_block
\t\t(title "Modular LED Matrix 6x6 (Bitluni Compatible)")
\t\t(date "2026-11-01")
\t\t(rev "v2.1-humanlike")
\t\t(company "Antigravity Hardware")
\t\t(comment 1 "6x6 WS2812D Addressable LEDs + ATtiny1604-SS + 4-Way Magnetic Snap Bus")
\t\t(comment 2 "Serpentine Daisy Chain with Direct Component Wiring")
\t)
{lib_symbols_block}

{rectangles}

{"\n".join(texts)}

{"\n".join(junctions)}

{"\n".join(wires)}

{"\n".join(labels)}

{"\n".join(symbols)}

\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
)
"""

with open("KiCad/modularmatrix.kicad_sch", "w") as f:
    f.write(full_sch)

print("Successfully generated clean, humanlike modularmatrix.kicad_sch!")
