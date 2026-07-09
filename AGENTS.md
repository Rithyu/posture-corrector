# LLM Context: Multi-Node Biomechanical Posture Tracking System (IDP)

## 🤖 INSTRUCTIONS FOR AI AGENTS
You are acting as an academic research assistant and technical writer. Use the context in this document to help the user draft academic reports, methodology sections, literature reviews, and technical documentation for their Interdisciplinary Departmental Project (IDP). Maintain a formal, academic, and clinical engineering tone.

---

## 1. PROJECT OVERVIEW
This project is a clinical-grade, multi-node wearable IoT system designed to monitor, classify, and correct human spinal posture in real-time. It bridges the gap between Deep Learning (TinyML) and deterministic biomechanical rules to prevent musculoskeletal disorders (MSDs).

*   **Primary Objective:** To detect acute postural strain and prolonged static fatigue using a dual-sensor setup on the Cervical (C7) and Thoraci (T12) spine.
*   **Key Innovation:** Combining a 1D-Convolutional Neural Network (for spatio-temporal pattern recognition) with real-time trigonometric thresholding (for strict clinical compliance).

## 2. HARDWARE ARCHITECTURE
*   **Microcontrollers:** 2x Seeed Studio XIAO BLE (nRF52840).
    *   Node 1: `XIAO-NECK` (Cervical).
    *   Node 2: `XIAO-BACK` (Thoracic).
*   **Sensors:** LSM6DS3 (6-axis IMU) operating over I2C.
*   **Communications:** Bluetooth Low Energy (BLE).
    *   Custom Posture Service UUID: `0x181A`
    *   Posture Characteristic UUID: `0x2A56` (Transmits 3 bytes: `[AI_State, Pitch_Angle, Roll_Angle]`)
    *   Standard Battery Service UUID: `0x180F`

## 3. SOFTWARE & FIRMWARE STACK
*   **Firmware:** Zephyr RTOS (C++). Handles I2C sensor reading, ML inference via Edge Impulse SDK, trigonometric angle calculations, and BLE GATT server hosting.
*   **Frontend Dashboard:** React.js, Tailwind CSS (v3), Recharts, and Web Bluetooth API.
*   **Frontend Features:** Live telemetry charting, Web Audio API alarm synthesis (for 5-min slouching/fatigue alerts), CSV clinical data export, zero-calibration, and a weighted "Overall Spine Score" gauge.

## 4. MACHINE LEARNING PIPELINE (TinyML)
*   **Platform:** Edge Impulse / Keras / TensorFlow Lite for Microcontrollers.
*   **Algorithm:** 1D-Convolutional Neural Network (1D-CNN).
*   **Input Features:** 2-second sliding window of Ax, Ay, Az acceleration data (sampled at ~50Hz).
*   **Classes:** `Sitting`, `Slouching`, `Standing`.
*   **Dataset & Augmentation:** The original dataset was augmented using a custom Python script (Pandas/NumPy) to reach **152,435 data points**. To ensure model generalization and prevent overfitting to a single user, Gaussian noise was applied, and the data was m,apped to **227 synthetic human profiles** featuring distinct anthropometric variables (Age, Height, Weight).

## 5. BIOMECHANICAL & CLINICAL METHODOLOGY
The system does not rely on the AI alone. To ensure clinical validity, raw accelerometer data (G-forces) are converted into exact Pitch and Roll angles using `atan2` trigonometry.

**Strict Clinical Thresholds applied in the Frontend:**
1.  **Cervical Forward Pitch:** Strain is flagged if neck angle exceeds **15° - 20°**.
2.  **Thoracic Forward Pitch:** Strain is flagged if back angle exceeds **30° - 40°**.
3.  **Lateral Stability (Roll):** Strain is flagged if side-to-side tilt exceeds **10°** on either node.
4.  **Muscular Fatigue Alert:** An alert is triggered if angular variance remains <3° for an extended period (static posture fatigue), alerting the user to stand and restore spinal disc hydration.

## 6. ACADEMIC REPORT WRITING GUIDELINES
When generating report content for this project, the LLM should emphasize:
*   **Sensor Fusion:** How the dual-node setup provides superior spatio-temporal data compared to single-node commercial trackers.
*   **TinyML Optimization:** How using the EON compiler to run a Keras model on a Cortex-M4 chip (<256KB RAM) reduces latency and saves power by avoiding cloud-computing dependencies.
*   **Deterministic vs. Probabilistic:** How the system uses Deep Learning (probabilistic) to understand the *context* of movement, and trigonometric math (deterministic) to enforce strict *clinical thresholds*.

## 7. KEY REPOSITORY FILES (Context)
*   `src/main.cpp`: Zephyr RTOS firmware handling IMU, BLE, and ML inference.
*   `App.jsx`: The React frontend containing the BLE connection logic, Spine Score calculator, and graphing.
*   `augment_dataset.py`: Python script used to expand the dataset to 152k rows and inject the 227 anthropometric profiles.
```eof