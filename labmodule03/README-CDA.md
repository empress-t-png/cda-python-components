
# Lab Module 03 - CDA README

## Summary
This lab module implemented data simulation capabilities for the Constrained Device Application (CDA), including sensor data generation, actuator simulation, and a centralized device data management system.

## What Does Your Implementation Do?
The Lab Module 03 implementation creates a complete data simulation infrastructure for IoT sensors and actuators:

- **Sensor Simulation**: Generates realistic time-series data for temperature, humidity, and pressure sensors
- **Actuator Simulation**: Simulates HVAC and humidifier actuators that respond to sensor data
- **Data Management**: Coordinates all data flow between sensors, actuators, and system performance monitoring
- **Automated Control**: Automatically triggers HVAC actuation when temperature exceeds configured thresholds

The implementation enables the CDA to run autonomously, collecting simulated sensor data and responding with appropriate actuator commands based on environmental conditions.

## How Does It Work?

### Architecture Overview
The implementation follows an object-oriented design with inheritance hierarchies for sensors and actuators:

**Core Simulation Components:**
1. **SensorDataGenerator** - Generates realistic sensor data with configurable ranges and randomization
2. **BaseSensorSimTask** - Base class for all sensor simulation tasks
3. **BaseActuatorSimTask** - Base class for all actuator simulation tasks

**Sensor Simulation Tasks:**
- TemperatureSensorSimTask (18-24°C range)
- HumiditySensorSimTask (30-70% range)
- PressureSensorSimTask (990-1010 kPa range)

**Actuator Simulation Tasks:**
- HvacActuatorSimTask - Simulates HVAC system
- HumidifierActuatorSimTask - Simulates humidifier

**Manager Classes:**
1. **SensorAdapterManager** - Manages sensor tasks using APScheduler for periodic data collection (every 5 seconds by default)
2. **ActuatorAdapterManager** - Manages actuator tasks and processes actuation commands
3. **DeviceDataManager** - Central coordinator that:
   - Receives sensor data callbacks
   - Analyzes temperature data
   - Triggers HVAC actuation when temperature is outside the 18-20°C range
   - Coordinates SystemPerformanceManager, SensorAdapterManager, and ActuatorAdapterManager

**Main Application:**
- **ConstrainedDeviceApp** - Entry point that initializes and starts the DeviceDataManager

### Data Flow
1. SensorAdapterManager periodically polls sensor tasks (every 5 seconds)
2. Sensor tasks generate simulated data using SensorDataGenerator
3. Sensor data is passed to DeviceDataManager via callbacks
4. DeviceDataManager analyzes temperature data
5. If temperature is outside threshold (18-20°C), DeviceDataManager creates ActuatorData command
6. ActuatorAdapterManager processes the command and triggers the HVAC actuator
7. Actuator logs the actuation event with ON/OFF status and target value

### Key Implementation Details
- **Inheritance Pattern**: All sensor/actuator tasks inherit from base classes for code reuse
- **Configuration-Driven**: Min/max values, thresholds, and polling rates configured in PiotConfig.props
- **Callback Architecture**: Managers use IDataMessageListener interface for loose coupling
- **Scheduled Execution**: APScheduler runs sensor polling in background threads
- **Location Awareness**: All data includes locationID for multi-device deployments

## How Did You Test It?

### Unit Tests (All Passed ✓)
Ran unit tests for simulation tasks:
```bash

