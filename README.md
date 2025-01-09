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
