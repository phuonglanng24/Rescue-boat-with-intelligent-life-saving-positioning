# Smart Boat Control Panel

This project is a **Smart Boat Control Panel** application built using Python. It integrates various components, including an ESP32-CAM, a YOLO object detection model, and a map interface powered by `TkinterMapView`. The application allows users to control the movement of a smart boat, monitor live video feeds, and visualize geographic coordinates on a map.

---

## Features

1. **Object Detection**: Utilizes the YOLOv8 model to detect objects in live camera feeds from the ESP32-CAM.
2. **Map Integration**: Displays the boat's current location on a map with options to set markers, zoom, and switch map views.
3. **Camera Control**: Supports commands to control the camera's position and movement (e.g., Left, Right, Forward, Stop).
4. **GUI Design**: A user-friendly graphical interface built with `CustomTkinter`.
5. **Live Updates**: Processes and displays real-time data received from the ESP32 server.

---

## Prerequisites

Before running this application, ensure you have the following installed:

1. **Python 3.8+**
2. Required Python libraries:
   - `tkinter`
   - `customtkinter`
   - `opencv-python`
   - `Pillow`
   - `numpy`
   - `requests`
   - `tkintermapview`
   - `ultralytics` (YOLO)

You can install the required dependencies using the following command:

```bash
pip install opencv-python pillow numpy requests tkintermapview customtkinter ultralytics
```
# Smart Boat Control Panel Setup and Usage Guide

---

## Setup Instructions

### 1. ESP32-CAM Configuration
- Set up your ESP32-CAM to stream video over an IP address.
- Update the following variables in the code to match your ESP32-CAM's configuration:
  - **`esp_ip`**: Replace with your ESP32-CAM's IP address.
  - **`esp_port`**: Replace with your ESP32-CAM's server port.

### 2. YOLOv8 Model
- The application uses YOLOv8 (`yolov8n.pt`) for object detection. 
- Ensure the model file is accessible in the working directory.

---

## How to Run

1. Clone the repository or copy the project files to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the application:

   ```bash
   Chuong_trinh_giao_dien.py
   ```

---

## User Interface

### **Left Frame**
- **Set Marker**: Adds a marker to the map at the current location.
- **Clear Markers**: Removes all markers from the map.
- **Tile Server**: Switch between OpenStreetMap, Google Normal, and Google Satellite map views.
- **Appearance Mode**: Change between Light, Dark, or System appearance modes.

### **Right Frame**
- Displays the map with real-time location updates.
- Includes a search bar for setting locations manually.

### **Control Buttons**
- **Left**: Move the camera/boat left.
- **Right**: Move the camera/boat right.
- **Forward**: Move the camera/boat forward.
- **Stop**: Stop the boat's movement.
- **Open/Close**: Control additional boat functionalities.

---

## Notes

- Ensure your ESP32-CAM and the computer running this application are on the same network.
- The application requires stable communication with the ESP32 server for smooth operation.


