"""MedCrypt-Vault FastAPI Backend Application Entrypoint.

Exposes RESTful endpoints for:
- Medical record compression & embedding pipeline
- Stego-image extraction & authentication pipeline
- Forensic & steganalysis analytics (PSNR, SSIM, Chi-Square)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MedCrypt-Vault API",
    description="Medical EHR Compression & Frequency-Domain Steganography Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local Vite development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "MedCrypt-Vault Backend",
        "version": "1.0.0",
        "supported_codecs": ["Pure LZ77", "Canonical Huffman", "AES-256-GCM", "Haar 2D-DWT"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
