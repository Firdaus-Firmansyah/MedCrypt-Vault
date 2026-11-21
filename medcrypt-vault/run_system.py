"""Unified Single-Command Launcher for MedCrypt-Vault.

Orchestrates running:
- Python FastAPI Backend (Port 8000)
- React Vite Medical PACS Frontend (Port 5173)
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"


def run_services():
    print("=" * 70)
    print(" 🏥 MEDCRYPT-VAULT: Medical EHR Compression & Steganography Platform")
    print("=" * 70)

    # 1. Start FastAPI Backend
    print("[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=str(BACKEND_DIR),
    )

    # 2. Check frontend
    print("[2/2] Checking Frontend environment...")
    frontend_proc = None
    if (FRONTEND_DIR / "package.json").exists():
        print("Starting React Vite Frontend on http://localhost:5173 ...")
        frontend_proc = subprocess.Popen(["npm", "run", "dev"], cwd=str(FRONTEND_DIR), shell=True)

    print("\n[SUCCESS] MedCrypt-Vault services running.")
    print("  - Backend API & Docs: http://127.0.0.1:8000/docs")
    print("  - Frontend PACS UI:   http://localhost:5173")
    print("\nPress Ctrl+C to terminate all services.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping MedCrypt-Vault services...")
        backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        print("Services stopped.")


if __name__ == "__main__":
    run_services()
