"""MedCrypt-Vault FastAPI Backend Application Entrypoint.

Exposes RESTful endpoints for:
- Medical record compression & embedding pipeline
- Stego-image extraction & authentication pipeline
- Forensic & steganalysis analytics (PSNR, SSIM, Chi-Square)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.compression.pipeline import compress_payload, decompress_payload

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


class CompressRequest(BaseModel):
    data: str


class CompressResponse(BaseModel):
    original_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float
    space_saving_percent: float
    original_entropy: float
    compressed_entropy: float
    hex_preview: str


@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "MedCrypt-Vault Backend",
        "version": "1.0.0",
        "supported_codecs": ["Pure LZ77", "Canonical Huffman", "AES-256-GCM", "Haar 2D-DWT"],
    }


@app.post("/api/v1/compress", response_model=CompressResponse, tags=["Compression"])
async def compress_text(req: CompressRequest):
    """Compresses arbitrary text or JSON payload using pure LZ77 + Canonical Huffman."""
    try:
        raw_bytes = req.data.encode("utf-8")
        if not raw_bytes:
            raise HTTPException(status_code=400, detail="Payload cannot be empty.")
        compressed, metrics = compress_payload(raw_bytes)
        return {
            **metrics,
            "hex_preview": compressed[:32].hex(" ").upper(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
