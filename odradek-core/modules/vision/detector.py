import config

class Detector:

    def __init__(self):
        self.model = None
        self.cap = None
        try:
            from ultralytics import YOLO
            self.model = YOLO(config.YOLO_MODEL)
            print("YOLO model loaded babyy")
        except Exception as e:
            print(f"YOLO not found, usind dummy.")

        try:
            import cv2
            self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
            if not self.cap.isOpened():
                self.cap = None
                print("No camera - using blank frames")
        except Exception:
            self.cap = None
    def update(self):
        import numpy as np
        import cv2
        import time

        frame = None
        if self.cap is not None:
            ok, frame = self.cap.read()
            if not ok:
                frame = None

        detections = []
        if self.model is not None and frame is not None:
            results = self.model(frame, verbose=False)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    if conf >= config.CONFIDENCE_THRESHOLD:
                        detections.append({
                            "label": r.names[int(box.cls[0])],
                            "conf": conf,
                            "box": (x1, y1, x2, y2),
                            "center": ((x1 +x2) // 2, (y1+ y2) //2),
                        })
        else:
            x = int((time.time() *120) % (config.SCREEN_WIDTH -100)) +50
            detections.append({
                "label": "dummy_target",
                "conf": 0.9,
                "box": (x, 330, x +40, 370),
                "center": (x +20,350),
            })

        if frame is None:
            frame = np.zeros((240, 320, 3), dtype=np.uint8)
        return frame, detections