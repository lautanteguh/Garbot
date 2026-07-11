# Setting environment behaviour for OpenCV
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import requests
import time
from ultralytics import YOLO

# Load model
model = YOLO("YOLOV.pt")

ESP32_IP = "LOCAL_ESP32_IP"  # change this

cap = cv2.VideoCapture(0)

last_sent = ""
last_time = 0
cooldown = 3  # seconds

VALID_LABELS = ["organic", "inorganic", "metal"]

def send_command(label):
    try:
        url = f"http://{ESP32_IP}/{label}"
        requests.get(url, timeout=1)
        print("Sent:", label)
    except:
        print("ESP32 not reachable")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Optional: reduce lag
    frame = cv2.resize(frame, (640, 480))

    results = model(frame)
    annotated_frame = results[0].plot()

    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])

            # convert to lowercase
            label = model.names[cls_id].lower()

            print("Detected:", label)

            if label in VALID_LABELS:
                now = time.time()

                if label != last_sent or (now - last_time > cooldown):
                    send_command(label)
                    last_sent = label
                    last_time = now

                break

    cv2.imshow("YOLO Live", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()