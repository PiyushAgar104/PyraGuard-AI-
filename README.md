🔥 PyraGuard AI - Real-Time Fire Detection System
PythonYOLOv8FastAPIOpenCVReactViteTailwind CSS
License

An enterprise-grade, high-performance AI Fire Detection System powered by YOLOv8, OpenCV, FastAPI, and React + Vite with Tailwind CSS. It delivers real-time fire detection across uploaded images, recorded videos, and live webcam streams with red bounding box overlays, confidence score metrics, visual alerts, and AI Voiceover speech warnings.

✨ Features
📸 Image Fire Detection: Drag & drop upload for high-resolution images with side-by-side original vs annotated bounding box comparison and image download.
🎥 Video Fire Detection: Frame-by-frame video processing with interactive browser video playback showing bounding box overlays and video download.
📹 Live Webcam Stream: Low-latency, high-FPS webcam fire detection powered by continuous canvas stream analysis.
🟥 Bounding Box Overlays: Draws bright red bounding boxes ((0, 0, 255)) with class labels and confidence percentages around detected fire regions.
📢 AI Voiceover Alerts: Integrated Web Speech Synthesis that speaks "Warning! Emergency fire hazard detected!" when a flame signature exceeds the threshold.
🔔 Visual & Sound Alarms: Pulsing red alert banner and Web Audio API tone synth.
🎚️ Dynamic Threshold Slider: Interactive confidence threshold control (10% to 95%) to adjust detection sensitivity in real time.
📊 Real-Time Metrics: Live statistics including total fire detections, max confidence score, FPS counter, and inference latency.
🌙 Modern Dark-Themed UI: Futuristic cyberpunk glassmorphism layout with Lucide icons.
🛠️ Tech Stack
Layer	Technologies Used
Artificial Intelligence	YOLOv8 (Ultralytics), PyTorch, OpenCV, NumPy
Backend REST API	Python 3.10+, FastAPI, Uvicorn, Python-Multipart
Frontend UI	React 18, Vite, Tailwind CSS, Lucide Icons, Axios
Audio & Speech	Web Speech Synthesis API, Web Audio API
📁 Repository Structure
text

fire-detection-system/
├── backend/
│   ├── main.py              # FastAPI server routes (/predict, /video, /webcam, /download)
│   ├── detector.py          # YOLOv8 & OpenCV fire detection engine & hybrid HSV detector
│   ├── init_model.py        # Custom YOLOv8 model initializer & weights generator (best.pt)
│   ├── test_backend.py      # Unit test script for detection pipeline
│   ├── requirements.txt     # Python backend dependencies
│   ├── models/              # Saved YOLO model weights (best.pt)
│   ├── uploads/             # Temporary folder for input files
│   └── outputs/             # Export directory for processed images & videos
│
├── frontend/
│   ├── index.html           # HTML5 document root
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite build & proxy settings
│   ├── tailwind.config.js   # Dark theme cyberpunk styles
│   └── src/
│       ├── main.jsx         # React DOM entrypoint
│       ├── App.jsx          # Dashboard layout & tab router
│       ├── index.css        # Global CSS & glassmorphism utilities
│       ├── services/
│       │   └── api.js       # Axios client pointing to http://localhost:8000
│       └── components/
│           ├── Navbar.jsx           # Top navigation bar & server status
│           ├── ImageUpload.jsx      # Image upload workspace & download
│           ├── VideoUpload.jsx      # Video upload & frame processing
│           ├── WebcamStream.jsx     # Live webcam stream & real-time canvas
│           ├── DetectionAlert.jsx   # Visual alert banner & AI voiceover
│           ├── StatsCard.jsx        # Metric counter grid
│           └── ThresholdSlider.jsx  # Confidence threshold slider
│
├── start_app.py             # Single-command launcher for backend & frontend
└── README.md                # Documentation
🚀 Quick Start & Installation
Prerequisites
Python 3.10+ installed
Node.js 18+ and npm installed
1. Clone the Repository
bash

git clone https://github.com/your-username/fire-detection-system.git
cd fire-detection-system
2. Set Up Backend (FastAPI + YOLOv8)
bash

cd backend
pip install -r requirements.txt
python init_model.py
3. Set Up Frontend (React + Vite)
bash

cd ../frontend
npm install
💻 Running the Application
Option 1: Single-Command Launch (Recommended)
Run the universal startup script from the project root:

bash

python start_app.py
Option 2: Run Servers Separately
Start Backend Server:

bash

cd backend
python main.py
# Backend runs at: http://localhost:8000
# OpenAPI Docs at: http://localhost:8000/docs
Start Frontend Server:

bash

cd frontend
npm run dev
# Frontend runs at: http://localhost:5173
📡 API Reference Endpoint Documentation
Method	Endpoint	Description	Payload / Query
GET	/health	Server health check and model status	N/A
POST	/predict	Image fire detection	file (image), confidence (float 0.1-0.95)
POST	/video	Video fire processing	file (video), confidence (float 0.1-0.95)
POST	/webcam	Real-time webcam frame prediction	frame_data (base64 string or file), confidence
GET	/download/{folder}/{filename}	Download processed image or video	Path variables
Sample Response (POST /predict):
json

{
  "status": "success",
  "filename": "fire_det_8a12b3c4.jpg",
  "fire_detected": true,
  "total_detections": 2,
  "max_confidence": 0.92,
  "inference_time_ms": 18.5,
  "detections": [
    {
      "box": [230, 110, 410, 350],
      "confidence": 0.92,
      "label": "FIRE"
    }
  ],
  "annotated_image": "data:image/jpeg;base64,...",
  "download_url": "/download/outputs/fire_det_8a12b3c4.jpg"
}
📄 License
Distributed under the MIT License. See LICENSE for more information.

⭐ If you find this project helpful, please consider giving it a star on GitHub! ⭐
