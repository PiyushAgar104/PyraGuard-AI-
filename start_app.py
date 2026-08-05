import subprocess
import sys
import time
import os

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    print("[STARTUP] Launching PyraGuard AI Fire Detection System...")
    print("=" * 60)
    print("Backend API URL  : http://localhost:8000")
    print("Frontend App URL : http://localhost:5173")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 60)

    # 1. Start FastAPI Backend Server
    print("\n[1/2] Starting FastAPI Backend on http://localhost:8000...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=backend_dir
    )

    time.sleep(2)

    # 2. Start Vite Frontend Server
    print("[2/2] Starting Vite Frontend on http://localhost:5173...")
    frontend_process = subprocess.Popen(
        "npx vite",
        shell=True,
        cwd=frontend_dir
    )

    print("\n[SUCCESS] Systems operational! Open http://localhost:5173 in your browser.")
    print("Press Ctrl+C to stop both servers.")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping processes...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
