import os

ENABLE_VOICE = False   # set True later when you want mic commands

# -----MODE------
SIMULATION_MODE = True

# -----VISION-----
YOLO_MODEL = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5
CAMERA_INDEX = 0 #Uses Built in Webcam

# -----VOICE-----(vosk my boii)
VOSK_MODEL_PATH = os.path.join("assets", "models", "vosk-model-small-en-us-0.15")

# -----DISPLAY-----
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# ----ARM------
ARM_SERVO_PIN = 18
ARM_STEPPER_PINS = {"step": 19, "dir": 20, "enable": 21}

# -----HEADS-----
ACTIVE_HEAD = "camera"