# Spinal Posture Tracking System (IDP)

A clinical-grade, multi-node wearable IoT system that monitors, classifies, and corrects human spinal posture in real time — combining on-device Deep Learning (TinyML) with deterministic biomechanical thresholds to help prevent musculoskeletal disorders (MSDs).

## How It Works

Two wireless sensor nodes are worn on the **cervical (neck)** and **thoracic (upper back)** spine. Each streams motion data over Bluetooth Low Energy to a web dashboard, which fuses a machine-learning posture classifier with strict trigonometric angle checks to flag bad posture and fatigue in real time.

## Architecture

| Layer | Tech | Purpose |
|---|---|---|
| **Firmware** (`XIAO_NECK/`, `XIAO_BACK/`, `nrf_app/`) | Zephyr RTOS, C++, Edge Impulse SDK | Reads the onboard IMU, runs a 1D-CNN posture classifier on-device, computes pitch/roll via `atan2`, and serves it all over a custom BLE GATT service |
| **ML Pipeline** (`datasets/`) | Python, Pandas/NumPy, Keras/TFLite Micro | Augments a ~152K-row accelerometer dataset across 227 synthetic anthropometric profiles to train a lightweight 1D-CNN (`Sitting` / `Slouching` / `Standing`) that fits in <256KB RAM on a Cortex-M4 |
| **Frontend** (`web_app/`) | React 19, Web Bluetooth API, Recharts, react-three-fiber | Landing page with a 3D spine visualization + a live dashboard that connects to both nodes, charts telemetry, computes a weighted "Spine Score," and sounds alerts for slouching/static fatigue |

## Hardware

- 2x Seeed Studio **XIAO BLE (nRF52840)** — one per node (`XIAO-NECK`, `XIAO-BACK`)
- **LSM6DS3** 6-axis IMU (I2C) on each node
- Custom BLE Posture Service (`0x181A`) broadcasting `[AI_State, Pitch_Angle, Roll_Angle]`, plus a standard Battery Service (`0x180F`)

## Clinical Thresholds

- **Cervical forward pitch** > 15–20° → flagged strain
- **Thoracic forward pitch** > 30–40° → flagged strain
- **Lateral tilt (roll)** > 10° on either node → flagged instability
- **Angular variance** < 3° sustained → static fatigue alert (prompts the user to stand)

These deterministic rules run alongside the ML classifier — the model interprets movement *context*, while the trigonometry enforces hard clinical limits.

## Running the Dashboard

```bash
cd web_app
npm install
npm start
```

Opens at `http://localhost:3000`. Requires a Web Bluetooth–capable browser (Chrome/Edge) and the physical XIAO nodes to connect to live telemetry.

## Repository Layout

```
XIAO_NECK/    Cervical node firmware (.ino)
XIAO_BACK/    Thoracic node firmware (.ino)
nrf_app/      Zephyr RTOS app: IMU + BLE GATT + Edge Impulse inference
datasets/     Raw + augmented training data, cleaning/partitioning scripts
web_app/      React dashboard (landing page + live telemetry/Spine Score UI)
```
