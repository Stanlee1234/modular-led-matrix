# 🧲 Modular Magnetic 6x6 LED Matrix

Hey! This is my modular 6x6 RGB LED matrix tile. It’s heavily inspired by [bitluni's magnetMatrix](https://github.com/bitluni/magnetMatrix6x6).

The idea is super simple: you can snap multiple tiles together like magnetic Lego bricks! When they click into place, they share 5V power and automatically sense which sides have a neighbor attached, so cool animations and color waves can ripple across the whole grid without any Wi-Fi or messy wires.

![Modular Matrix](KiCad/pcb_preview_top.png)

---

## ⚡ How It Works

* **Magnetic Snap**: Every edge has a 4-pin magnetic connector (carrying 5V, GND, and 2 sense lines). Opposing edges have matching male & female connectors that pull themselves together.
* **Instant Neighbor Detection**: Instead of dealing with complicated networking protocols, each edge has complementary pull-up and pull-down pins. The second two boards touch, the ATtiny pin gets pulled low and immediately knows: *"Hey, someone just connected to my right!"*
* **36 RGB LEDs**: Uses 36 through-hole diffused WS2812D (5mm) LEDs in a serpentine layout.
* **Brain**: An ATtiny1604 running at 20MHz controls all the animations and logic standalone.
* **Buttons**: 2 little tactile buttons on the back let you switch animation modes and adjust brightness.

---

## 🛠️ Main Parts (Per Tile)

* **1x** Microchip ATtiny1604 (SOIC-14)
* **36x** WS2812D-F5 (5mm diffused through-hole RGB LEDs)
* **4x** 4-pin 2.2mm right-angle magnetic connectors (2 male pogo, 2 female flat pad)
* **37x** 100nF 0603 SMD capacitors (one for each LED + MCU power)
* **1x** 470Ω 0603 SMD resistor
* **2x** 3×4mm 2-pin SMD tactile buttons
* **2x** 2×4 2.54mm SMD pin headers (for UPDI flashing & expansion)

---

## 🚀 How to Flash & Build

1. **Soldering**: Solder the SMD stuff on the back first (ATtiny1604, caps, resistor, buttons), then solder the through-hole LEDs on the front and magnetic connectors on the edges.
2. **Setup Arduino IDE**: Install **megaTinyCore** by Spence Konde (`http://drazzy.com/package_drazzy.com_index.json`).
3. **Flashing**: Hook up a cheap SerialUPDI adapter (or Arduino running `jtag2updi`) to the UPDI, 5V, and GND pins on the header. Select **Board: ATtiny1604** and hit **Upload Using Programmer**!
4. **Case**: 3D print the snap-on case (`top6x6.stl` in white filament for light diffusion, and `bottom6x6.stl` in black).

---

## Big Thanks
Huge shoutout to **bitluni** for the awesome original project idea and magnetic connector layout!
