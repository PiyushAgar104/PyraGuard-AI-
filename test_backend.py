import cv2
import numpy as np
import os
from detector import FireDetector

def test_fire_detector():
    print("[TEST] Initializing FireDetector...")
    detector = FireDetector(model_path="models/best.pt")
    
    # Create a synthetic image with a fire-like bright red/orange region
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # Background dark gradient
    img[:, :] = (30, 25, 20)
    # Draw fire region (bright yellow/orange/red flame center)
    cv2.ellipse(img, (320, 240), (80, 120), 0, 0, 360, (0, 165, 255), -1) # Orange
    cv2.ellipse(img, (320, 240), (50, 80), 0, 0, 360, (0, 230, 255), -1) # Bright yellow core

    annotated, detections, fire_detected, total_dets, max_conf, infer_ms = detector.predict_frame(img, conf_threshold=0.3)
    
    print(f"Fire Detected: {fire_detected}")
    print(f"Total Detections: {total_dets}")
    print(f"Max Confidence: {max_conf}")
    print(f"Inference Time: {infer_ms} ms")
    print(f"Detections details: {detections}")

    assert fire_detected, "Fire should be detected in synthetic flame image!"
    assert total_dets > 0, "Detections count should be greater than 0"
    print("[SUCCESS] FireDetector unit test passed!")

if __name__ == "__main__":
    test_fire_detector()
