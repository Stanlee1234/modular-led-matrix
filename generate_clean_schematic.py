import re
import uuid

# Read current schematic
with open("KiCad/modularmatrix.kicad_sch", "r") as f:
    text = f.read()

# Extract lib_symbols with exact parentheses balance
idx1 = text.find("(lib_symbols")
bal = 0
for idx, ch in enumerate(text[idx1:]):
    if ch == "(": bal += 1
    elif ch == ")": bal -= 1
    if bal == 0:
        end_idx = idx1 + idx + 1
        break

lib_symbols_raw = text[idx1:end_idx]

pwr_flag_def = """\t\t(symbol "power:PWR_FLAG"
\t\t\t(power global)
\t\t\t(pin_numbers
\t\t\t\t(hide yes)
\t\t\t)
\t\t\t(pin_names
\t\t\t\t(offset 0)
\t\t\t\t(hide yes)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "#FLG"
\t\t\t\t(at 0 1.905 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t\t(hide yes)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Value" "PWR_FLAG"
\t\t\t\t(at 0 3.81 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Footprint" ""
\t\t\t\t(at 0 0 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t\t(hide yes)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Datasheet" "~"
\t\t\t\t(at 0 0 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t\t(hide yes)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Description" "Power flag symbol"
\t\t\t\t(at 0 0 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t\t(hide yes)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "PWR_FLAG_0_0"
\t\t\t\t(polyline
\t\t\t\t\t(pts
\t\t\t\t\t\t(xy 0 0)
\t\t\t\t\t\t(xy 0 1.27)
\t\t\t\t\t\t(xy -1.016 1.905)
\t\t\t\t\t\t(xy 0 2.54)
\t\t\t\t\t\t(xy 1.016 1.905)
\t\t\t\t\t\t(xy 0 1.27)
\t\t\t\t\t)
\t\t\t\t\t(stroke
\t\t\t\t\t\t(width 0)
\t\t\t\t\t\t(type default)
\t\t\t\t\t)
\t\t\t\t\t(fill
\t\t\t\t\t\t(type none)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "PWR_FLAG_0_1"
\t\t\t\t(pin power_out line
\t\t\t\t\t(at 0 0 90)
\t\t\t\t\t(length 0)
\t\t\t\t\t(name "pwr"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "1"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t)
"""

if "power:PWR_FLAG" not in lib_symbols_raw:
    last_paren = lib_symbols_raw.rfind(")")
    lib_symbols_raw = lib_symbols_raw[:last_paren].rstrip() + "\n" + pwr_flag_def + "\t)"

# Extract all symbol blocks
sym_blocks_raw = re.findall(r"(\t\(symbol\s+\(lib_id\s+\"([^\"]+)\"\)\s+\(at\s+[\d\.\-]+\s+[\d\.\-]+(?:\s+[\d\.\-]+)?\).*?\n\t\))", text[end_idx:], re.DOTALL)
sym_dict = {}
for full_block, lib_id in sym_blocks_raw:
    ref_m = re.search(r"\(property\s+\"Reference\"\s+\"([^\"]+)\"", full_block)
    if ref_m:
        sym_dict[ref_m.group(1)] = (lib_id, full_block)

def make_sym(ref, sx, sy, srot, ref_dx, ref_dy, ref_just, val_dx, val_dy, val_just, hide_val=False):
    if ref in ("#FLG01", "#FLG02"):
        flag_uuid = "3fdaae88-2982-4799-8c51-02fc499a2756" if ref == "#FLG01" else "5501b341-5997-4d2a-859d-97fcb549963f"
        pin_uuid = "1f8d79d2-f1ae-4214-85db-d66755d5a3aa" if ref == "#FLG01" else "68bb7068-ebda-4f71-8dab-f073654bb47c"
        return f"""\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{flag_uuid}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {sx:.2f} {sy-3.81:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "PWR_FLAG"
\t\t\t(at {sx:.2f} {sy+3.81:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" "Power flag symbol"
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1" (uuid "{pin_uuid}"))
\t\t(instances
\t\t\t(project "modularmatrix"
\t\t\t\t(path "/5ab56492-366c-4f9f-88c9-0814fc5584d0"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""

    lib_id, old_block = sym_dict[ref]
    
    uuid_m = re.search(r"\(uuid\s+\"([^\"]+)\"\)", old_block)
    sym_uuid = uuid_m.group(1) if uuid_m else str(uuid.uuid4())
    if ref == "U69":
        sym_uuid = "5516d5d6-05b9-4283-8c49-7662e62ce63e"
        
    val_m = re.search(r"\(property\s+\"Value\"\s+\"([^\"]+)\"", old_block)
    val_str = val_m.group(1) if val_m else ref
    
    fp_m = re.search(r"\(property\s+\"Footprint\"\s+\"([^\"]*)\"", old_block)
    fp_str = fp_m.group(1) if fp_m else ""
    
    ds_m = re.search(r"\(property\s+\"Datasheet\"\s+\"([^\"]*)\"", old_block)
    ds_str = ds_m.group(1) if ds_m else ""
    
    desc_m = re.search(r"\(property\s+\"Description\"\s+\"([^\"]*)\"", old_block)
    desc_str = desc_m.group(1) if desc_m else ""
    
    mpn_m = re.search(r"\(property\s+\"MPN\"\s+\"([^\"]*)\"", old_block)
    mpn_str = mpn_m.group(1) if mpn_m else ""
    
    pins_block = ""
    for p_m in re.finditer(r"(\(pin\s+\"[^\"]+\"\s+\(uuid\s+\"[^\"]+\"\)\))", old_block):
        pins_block += "\t\t" + p_m.group(1) + "\n"
        
    inst_m = re.search(r"(\(instances.*?\n\t\t\))", old_block, re.DOTALL)
    inst_block = ("\t\t" + inst_m.group(1) + "\n") if inst_m else ""
    if ref == "U69" and inst_block:
        inst_block = inst_block.replace("a3f0cf89-0e47-4b12-bd55-62d06fa851fd", "5516d5d6-05b9-4283-8c49-7662e62ce63e")

    rx = sx + ref_dx
    ry = sy + ref_dy
    vx = sx + val_dx
    vy = sy + val_dy

    r_just_str = f"\n\t\t\t\t(justify {ref_just})" if ref_just else ""
    v_just_str = f"\n\t\t\t\t(justify {val_just})" if val_just else ""
    v_hide_str = "\n\t\t\t(hide yes)" if hide_val else ""
    rot_str = f" {srot}" if srot != 0 else " 0"

    out = f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {sx:.2f} {sy:.2f}{rot_str})
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{sym_uuid}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {rx:.2f} {ry:.2f} 0)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t){r_just_str}
\t\t\t)
\t\t)
\t\t(property "Value" "{val_str}"
\t\t\t(at {vx:.2f} {vy:.2f} 0){v_hide_str}
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t){v_just_str}
\t\t\t)
\t\t)
\t\t(property "Footprint" "{fp_str}"
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "{ds_str}"
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" "{desc_str}"
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)"""

    if mpn_str:
        out += f"""
\t\t(property "MPN" "{mpn_str}"
\t\t\t(at {sx:.2f} {sy:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)"""

    out += f"\n{pins_block}{inst_block}\t)"
    return out

# Build all symbols
symbols = []

# --- Section 1 ---
# U69: MCU
symbols.append(make_sym("U69", 78.74, 78.74, 0, -12.70, -16.51, "left", -12.70, 17.50, "left"))
# C63: Decoupling cap for MCU
symbols.append(make_sym("C63", 53.34, 55.88, 0, 2.54, -1.27, "left", 2.54, 1.27, "left"))
# R1: 470R DIN resistor
symbols.append(make_sym("R1", 106.68, 71.12, 270, 0.00, -2.54, None, 0.00, 2.54, None))
# SW1: Brightness Dimmer
symbols.append(make_sym("SW1", 53.34, 127.00, 0, 0.00, -4.50, None, 0.00, 4.50, None))
# SW2: Mode Selector
symbols.append(make_sym("SW2", 109.22, 127.00, 0, 0.00, -4.50, None, 0.00, 4.50, None))

# --- Section 2 ---
# U26: North Female
symbols.append(make_sym("U26", 53.34, 185.42, 0, 3.81, -6.50, None, 3.81, 6.50, None))
# U28: East Male
symbols.append(make_sym("U28", 111.76, 185.42, 0, 3.81, -6.50, None, 3.81, 6.50, None))
# U27: South Female
symbols.append(make_sym("U27", 53.34, 226.06, 0, 3.81, -6.50, None, 3.81, 6.50, None))
# U29: West Male
symbols.append(make_sym("U29", 111.76, 226.06, 0, 3.81, -6.50, None, 3.81, 6.50, None))

# --- Section 4 ---
# J1: UPDI & Expansion
symbols.append(make_sym("J1", 347.98, 66.04, 0, 0.00, -6.50, None, 0.00, 6.50, None))
# J2: Mirror Bus
symbols.append(make_sym("J2", 391.16, 66.04, 0, 0.00, -6.50, None, 0.00, 6.50, None))
# PWR_FLAGS
symbols.append(make_sym("#FLG01", 345.44, 100.33, 0, 0.00, -3.81, None, 0.00, 3.81, None, hide_val=False))
symbols.append(make_sym("#FLG02", 388.62, 100.33, 0, 0.00, -3.81, None, 0.00, 3.81, None, hide_val=False))

# --- Section 3 ---
# 6 rows of 6 LEDs + 6 decoupling caps
rows = [
    ("ROW 0", 48.26, ["U15", "U14", "U13", "U12", "U11", "U10"], ["C29", "C30", "C23", "C2", "C20", "C17"]),
    ("ROW 1", 86.36, ["U23", "U22", "U21", "U20", "U19", "U18"], ["C14", "C9", "C6", "C10", "C8", "C52"]),
    ("ROW 2", 124.46, ["U35", "U34", "U33", "U32", "U31", "U30"], ["C43", "C48", "C56", "C15", "C3", "C11"]),
    ("ROW 3", 162.56, ["U43", "U42", "U41", "U40", "U39", "U38"], ["C4", "C16", "C12", "C57", "C33", "C51"]),
    ("ROW 4", 200.66, ["U51", "U50", "U49", "U48", "U47", "U46"], ["C34", "C27", "C44", "C22", "C54", "C38"]),
    ("ROW 5", 238.76, ["U59", "U58", "U57", "U56", "U55", "U54"], ["C62", "C58", "C47", "C55", "C41", "C31"])
]

lx_cols = [165.10, 189.23, 213.36, 237.49, 261.62, 285.75]
cx_cols = [173.99, 198.12, 222.25, 246.38, 270.51, 294.64]

for r_name, y_row, led_list, cap_list in rows:
    for c in range(6):
        led_ref = led_list[c]
        cap_ref = cap_list[c]
        lx = lx_cols[c]
        cx = cx_cols[c]
        
        symbols.append(make_sym(led_ref, lx, y_row, 0, 4.50, -6.50, None, 4.50, 6.50, None, hide_val=True))
        symbols.append(make_sym(cap_ref, cx, y_row, 180, 2.00, -1.27, "left", 2.00, 1.27, "left"))

wires = []
junctions = []
labels = []

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

def add_local_label(name, x, y, rot):
    just = "right" if rot in (180, 270) else "left"
    labels.append(f"""\t(label "{name}"
\t\t(at {x:.2f} {y:.2f} {rot})
\t\t(fields_autoplaced yes)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {just})
\t\t)
\t\t(uuid "{uuid.uuid4()}")
\t)""")

# ==================== SECTION 1 WIRES & LABELS ====================
# MCU Power
add_wire(78.74, 60.96, 78.74, 53.34)
add_global_label("5V", 78.74, 53.34, 90)

add_wire(78.74, 96.52, 78.74, 104.14)
add_global_label("GND", 78.74, 104.14, 270)

# MCU Decoupling Cap C63 (at 53.34, 55.88)
# Pin 1 (at 53.34, 59.69) -> 5V
add_wire(53.34, 59.69, 33.02, 59.69)
add_global_label("5V", 33.02, 59.69, 180)
# Pin 2 (at 53.34, 52.07) -> GND
add_wire(53.34, 52.07, 33.02, 52.07)
add_global_label("GND", 33.02, 52.07, 180)

# MCU Right side pins (x=93.98)
# Pin 10 (PA0/UPDI): at (93.98, 68.58)
add_wire(93.98, 68.58, 137.16, 68.58)
add_global_label("/RESET/UPDI", 137.16, 68.58, 0)

# Pin 9 (PA1/DIN via R1): at (93.98, 71.12) -> R1 at 106.68 -> DIN
add_wire(93.98, 71.12, 102.87, 71.12)
add_wire(110.49, 71.12, 137.16, 71.12)
add_global_label("DIN", 137.16, 71.12, 0)

# Pin 8 (PA2/D00): at (93.98, 73.66)
add_wire(93.98, 73.66, 137.16, 73.66)
add_global_label("D00", 137.16, 73.66, 0)

# Pin 7 (PA3/D01): at (93.98, 76.20)
add_wire(93.98, 76.20, 137.16, 76.20)
add_global_label("D01", 137.16, 76.20, 0)

# Pin 13 (PB0/D10): at (93.98, 78.74)
add_wire(93.98, 78.74, 137.16, 78.74)
add_global_label("D10", 137.16, 78.74, 0)

# Pin 12 (PB1/D11): at (93.98, 81.28)
add_wire(93.98, 81.28, 137.16, 81.28)
add_global_label("D11", 137.16, 81.28, 0)

# Pin 11 (PB2/D20): at (93.98, 83.82)
add_wire(93.98, 83.82, 137.16, 83.82)
add_global_label("D20", 137.16, 83.82, 0)

# Pin 6 (PB3/D21): at (93.98, 86.36)
add_wire(93.98, 86.36, 137.16, 86.36)
add_global_label("D21", 137.16, 86.36, 0)

# MCU Left side pins (x=63.50)
# Pin 2 (PA4/B0/SCL): at (63.50, 68.58)
add_wire(63.50, 68.58, 33.02, 68.58)
add_global_label("B0/SCL", 33.02, 68.58, 180)

# Pin 3 (PA5/B1/SDA): at (63.50, 71.12)
add_wire(63.50, 71.12, 33.02, 71.12)
add_global_label("B1/SDA", 33.02, 71.12, 180)

# Pin 4 (PA6/D31): at (63.50, 73.66)
add_wire(63.50, 73.66, 33.02, 73.66)
add_global_label("D31", 33.02, 73.66, 180)

# Pin 5 (PA7/D30): at (63.50, 76.20)
add_wire(63.50, 76.20, 33.02, 76.20)
add_global_label("D30", 33.02, 76.20, 180)

# SW1: Brightness Dimmer (at 53.34, 127.00)
add_wire(48.26, 127.00, 33.02, 127.00)
add_global_label("B0/SCL", 33.02, 127.00, 180)
add_wire(58.42, 127.00, 66.04, 127.00)
add_global_label("GND", 66.04, 127.00, 0)

# SW2: Mode Selector (at 109.22, 127.00)
add_wire(104.14, 127.00, 96.52, 127.00)
add_global_label("B1/SDA", 96.52, 127.00, 180)
add_wire(114.30, 127.00, 137.16, 127.00)
add_global_label("GND", 137.16, 127.00, 0)

# ==================== SECTION 2 WIRES & LABELS ====================
# North Female U26 (at 53.34, 185.42)
add_wire(50.80, 181.61, 27.94, 181.61)
add_global_label("5V", 27.94, 181.61, 180)
add_wire(50.80, 184.15, 27.94, 184.15)
add_global_label("D00", 27.94, 184.15, 180)
add_wire(50.80, 186.69, 27.94, 186.69)
add_global_label("D01", 27.94, 186.69, 180)
add_wire(50.80, 189.23, 27.94, 189.23)
add_global_label("GND", 27.94, 189.23, 180)

# East Male U28 (at 111.76, 185.42)
add_wire(109.22, 181.61, 85.09, 181.61)
add_global_label("GND", 85.09, 181.61, 180)
add_wire(109.22, 184.15, 85.09, 184.15)
add_global_label("D11", 85.09, 184.15, 180)
add_wire(109.22, 186.69, 85.09, 186.69)
add_global_label("D10", 85.09, 186.69, 180)
add_wire(109.22, 189.23, 85.09, 189.23)
add_global_label("5V", 85.09, 189.23, 180)

# South Female U27 (at 53.34, 226.06)
add_wire(50.80, 222.25, 27.94, 222.25)
add_global_label("5V", 27.94, 222.25, 180)
add_wire(50.80, 224.79, 27.94, 224.79)
add_global_label("D20", 27.94, 224.79, 180)
add_wire(50.80, 227.33, 27.94, 227.33)
add_global_label("D21", 27.94, 227.33, 180)
add_wire(50.80, 229.87, 27.94, 229.87)
add_global_label("GND", 27.94, 229.87, 180)

# West Male U29 (at 111.76, 226.06)
add_wire(109.22, 222.25, 85.09, 222.25)
add_global_label("GND", 85.09, 222.25, 180)
add_wire(109.22, 224.79, 85.09, 224.79)
add_global_label("D30", 85.09, 224.79, 180)
add_wire(109.22, 227.33, 85.09, 227.33)
add_global_label("D31", 85.09, 227.33, 180)
add_wire(109.22, 229.87, 85.09, 229.87)
add_global_label("5V", 85.09, 229.87, 180)

# ==================== SECTION 4 WIRES & LABELS ====================
# J1: UPDI & Expansion (at 347.98, 66.04)
# Left pins (1, 3, 5, 7) at x = 347.98 - 5.08 = 342.90
add_wire(342.90, 63.50, 330.20, 63.50)
add_global_label("/RESET/UPDI", 330.20, 63.50, 180)
add_wire(342.90, 66.04, 330.20, 66.04)
add_global_label("GND", 330.20, 66.04, 180)
add_wire(342.90, 68.58, 330.20, 68.58)
add_global_label("B0/SCL", 330.20, 68.58, 180)
add_wire(342.90, 71.12, 330.20, 71.12)
add_global_label("B1/SDA", 330.20, 71.12, 180)

# Right pins (2, 4, 6, 8) at x = 347.98 + 7.62 = 355.60
add_wire(355.60, 63.50, 368.30, 63.50)
add_global_label("5V", 368.30, 63.50, 0)
add_wire(355.60, 66.04, 368.30, 66.04)
add_global_label("DIN", 368.30, 66.04, 0)
add_wire(355.60, 68.58, 368.30, 68.58)
add_global_label("GND", 368.30, 68.58, 0)
add_wire(355.60, 71.12, 368.30, 71.12)
add_global_label("DOUT", 368.30, 71.12, 0)

# J2: Mirror Bus (at 391.16, 66.04)
# Left pins (1, 3, 5, 7) at x = 391.16 - 5.08 = 386.08
add_wire(386.08, 63.50, 373.38, 63.50)
add_global_label("/RESET/UPDI", 373.38, 63.50, 180)
add_wire(386.08, 66.04, 373.38, 66.04)
add_global_label("GND", 373.38, 66.04, 180)
add_wire(386.08, 68.58, 373.38, 68.58)
add_global_label("B0/SCL", 373.38, 68.58, 180)
add_wire(386.08, 71.12, 373.38, 71.12)
add_global_label("B1/SDA", 373.38, 71.12, 180)

# Right pins (2, 4, 6, 8) at x = 391.16 + 7.62 = 398.78
add_wire(398.78, 63.50, 411.48, 63.50)
add_global_label("5V", 411.48, 63.50, 0)
add_wire(398.78, 66.04, 411.48, 66.04)
add_global_label("DIN", 411.48, 66.04, 0)
add_wire(398.78, 68.58, 411.48, 68.58)
add_global_label("GND", 411.48, 68.58, 0)
add_wire(398.78, 71.12, 411.48, 71.12)
add_global_label("DOUT", 411.48, 71.12, 0)

# Power Flags
add_wire(345.44, 100.33, 330.20, 100.33)
add_global_label("5V", 330.20, 100.33, 180)
add_wire(388.62, 100.33, 373.38, 100.33)
add_global_label("GND", 373.38, 100.33, 180)

# ==================== SECTION 3 WIRES & LABELS ====================
inter_row_nets = [
    ("DIN", "Net-(U10-DOUT)"),
    ("Net-(U10-DOUT)", "Net-(U18-DOUT)"),
    ("Net-(U18-DOUT)", "Net-(U30-DOUT)"),
    ("Net-(U30-DOUT)", "Net-(U38-DOUT)"),
    ("Net-(U38-DOUT)", "Net-(U46-DOUT)"),
    ("Net-(U46-DOUT)", "DOUT")
]

for r_idx, (r_name, y_row, led_list, cap_list) in enumerate(rows):
    in_net, out_net = inter_row_nets[r_idx]
    
    # 1. 5V Power Rail (Upper): at y = y_row - 1.27
    y_vdd = y_row - 1.27
    add_wire(154.94, y_vdd, 294.64, y_vdd)
    add_global_label("5V", 154.94, y_vdd, 180)
    
    # 2. GND Power Rail (Lower): at y = y_row + 1.27
    y_gnd = y_row + 1.27
    add_wire(154.94, y_gnd, 294.64, y_gnd)
    add_global_label("GND", 154.94, y_gnd, 180)
    
    # Connect each LED and Capacitor to 5V and GND
    for c in range(6):
        lx = lx_cols[c]
        cx = cx_cols[c]
        
        # LED Pin 3 (VDD) is at (lx - 2.54, y_vdd)
        add_junc(lx - 2.54, y_vdd)
        
        # LED Pin 2 (GND) is at (lx - 2.54, y_gnd)
        add_junc(lx - 2.54, y_gnd)
        
        # Capacitor (rot 180):
        # Pin 1 (5V) is at (cx, y_row - 3.81) -> wire down to (cx, y_vdd)
        add_wire(cx, y_row - 3.81, cx, y_vdd)
        add_junc(cx, y_vdd)
        
        # Pin 2 (GND) is at (cx, y_row + 3.81) -> wire up to (cx, y_gnd)
        add_wire(cx, y_row + 3.81, cx, y_gnd)
        add_junc(cx, y_gnd)

    # 3. Data In: to LED 0 Pin 4 (DIN) at (162.56, y_row + 3.81)
    y_din = y_row + 3.81
    y_dout = y_row - 3.81
    add_wire(154.94, y_din, 162.56, y_din)
    if in_net == "DIN":
        add_global_label("DIN", 154.94, y_din, 180)
    else:
        add_local_label(in_net, 154.94, y_din, 180)

    # 4. Serpentine chaining within the row:
    for c in range(5):
        x_dout = lx_cols[c] - 2.54
        x_din_next = lx_cols[c+1] - 2.54
        x_step = cx_cols[c] + 6.35
        
        add_wire(x_dout, y_dout, x_step, y_dout)
        add_wire(x_step, y_dout, x_step, y_din)
        add_wire(x_step, y_din, x_din_next, y_din)

    # 5. Data Out from LED 5 Pin 1 (DOUT) at (283.21, y_dout)
    # 304.80 is 240 * 1.27 mm (exact 50 mil connection grid!)
    add_wire(283.21, y_dout, 304.80, y_dout)
    if out_net == "DOUT":
        add_global_label("DOUT", 304.80, y_dout, 0)
    else:
        add_local_label(out_net, 304.80, y_dout, 0)

rectangles = """	(rectangle
		(start 16.00 16.00)
		(end 146.00 142.00)
		(stroke
			(width 0.3)
			(type dash)
		)
		(fill
			(type none)
		)
		(uuid "56c5e2ec-48e0-4a87-9759-4bb485fc3db3")
	)
	(rectangle
		(start 16.00 148.00)
		(end 146.00 282.00)
		(stroke
			(width 0.3)
			(type dash)
		)
		(fill
			(type none)
		)
		(uuid "3f9801ad-b1a7-4740-b610-d02c65aa1d9c")
	)
	(rectangle
		(start 152.00 16.00)
		(end 316.00 282.00)
		(stroke
			(width 0.3)
			(type dash)
		)
		(fill
			(type none)
		)
		(uuid "6f3d4e78-0cb9-4679-b141-86fbfb01e389")
	)
	(rectangle
		(start 322.00 16.00)
		(end 418.00 120.00)
		(stroke
			(width 0.3)
			(type dash)
		)
		(fill
			(type none)
		)
		(uuid "ea46db3e-c6e3-479e-a89d-7201c70e7b7c")
	)
	(rectangle
		(start 322.00 126.00)
		(end 418.00 282.00)
		(stroke
			(width 0.3)
			(type dash)
		)
		(fill
			(type none)
		)
		(uuid "03b22cfc-0f6a-4648-9366-22a3db61c32c")
	)"""

texts = """	(text "1. MICROCONTROLLER & CONTROLS (ATtiny1604)"
		(at 20.00 20.00 0)
		(effects
			(font
				(size 2.5 2.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "6eb77efb-5e63-4ce4-82a1-aa8be7f91720")
	)
	(text "20MHz AVR Core | Dual User Buttons | LED Buffer Resistor"
		(at 20.00 25.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(italic yes)
			)
			(justify left)
		)
		(uuid "3b9a59aa-b51f-4b0d-9b57-19aa82be1e22")
	)
	(text "SW1: Brightness Dimmer"
		(at 36.00 118.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "17d05777-6262-432d-8692-a1f0a2d21652")
	)
	(text "SW2: Mode Selector"
		(at 94.00 118.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "b09eb12f-6888-4c12-9e2e-2e06f8595aee")
	)
	(text "2. 4-WAY MAGNETIC SNAP BUS CONNECTORS"
		(at 20.00 154.00 0)
		(effects
			(font
				(size 2.5 2.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "fcf6e680-e83c-4444-a15e-a61fefffa744")
	)
	(text "Self-Aligning Edge Pogo Connectors with Instant Hardware Detection"
		(at 20.00 159.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(italic yes)
			)
			(justify left)
		)
		(uuid "f183cf53-bba2-47ea-a4be-4f4aa0093a41")
	)
	(text "NORTH EDGE (Female)"
		(at 28.00 171.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "df6fe992-0720-4e31-8ca6-d62f4370ecf6")
	)
	(text "EAST EDGE (Male)"
		(at 88.00 171.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "9b3c4314-ecfa-4da6-92c1-d41cfa2a884f")
	)
	(text "SOUTH EDGE (Female)"
		(at 28.00 211.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "217215ca-eec6-4f48-ab50-ff9b986e681c")
	)
	(text "WEST EDGE (Male)"
		(at 88.00 211.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "eb458348-18e0-4ba2-921d-23956e1df26f")
	)
	(text "3. 6x6 WS2812D ADDRESSABLE RGB LED MATRIX"
		(at 156.00 20.00 0)
		(effects
			(font
				(size 2.5 2.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "9f116a4a-1ad0-4f51-b0fe-24df974bb75f")
	)
	(text "36x Diffused LEDs in Serpentine Chain | Local 100n Decoupling Capacitors"
		(at 156.00 25.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(italic yes)
			)
			(justify left)
		)
		(uuid "1d6c8e3c-8b83-4a1d-a320-f5a6b7d159ae")
	)
	(text "ROW 0"
		(at 154.00 39.26 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "03b30ad5-9eb9-40ae-af65-748981df52ea")
	)
	(text "ROW 1"
		(at 154.00 77.36 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "8939c07e-07bf-4f93-8f0a-115fb38c3539")
	)
	(text "ROW 2"
		(at 154.00 115.46 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "fcf061c0-eb88-4682-841f-135e5d1ecafc")
	)
	(text "ROW 3"
		(at 154.00 153.56 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "14f2e96d-c840-41bf-94f4-6da5e486016e")
	)
	(text "ROW 4"
		(at 154.00 191.66 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "e6c0c299-d4c3-4d43-85f5-f53835ee6162")
	)
	(text "ROW 5"
		(at 154.00 229.76 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "3f9848f5-9610-4f51-b847-f38b0292b3ef")
	)
	(text "4. PROGRAMMING & EXPANSION HEADERS"
		(at 326.00 20.00 0)
		(effects
			(font
				(size 2.5 2.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "f3ef9cf5-1ea9-42b7-a3ea-20d0fdf1f2f0")
	)
	(text "Dual 2x4 SMD Headers for 1-Wire UPDI Flashing & Bus Expansion"
		(at 326.00 25.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(italic yes)
			)
			(justify left)
		)
		(uuid "7fbeba9d-a41e-450f-9ad0-42790906be73")
	)
	(text "J1 (UPDI & EXPANSION)"
		(at 332.00 48.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "89fba9dc-e2b2-4d1a-be10-d023f05d92e5")
	)
	(text "J2 (MIRROR BUS)"
		(at 376.00 48.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "6f35ea90-251a-471a-9694-817abdf2847a")
	)
	(text "POWER FLAGS & NET DECLARATION"
		(at 326.00 90.00 0)
		(effects
			(font
				(size 2.0 2.0)
				(bold yes)
			)
			(justify left)
		)
		(uuid "5ef731ad-35ea-4dca-9759-994f31cfa7ee")
	)
	(text "5. THEORY OF OPERATION & SYSTEM NOTES"
		(at 326.00 130.00 0)
		(effects
			(font
				(size 2.5 2.5)
				(bold yes)
			)
			(justify left)
		)
		(uuid "d0a85ba4-e0b4-4b47-b86c-0f9c2d76587d")
	)
	(text "Architecture, Flashing Guide, and Mechanical Assembly"
		(at 326.00 135.00 0)
		(effects
			(font
				(size 1.5 1.5)
				(italic yes)
			)
			(justify left)
		)
		(uuid "fcf061be-c045-4235-9689-138b051268ea")
	)
	(text "SYSTEM OVERVIEW:\\n* Microcontroller: Microchip ATtiny1604-SS (20MHz internal oscillator, 16KB Flash, 1KB SRAM).\\n* LED Display: 36x WS2812D addressable RGB LEDs arranged in a 6x6 serpentine array.\\n* Decoupling: Dedicated 100nF ceramic capacitor for each LED and MCU VDD rail.\\n\\n4-WAY MAGNETIC BUS & AUTODETECT:\\n* Complementary Gender Architecture:\\n  - North & South edges: 4-pin Female spring pogo connectors.\\n  - East & West edges: 4-pin Male target pad connectors.\\n* Automatic Grid Topology Mapping:\\n  - Pins D00..D31 form complementary neighbor detection pairs across adjacent tiles.\\n  - Internal pullups sense tile attachment instantly on contact without software overhead.\\n\\nFIRMWARE FLASHING (UPDI):\\n* Single-wire UPDI interface available on Pin 1 of J1/J2 (/RESET/UPDI).\\n* Compatible with SerialUPDI (CH340/CP2102 + 4.7k resistor + diode) or jtag2updi programmer.\\n* Board package: megaTinyCore in Arduino IDE.\\n* Recommended settings: ATtiny1604, 20MHz internal clock, BOD disabled / 2.6V."
		(at 326.00 144.00 0)
		(effects
			(font
				(size 1.3 1.3)
			)
			(justify left top)
		)
		(uuid "7fbe7cf5-87ea-46b5-82b1-4191fe8c71b1")
	)"""

header = """(kicad_sch
	(version 20231120)
	(generator "eeschema")
	(generator_version "8.0")
	(uuid "5ab56492-366c-4f9f-88c9-0814fc5584d0")
	(paper "A3")
	(title_block
		(title "Modular LED Matrix 6x6 (Bitluni Architecture)")
		(date "2026-11-01")
		(rev "v2.0-aligned")
		(company "Antigravity Hardware")
		(comment 1 "6x6 WS2812D Addressable LEDs + ATtiny1604-SS + 4-Way Magnetic Snap Bus")
		(comment 2 "Serpentine Daisy Chain with Complementary Neighbor Sensing")
		(comment 3 "Clean Modular Schematic Layout")
	)
"""

trailer = """	(sheet_instances
		(path "/"
			(page "1")
		)
	)
)
"""

assembled = header + "\t" + lib_symbols_raw + "\n" + rectangles + "\n" + texts + "\n" + "\n".join(wires) + "\n" + "\n".join(junctions) + "\n" + "\n".join(labels) + "\n" + "\n".join(symbols) + "\n" + trailer

open_p = assembled.count("(")
close_p = assembled.count(")")
assert open_p == close_p, f"Parentheses mismatch: {open_p} vs {close_p}"

with open("KiCad/modularmatrix.kicad_sch", "w") as f:
    f.write(assembled)

print("Generated clean schematic with exact pin alignments!")
