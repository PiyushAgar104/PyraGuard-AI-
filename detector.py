import os
import cv2
import numpy as np
import time
import torch

# Monkey patch torch.load for PyTorch 2.6+ compatibility with Ultralytics models
_original_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _patched_torch_load

from ultralytics import YOLO

class FireDetector:
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "models", "best.pt")
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        """Load custom YOLOv8 model if available, else fall back to yolov8n.pt with hybrid fire detection."""
        try:
            if os.path.exists(self.model_path):
                print(f"[INFO] Loading custom YOLOv8 model from {self.model_path}...")
                self.model = YOLO(self.model_path)
            else:
                print(f"[INFO] Custom model {self.model_path} not found. Loading YOLOv8 default model (yolov8n.pt)...")
                self.model = YOLO("yolov8n.pt")
        except Exception as e:
            print(f"[WARNING] Error loading YOLO model: {e}. Falling back to lightweight HSV detector.")
            self.model = None

    def detect_fire_hsv(self, image):
        """
        HSV-based fire region detection for flame/fire color analysis.
        Detects bright yellow/orange/red flame signatures.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define HSV range for fire/flame colors (yellow, orange, intense red)
        lower_fire1 = np.array([0, 80, 190], dtype=np.uint8)
        upper_fire1 = np.array([35, 255, 255], dtype=np.uint8)
        
        lower_fire2 = np.array([170, 80, 190], dtype=np.uint8)
        upper_fire2 = np.array([180, 255, 255], dtype=np.uint8)
        
        mask1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
        mask2 = cv2.inRange(hsv, lower_fire2, upper_fire2)
        fire_mask = cv2.bitwise_or(mask1, mask2)
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
        fire_mask = cv2.dilate(fire_mask, kernel, iterations=2)
        
        contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        h_img, w_img = image.shape[:2]
        min_area = (h_img * w_img) * 0.0008
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(cnt)
                roi_mask = fire_mask[y:y+h, x:x+w]
                fire_density = np.sum(roi_mask > 0) / (w * h)
                
                if fire_density > 0.25:
                    roi_hsv = hsv[y:y+h, x:x+w]
                    avg_val = np.mean(roi_hsv[:, :, 2]) / 255.0
                    conf = round(float(min(0.99, 0.45 + (fire_density * 0.3) + (avg_val * 0.25))), 2)
                    detections.append({
                        "box": [int(x), int(y), int(x + w), int(y + h)],
                        "confidence": conf,
                        "label": "FIRE"
                    })
        return detections

    def predict_frame(self, frame, conf_threshold=0.35):
        """
        Run inference on a single frame.
        Returns:
            annotated_frame (numpy array)
            detections (list of dicts)
            fire_detected (bool)
            total_detections (int)
            max_confidence (float)
            inference_time_ms (float)
        """
        start_time = time.time()
        detections = []
        
        if frame is None or frame.size == 0:
            return frame, [], False, 0, 0.0, 0.0

        h, w = frame.shape[:2]

        # 1. Run YOLO inference if model loaded
        if self.model is not None:
            try:
                results = self.model.predict(frame, conf=conf_threshold, verbose=False)
                for r in results:
                    for box in r.boxes:
                        c_id = int(box.cls[0])
                        cls_name = self.model.names.get(c_id, "").lower()
                        conf = float(box.conf[0])

                        if "fire" in cls_name or "smoke" in cls_name or c_id == 0 or conf >= conf_threshold:
                            xyxy = box.xyxy[0].cpu().numpy().astype(int)
                            detections.append({
                                "box": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
                                "confidence": round(conf, 2),
                                "label": "FIRE" if "fire" in cls_name or c_id == 0 else cls_name.upper()
                            })
            except Exception as e:
                pass

        # 2. Hybrid HSV detection boost if no specific YOLO fire detections found
        if len(detections) == 0:
            hsv_detections = self.detect_fire_hsv(frame)
            for d in hsv_detections:
                if d["confidence"] >= conf_threshold:
                    detections.append(d)

        # 3. Draw bounding boxes on annotated frame
        annotated_frame = frame.copy()
        fire_detected = False
        max_confidence = 0.0

        for det in detections:
            conf = det["confidence"]
            if conf >= conf_threshold:
                fire_detected = True
                if conf > max_confidence:
                    max_confidence = conf

                x1, y1, x2, y2 = det["box"]

                # Draw red bounding box (BGR: 0, 0, 255)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

                # Label background & text
                label_text = f"FIRE {int(conf * 100)}%"
                (text_w, text_h), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                
                cv2.rectangle(
                    annotated_frame, 
                    (x1, max(0, y1 - text_h - 10)), 
                    (x1 + text_w + 10, max(text_h + 10, y1)), 
                    (0, 0, 180), 
                    -1
                )
                
                cv2.putText(
                    annotated_frame, 
                    label_text, 
                    (x1 + 5, max(text_h + 2, y1 - 5)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.65, 
                    (255, 255, 255), 
                    2
                )

        # Top alert banner
        if fire_detected:
            alert_text = f"CRITICAL ALERT: FIRE DETECTED ({len(detections)} ACTIVE DETECTIONS)"
            cv2.rectangle(annotated_frame, (0, 0), (w, 40), (0, 0, 200), -1)
            cv2.putText(
                annotated_frame, 
                alert_text, 
                (20, 28), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (255, 255, 255), 
                2
            )

        inference_time_ms = round((time.time() - start_time) * 1000, 2)

        return (
            annotated_frame,
            detections,
            fire_detected,
            len(detections),
            round(max_confidence, 2),
            inference_time_ms
        )
