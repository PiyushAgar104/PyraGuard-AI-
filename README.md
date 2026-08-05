# 🔥 PyraGuard AI – Real-Time Fire Detection System

PyraGuard AI is a real-time fire detection system powered by **YOLOv8** and **OpenCV**. It detects fire from **images, videos, and live webcam streams** with high-speed inference through a modern web interface.

---

## 🚀 Features

* 🔥 Real-Time Fire Detection
* 📸 Image Detection
* 🎥 Video Detection
* 📹 Live Webcam Detection
* 🎯 Bounding Boxes with Confidence Scores
* ⚡ Fast YOLOv8 Inference
* 🌐 FastAPI REST API
* 💻 React + Vite Frontend
* 🎨 Responsive UI with Tailwind CSS
* 💾 Download Detection Results

---

## 🛠️ Tech Stack

### AI & Backend

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* FastAPI

### Frontend

* React
* Vite
* Tailwind CSS

---

## 📂 Project Structure

```text
PyraGuard-AI/
│
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── routes.py
│   ├── uploads/
│   ├── outputs/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   └── best.pt
│
├── screenshots/
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/PyraGuard-AI.git
cd PyraGuard-AI
```

### Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

uvicorn app:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## 📸 Supported Inputs

* ✅ Images (.jpg, .png, .jpeg)
* ✅ Videos (.mp4, .avi, .mov)
* ✅ Live Webcam

---

## 🎯 Model

This project uses a custom-trained **YOLOv8** model (`best.pt`) for fire detection.

---

## 📷 Demo

Add screenshots or GIFs inside the `screenshots/` folder and display them here.

Example:

```markdown
![Home](screenshots/home.png)

![Detection](screenshots/detection.png)
```

---

## 🔮 Future Improvements

* SMS & Email Alerts
* Push Notifications
* Multi-Camera Monitoring
* Cloud Deployment
* Firebase Integration
* Detection History Dashboard

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Piyush Agar**

If you found this project useful, consider giving it a ⭐ on GitHub.

Happy Coding! 🚀
