from ultralytics import YOLO
import cv2


class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt", confidence=0.70, classes=None):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.classes = set(classes or [])

    def set_settings(self, confidence, classes):
        self.confidence = max(0.01, min(float(confidence), 0.99))
        self.classes = {
            item.strip().lower()
            for item in classes
            if item.strip()
        }

    def detect(self, frame):
        results = self.model(
            frame,
            conf=self.confidence,
            verbose=False
        )

        result = results[0]
        detections = []

        if result.boxes is None:
            return frame, detections

        names = result.names

        for box in result.boxes:
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            object_class = str(names[class_id]).lower()

            if self.classes and object_class not in self.classes:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            width = max(0, x2 - x1)
            height = max(0, y2 - y1)

            detections.append({
                "object_class": object_class,
                "confidence": confidence,
                "bbox": (x1, y1, width, height),
            })

            label = f"{object_class} {confidence * 100:.1f}%"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            text_y = max(y1 - 10, 20)
            cv2.rectangle(
                frame,
                (x1, text_y - 22),
                (x1 + max(150, len(label) * 9), text_y + 3),
                (0, 255, 0),
                -1,
            )
            cv2.putText(
                frame,
                label,
                (x1 + 5, text_y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

        return frame, detections
