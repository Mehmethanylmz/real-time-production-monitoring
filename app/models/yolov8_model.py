from ultralytics import YOLO
import cv2

# Modeli yükle
model = YOLO('saved_models/best.pt')  # küçük model, hızlı

def detect_with_yolo(img):
    results = model.predict(img, imgsz=640, conf=0.5)
    
    # Görüntü üstüne kutuları çiz
    annotated_frame = results[0].plot()

    return annotated_frame