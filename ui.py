import time
import tkinter as tk
from tkinter import ttk, messagebox

import cv2
from PIL import Image, ImageTk

import config
from database import fetch_recent_logs, log_detection
from detector import ObjectDetector


class DetectionUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VisionLog — Real-Time Object Detection Platform")
        self.root.geometry("1250x820")
        self.root.minsize(1050, 700)
        self.root.configure(bg="#10131a")

        self.camera = None
        self.running = False
        self.photo = None
        self.last_log_time = {}
        self.last_db_refresh = 0

        self.detector = ObjectDetector(
            confidence=config.CONFIDENCE_THRESHOLD,
            classes=config.DETECT_CLASSES,
        )

        self.total_objects = 0
        self.frame_count = 0
        self.fps_start = time.time()
        self.fps = 0.0

        self.build_ui()
        self.refresh_logs()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="VISIONLOG",
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#10131a",
        )
        title.pack(anchor="w", padx=25, pady=(18, 0))

        subtitle = tk.Label(
            self.root,
            text="Real-Time Object Detection • YOLOv8 • OpenCV • MySQL",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#10131a",
        )
        subtitle.pack(anchor="w", padx=27, pady=(0, 12))

        top = tk.Frame(self.root, bg="#181c25", padx=15, pady=12)
        top.pack(fill="x", padx=20, pady=8)

        tk.Label(
            top, text="Confidence ≥", font=("Segoe UI", 10, "bold"),
            fg="#ffffff", bg="#181c25"
        ).grid(row=0, column=0, padx=(0, 6))

        self.conf_var = tk.StringVar(value=str(config.CONFIDENCE_THRESHOLD))
        self.conf_entry = ttk.Entry(top, textvariable=self.conf_var, width=8)
        self.conf_entry.grid(row=0, column=1, padx=(0, 18))

        tk.Label(
            top, text="Detect classes:", font=("Segoe UI", 10, "bold"),
            fg="#ffffff", bg="#181c25"
        ).grid(row=0, column=2, padx=(0, 6))

        self.classes_var = tk.StringVar(value=", ".join(config.DETECT_CLASSES))
        self.classes_entry = ttk.Entry(top, textvariable=self.classes_var, width=35)
        self.classes_entry.grid(row=0, column=3, padx=(0, 18))

        self.start_button = ttk.Button(
            top, text="▶  Start Camera", command=self.start_camera
        )
        self.start_button.grid(row=0, column=4, padx=5)

        self.stop_button = ttk.Button(
            top, text="■  Stop", command=self.stop_camera, state="disabled"
        )
        self.stop_button.grid(row=0, column=5, padx=5)

        self.status_var = tk.StringVar(value="Status: Ready")
        tk.Label(
            top, textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            fg="#7dd3fc", bg="#181c25"
        ).grid(row=1, column=0, columnspan=6, sticky="w", pady=(10, 0))

        content = tk.Frame(self.root, bg="#10131a")
        content.pack(fill="both", expand=True, padx=20, pady=8)

        left = tk.Frame(content, bg="#181c25")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.video_label = tk.Label(
            left,
            text="Camera preview will appear here",
            font=("Segoe UI", 14),
            fg="#9ca3af",
            bg="#0b0e13",
            width=80,
            height=25,
        )
        self.video_label.pack(fill="both", expand=True, padx=10, pady=10)

        right = tk.Frame(content, bg="#181c25", width=380)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(
            right, text="LIVE METRICS",
            font=("Segoe UI", 13, "bold"),
            fg="#ffffff", bg="#181c25"
        ).pack(anchor="w", padx=15, pady=(15, 8))

        self.metric_var = tk.StringVar(
            value="Objects: 0\nFPS: 0.0\nDB: Connected"
        )
        tk.Label(
            right, textvariable=self.metric_var,
            justify="left", font=("Segoe UI", 11),
            fg="#d1d5db", bg="#181c25"
        ).pack(anchor="w", padx=15, pady=(0, 15))

        tk.Label(
            right, text="RECENT MYSQL LOGS",
            font=("Segoe UI", 13, "bold"),
            fg="#ffffff", bg="#181c25"
        ).pack(anchor="w", padx=15, pady=(5, 8))

        table_frame = tk.Frame(right, bg="#181c25")
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("id", "time", "object", "conf")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=22
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("time", text="Time")
        self.tree.heading("object", text="Object")
        self.tree.heading("conf", text="Conf.")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("time", width=105, anchor="center")
        self.tree.column("object", width=90, anchor="center")
        self.tree.column("conf", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def read_settings(self):
        try:
            confidence = float(self.conf_var.get().strip())
            if confidence > 1:
                confidence = confidence / 100.0

            if not 0.01 <= confidence <= 0.99:
                raise ValueError

            classes = [
                item.strip().lower()
                for item in self.classes_var.get().split(",")
                if item.strip()
            ]

            self.detector.set_settings(confidence, classes)
            self.conf_var.set(f"{confidence:.2f}")
            return True
        except ValueError:
            messagebox.showerror(
                "Invalid settings",
                "Confidence must be between 0.01 and 0.99.\n"
                "Example: 0.70 or 70"
            )
            return False

    def start_camera(self):
        if not self.read_settings():
            return

        self.camera = cv2.VideoCapture(config.CAMERA_INDEX)

        if not self.camera.isOpened():
            self.camera.release()
            self.camera = None
            messagebox.showerror(
                "Camera Error",
                "Could not open the webcam.\n\n"
                "Close other apps using the camera and try again."
            )
            self.status_var.set("Status: Camera unavailable")
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_var.set("Status: Detection running")
        self.fps_start = time.time()
        self.frame_count = 0
        self.update_frame()

    def stop_camera(self):
        self.running = False

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_var.set("Status: Camera stopped")

    def update_frame(self):
        if not self.running or self.camera is None:
            return

        success, frame = self.camera.read()

        if not success:
            self.stop_camera()
            messagebox.showerror("Camera Error", "Could not read a frame.")
            return

        frame = cv2.flip(frame, 1)
        annotated_frame, detections = self.detector.detect(frame)

        self.total_objects += len(detections)
        self.frame_count += 1

        elapsed = time.time() - self.fps_start
        if elapsed >= 1:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.fps_start = time.time()

        for detection in detections:
            object_class = detection["object_class"]
            current_time = time.time()
            last_time = self.last_log_time.get(object_class, 0)

            if current_time - last_time >= config.LOG_COOLDOWN_SECONDS:
                if log_detection(
                    object_class,
                    detection["confidence"],
                    detection["bbox"],
                ):
                    self.last_log_time[object_class] = current_time

        rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)

        max_w = max(self.video_label.winfo_width() - 20, 500)
        max_h = max(self.video_label.winfo_height() - 20, 400)
        image.thumbnail((max_w, max_h))

        self.photo = ImageTk.PhotoImage(image=image)
        self.video_label.configure(image=self.photo, text="")

        self.metric_var.set(
            f"Objects detected: {len(detections)}\n"
            f"FPS: {self.fps:.1f}\n"
            f"Threshold: {self.detector.confidence:.2f}\n"
            f"Filter: {', '.join(sorted(self.detector.classes)) or 'ALL'}"
        )

        if time.time() - self.last_db_refresh >= 2:
            self.refresh_logs()

        self.root.after(20, self.update_frame)

    def refresh_logs(self):
        rows = fetch_recent_logs(15)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            log_id, timestamp, object_class, confidence, x, y, w, h = row
            time_text = timestamp.strftime("%H:%M:%S") if timestamp else ""
            self.tree.insert(
                "",
                "end",
                values=(
                    log_id,
                    time_text,
                    object_class,
                    f"{float(confidence) * 100:.1f}%",
                ),
            )

        self.last_db_refresh = time.time()

    def close(self):
        self.stop_camera()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
