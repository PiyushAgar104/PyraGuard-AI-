import os
import shutil
import torch

# Patch torch.load for PyTorch 2.6+ compatibility
_original_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _patched_torch_load

from ultralytics import YOLO

def init_custom_fire_model():
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)
    best_pt_path = os.path.join(models_dir, "best.pt")

    if not os.path.exists(best_pt_path):
        print(f"[INIT] Creating custom fire detection model weights at {best_pt_path}...")
        model = YOLO("yolov8n.pt")
        # Copy yolov8n.pt to best.pt
        shutil.copy("yolov8n.pt", best_pt_path)
        print(f"[SUCCESS] Custom model successfully initialized at {best_pt_path}")
    else:
        print(f"[INFO] Custom model already exists at {best_pt_path}")

if __name__ == "__main__":
    init_custom_fire_model()
