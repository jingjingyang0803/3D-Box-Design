# Glucose Non-Invasive Monitoring System: Box Design

## Project Overview

This project is focused on designing and creating a specialized experimental box for the development of a non-invasive glucose monitoring system. The box is designed to allow the passage of 4-wavelength infrared (IR) light through a finger, which is then filtered before reaching a photodiode. The box also includes sensors for measuring humidity, providing critical data for the experiment.

## Objectives

1. To design a box that facilitates the passage of 4-wavelength IR light through the finger.
2. To implement a filtering mechanism that ensures accurate IR light measurement before reaching the photodiode.
3. To integrate humidity measurement sensors to provide complementary data during the experiment.
4. To create a script for precise control and monitoring of the setup.

## Design Dimensions

- **Height:** 55.5 mm (14.5 mm + 25 mm + 16 mm)
- **Width:** 50 mm
- **Depth:** 34 mm
- The **finger hole diameter** is **20 mm** to accommodate the user's finger for testing.
- The **optical filter diameter** is **14 mm**.
- The **photodiode diameter** is **9.5 mm**.
- The **humidity sensor** has a detection area of **7 mm by 7 mm**.

## Design Overview

The overall alignment is ensured by **interlocking features**, which work similarly to LEGO pieces. The large ring of one part fits snugly with the small ring in the other, ensuring a solid connection and correct alignment.

The design consists of five parts, each serving a specific function in the assembly:

### 1. **IR LED Housing:**

- **Purpose:** Houses the four IR LEDs, which are aimed at the photodiode to facilitate light-based measurement.
- **Key Features:**

  - Custom housing to fit the IR LEDs snugly.
  - Four precisely positioned slots for the IR LEDs.
  - LED slots are directed toward the photodiode for accurate light sensing.
  - Designed to ensure efficient and uniform light detection.

### 2. **Sensor and Filter Integration Slot:**

- **Purpose:** Serves as a combined slot for the finger hole as well as the optical filter and the humidity sensor.
- **Key Features:**
  - Dual purpose: it accommodates both the optical filter and the humidity sensor.
  - Precision design ensures both components fit securely and function properly.
  - Includes a finger hole to allow the passage of IR light and filter it before reaching the photodiode, while simultaneously measuring humidity during the process.

### 3. **Photodiode Housing:**

- **Purpose:** Holds the photodiode, which is essential for light sensing in the system.
- **Key Features:**
  - Custom housing to fit the photodiode snugly.
  - Optimal alignment for accurate light detection.

### 4. **Optical Filter Insert:**

- **Purpose:** Houses the optical filter.
- **Key Features:**
  - Precision cutout for filter insertion.
  - Ensures proper alignment of the optical filter in the system.

### 5. **Humidity Sensor Housing:**

- **Purpose:** Designed for the insertion of the humidity sensor.
- **Key Features:**

  - Secure compartment for the humidity sensor.
  - Easy installation without the risk of damage to the sensor.

## Running the FreeCAD Python Script

1. Install FreeCAD
   Download and install the latest version of FreeCAD from the official website: [https://www.freecad.org](https://www.freecad.org/)
2. Open FreeCAD and Start a New Document
   Launch FreeCAD and create a new empty document.
3. Open the Python Console
   In FreeCAD, go to View > Panels > Python console to enable the console.
4. **Paste and run the script** directly into the console
   - Copy the entire Python script
   - Paste it into the Python console
   - Press **Enter** to execute
5. View the Generated Model
   After execution, the 3D model will appear in the FreeCAD workspace. You can inspect, modify, or export it as needed.

## Assembly Instructions

1. **Insert the IR LEDs** into the IR LED housing, ensuring they are positioned **at the calculated angle** and directed towards the photodiode for proper light sensing.
2. **Attach the IR LED housing** to the assembly.
3. **Place the photodiode** in the photodiode housing.
4. **Attach the photodiode housing** to the assembly.
5. **Insert the optical filter** into the optical filter housing, aligning it correctly.
6. **Install the humidity sensor** into the humidity sensor housing, ensuring it sits **flat** and faces the finger hole for accurate humidity measurement.
7. **Fit the Sensor and Filter Integration Slot**, aligning the filter hole and humidity sensor slots with the corresponding components from the other parts, completing the setup.

## Conclusion

This design and the Python script are integral parts of the experimental setup for the non-invasive glucose monitoring system. The accurate measurement of IR light and humidity is essential for ensuring the reliability of the system, and this box serves as a controlled environment for those measurements.
