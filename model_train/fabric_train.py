# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 23:41:06 2025

@author: Mete
"""


from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO('yolov8s.pt')
    model.train(
        data="C:/Users/Mete/Desktop/fabric2.v1i.yolov8/data.yaml",
        epochs=50,
        batch=32,
        imgsz=640,
        device=0,
        workers=6,
        name="fabric_detect",
        project="runs/detect",
        pretrained=True
    )
