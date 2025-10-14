# Lab Module 04: Data Emulation

## Overview
This lab module implements sensor and actuator emulation using the Sense HAT Emulator, transitioning from simulated random data to actual emulated sensor readings and LED display control.

## Completed Tasks

### PIOT-CFG-04-001: Configuration
- Installed sense-emu (v1.2.1) and pisense (v0.2) libraries
- Applied source code fixes to gui.py and anim.py for compatibility
- Configured virtual environment for emulator support

### PIOT-CDA-04-001: Sensor Emulator Modules
Created 3 sensor emulator tasks:
- HumiditySensorEmulatorTask.py
- PressureSensorEmulatorTask.py
- TemperatureSensorEmulatorTask.py

### PIOT-CDA-04-002: Actuator Emulator Modules
Created 3 actuator emulator tasks:
- HumidifierEmulatorTask.py
- HvacEmulatorTask.py
- LedDisplayEmulatorTask.py

### PIOT-CDA-04-003: SensorAdapterManager Integration
- Added dynamic loading of sensor emulators
- Implemented conditional logic for emulator/simulator switching

### PIOT-CDA-04-004: ActuatorAdapterManager Integration
- Added dynamic loading of actuator emulators
- Implemented conditional logic for emulator/simulator switching

### PIOT-CDA-04-005: Hardware Deployment (OPTIONAL)
- Skipped - requires physical Raspberry Pi and Sense HAT hardware

### PIOT-CDA-04-100: Git Merge
- Successfully merged labmodule04 branch into default
- All changes pushed to GitHub

## Implementation Summary

Total files created/modified: 9
- 6 new emulator modules
- 2 updated manager classes
- 1 configuration file updated

## Author
Tosin (empress-t-png)

## Date
October 13, 2025
