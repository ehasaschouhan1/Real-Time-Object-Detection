# Building a Real-Time Object Detection & Logging Platform with YOLOv8, OpenCV and MySQL

## Introduction

For Assignment 5, I built a Real-Time Object Detection and Logging Platform using Python. The project combines computer vision, YOLOv8 object detection, OpenCV webcam processing, a Tkinter dashboard, and MySQL event logging.

The main goal was to detect selected objects in real time, display bounding boxes and confidence scores, and store detection events in a database.

## Computer Vision & YOLO Learning

I learned how OpenCV can capture frames from a webcam and process them continuously.

I used the lightweight YOLOv8n model from Ultralytics. The model provides the detected object's class, confidence score, and bounding-box coordinates.

The platform also supports a configurable confidence threshold. For example, setting the threshold to 0.70 means that only detections with at least 70% confidence are considered.

## Modular Application Development

I separated the project into multiple Python files:

- `main.py` starts the application.
- `detector.py` handles YOLO detection.
- `database.py` handles MySQL operations.
- `ui.py` contains the dashboard.
- `config.py` manages configuration.

This structure makes the application easier to understand, test, and maintain.

## Database Integration

I created a MySQL database named `vision_platform` with a `detection_logs` table.

Each event stores:

- Log ID
- Timestamp
- Object class
- Confidence
- Bounding-box X and Y coordinates
- Bounding-box width and height

To avoid exposing credentials, database settings are stored in a `.env` file and excluded using `.gitignore`.

## User Interface

The dashboard was created using Tkinter. It contains:

- Live webcam feed
- YOLO bounding boxes
- Confidence threshold control
- Object-class filter
- Live metrics
- Recent MySQL detection logs

This provides a simple interface for demonstrating the complete pipeline.

## Challenges & Solutions

One challenge was connecting real-time computer vision processing with database logging without creating an excessive number of duplicate rows.

I solved this by adding a small logging cooldown for each detected object class.

Another challenge was keeping the project modular. I separated detection, database, configuration, and UI responsibilities into different files.

## Final Result

The final platform can detect selected objects through a webcam, display their bounding boxes and confidence scores, and save detection events into MySQL in real time.

### Links

GitHub: PASTE_YOUR_GITHUB_LINK_HERE

Demo Video: PASTE_YOUR_DEMO_LINK_HERE

Screenshots: Add screenshots of the dashboard and MySQL table here.

## Conclusion

This project helped me understand how computer vision, machine learning inference, databases, and user interfaces can be combined into one practical application.
