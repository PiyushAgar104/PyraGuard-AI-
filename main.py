import os
import cv2
import uuid
import time
import base64
import numpy as np
from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from detector import FireDetector

app = FastAPI(
    title="AI Fire Detection API",
    description="Real-Time Fire Detection System using YOLOv8 & OpenCV",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Mount outputs directory for static serving
app.mount("/static_outputs", StaticFiles(directory=OUTPUTS_DIR), name="static_outputs")

# Initialize Detector
model_path = os.path.join(MODELS_DIR, "best.pt")
detector = FireDetector(model_path=model_path)


@app.get("/health")
def health_check():
    """System health check endpoint."""
    return {
        "status": "online",
        "model_loaded": detector.model is not None,
        "model_path": model_path,
        "timestamp": time.time()
    }


@app.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    confidence: float = Query(0.35, ge=0.05, le=0.95)
):
    """
    Fire detection endpoint for uploaded images.
    Returns annotated image in base64, detection count, confidence score, and download URL.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file format.")

    # Process image
    annotated_img, detections, fire_detected, total_dets, max_conf, infer_ms = detector.predict_frame(
        image, conf_threshold=confidence
    )

    # Save output image
    filename = f"fire_det_{uuid.uuid4().hex[:8]}.jpg"
    output_path = os.path.join(OUTPUTS_DIR, filename)
    cv2.imwrite(output_path, annotated_img)

    # Encode image to base64 for direct browser rendering
    _, buffer = cv2.imencode(".jpg", annotated_img)
    base64_image = base64.b64encode(buffer).decode("utf-8")

    return {
        "status": "success",
        "filename": filename,
        "fire_detected": fire_detected,
        "total_detections": total_dets,
        "max_confidence": max_conf,
        "inference_time_ms": infer_ms,
        "detections": detections,
        "annotated_image": f"data:image/jpeg;base64,{base64_image}",
        "download_url": f"/download/outputs/{filename}"
    }


@app.post("/webcam")
async def predict_webcam(
    file: UploadFile = File(None),
    frame_data: str = Form(None),
    confidence: float = Form(0.35)
):
    """
    Real-time webcam frame prediction endpoint.
    Accepts image file upload or base64 frame string.
    """
    image = None

    if file is not None:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif frame_data is not None:
        if "," in frame_data:
            frame_data = frame_data.split(",")[1]
        img_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid webcam frame input.")

    annotated_img, detections, fire_detected, total_dets, max_conf, infer_ms = detector.predict_frame(
        image, conf_threshold=confidence
    )

    _, buffer = cv2.imencode(".jpg", annotated_img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    base64_image = base64.b64encode(buffer).decode("utf-8")

    return {
        "fire_detected": fire_detected,
        "total_detections": total_dets,
        "max_confidence": max_conf,
        "inference_time_ms": infer_ms,
        "detections": detections,
        "annotated_frame": f"data:image/jpeg;base64,{base64_image}"
    }


@app.post("/video")
async def predict_video(
    file: UploadFile = File(...),
    confidence: float = Query(0.35, ge=0.05, le=0.95)
):
    """
    Video fire detection endpoint.
    Processes video frame-by-frame, annotates fire detections, and returns output video details.
    """
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a video.")

    input_filename = f"upload_{uuid.uuid4().hex[:8]}.mp4"
    input_path = os.path.join(UPLOADS_DIR, input_filename)

    with open(input_path, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Failed to open video file.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    output_filename = f"fire_video_{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(OUTPUTS_DIR, output_filename)

    # Use mp4v codec for broad compatibility
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = 0
    fire_frames_count = 0
    max_confidence = 0.0
    total_detections_count = 0
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        annotated, dets, fire_det, num_dets, conf, _ = detector.predict_frame(
            frame, conf_threshold=confidence
        )

        if fire_det:
            fire_frames_count += 1
            total_detections_count += num_dets
            if conf > max_confidence:
                max_confidence = conf

        out.write(annotated)

    cap.release()
    out.release()

    total_processing_sec = round(time.time() - start_time, 2)

    return {
        "status": "success",
        "output_filename": output_filename,
        "total_frames": total_frames,
        "fire_frames_detected": fire_frames_count,
        "total_fire_detections": total_detections_count,
        "max_confidence": max_confidence,
        "processing_time_sec": total_processing_sec,
        "download_url": f"/download/outputs/{output_filename}"
    }


@app.get("/download/{folder}/{filename}")
def download_file(folder: str, filename: str):
    """File download endpoint."""
    if folder == "outputs":
        target_dir = OUTPUTS_DIR
    elif folder == "uploads":
        target_dir = UPLOADS_DIR
    else:
        raise HTTPException(status_code=400, detail="Invalid folder specified.")

    file_path = os.path.join(target_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path, filename=filename)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
