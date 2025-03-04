# PLC
PLC Programmable Logic Controller Software<br>
Written in Python using Pygame-CE<br>
Using Modbus to interact with the physical world

### Current Features
- 5 Different Node Types
    - Digital Input
    - Digital Output
    - Timer Module (Standard Delay, On/Off Delay, Clock)
    - Inverter (Not Gate)
    - And Gate
- Infinite Page for dragging nodes onto
- Node menus to modify parameters
- Home and Program screens
    - Home locks the page and allows the user to simulate inputs
    - Program allows the user to drag any node to anywhere on the page and program the logic
- Outputs can be connected over ModbusTCP to any Modbus RTU to interact with the physical world (Inputs coming soon!)
- Millisecond level accurate timing

### New Feature Ideas
- Save and Load files
- Connect to ESP32 IO nodes for physical connections
- More Logic Gates
- Non-boolean values, numbers, compare operations
- Number variables

### Demonstration Video:
[![Demonstration Video Thumbnail](https://img.youtube.com/vi/ws9uSAPO2gg/0.jpg)](https://www.youtube.com/watch?v=ws9uSAPO2gg)
