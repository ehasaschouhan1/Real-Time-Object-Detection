# VisionLog — Real-Time Object Detection & Logging Platform

A modular Python project for real-time object detection using YOLOv8, OpenCV, Tkinter, and MySQL.

## Features

- Real-time webcam object detection
- YOLOv8n pre-trained model
- Bounding boxes and confidence scores
- Configurable object-class filter
- Adjustable confidence threshold
- MySQL event logging
- Recent detection log dashboard
- Modular architecture
- `.env` based database credentials

## Project Structure

```text
Real-Time-Object-Detection/
│
├── main.py
├── detector.py
├── database.py
├── ui.py
├── config.py
├── database_schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup

### 1. Install Python

Python 3.10 or newer is recommended.

### 2. Create virtual environment

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Install packages

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

Start MySQL using XAMPP or MySQL Workbench.

Copy `.env.example` to `.env` and set your MySQL username/password.

Example for a default local XAMPP MySQL setup:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=vision_platform
```

The application automatically creates the database and table on startup.

### 5. Run

```powershell
python main.py
```

The first YOLO run may download `yolov8n.pt` automatically.

## Object Filter

In the application:

```text
person, cell phone
```

You can change it to:

```text
person
```

or:

```text
bottle, cup, laptop
```

Use YOLO class names.

## Confidence

Use `0.70` for 70% confidence.

The application only processes detections at or above the selected threshold.

## Database

Database name:

```text
vision_platform
```

Table:

```text
detection_logs
```

Columns:

- log_id
- timestamp
- object_class
- confidence
- bbox_x
- bbox_y
- bbox_w
- bbox_h

## Demo

1. Start MySQL.
2. Run `python main.py`.
3. Click Start Camera.
4. Show a person and/or cell phone.
5. Show bounding boxes.
6. Point to the Recent MySQL Logs panel.
7. Open MySQL and run:

```sql
USE vision_platform;
SELECT * FROM detection_logs ORDER BY log_id DESC;
```

## Safety

Never upload `.env` or database passwords to GitHub.
