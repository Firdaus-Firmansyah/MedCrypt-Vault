# Implementation Plan & Engineering Checklist
## MedCrypt-Vault: Step-by-Step Build Roadmap (React 18 + shadcn/ui + FastAPI)

---

### 1. Phased Architecture Breakdown

Implementasi MedCrypt-Vault dibagi menjadi **9 Fase Terstruktur** untuk menjamin kode modular, bebas bug, dan siap didemonstrasikan di depan kelas dan dosen penguji.

```mermaid
gantt
    title Roadmap Eksekusi Proyek MedCrypt-Vault
    dateFormat  YYYY-MM-DD
    section Fase 1-3 (Core Engine)
    Fase 1: Inisialisasi & Scaffolding        :active, p1, 2026-11-21, 2d
    Fase 2: Engine Kompresi (LZ77 + Huffman) :p2, after p1, 3d
    Fase 3: Engine Keamanan (AES-GCM + KDF)   :p3, after p2, 2d
    section Fase 4-5 (Stego & Forensik)
    Fase 4: Engine Steganografi 2D-DWT        :p4, after p3, 4d
    Fase 5: Engine Forensik (PSNR, SSIM, χ²) :p5, after p4, 3d
    section Fase 6-7 (API & UI)
    Fase 6: Backend API Layer (FastAPI)       :p6, after p5, 3d
    Fase 7: Medical PACS Frontend UI (shadcn) :p7, after p6, 4d
    section Fase 8-9 (QA & Demo)
    Fase 8: Test Suite & Verifikasi BER 0%   :p8, after p7, 2d
    Fase 9: Paket Presentasi & Demo Script   :p9, after p8, 2d
```

---

### 2. Rincian Pekerjaan Tiap Fase (Checklist)

#### FASE 1: Inisialisasi Proyek & Scaffolding
- [ ] Buat struktur folder proyek monorepo modular di folder `TUGAS AKHIR/medcrypt-vault`:
  ```
  medcrypt-vault/
  ├── backend/
  │   ├── core/
  │   │   ├── compression/    # LZ77, Canonical Huffman, Shannon Entropy
  │   │   ├── security/       # AES-256-GCM, PBKDF2, Frame Header 90-byte
  │   │   ├── steganography/  # 2D-DWT, IDWT, QIM Embedder & Extractor
  │   │   └── metrics/        # MSE, PSNR, SSIM, Chi-Square Steganalysis
  │   ├── api/                # FastAPI routers, schemas, services
  │   ├── tests/              # Pytest unit & integration tests
  │   ├── sample_data/        # Sample medical X-Ray PNGs & dummy EHR JSONs
  │   ├── requirements.txt    # Python dependencies
  │   └── main.py             # FastAPI entry point
  ├── frontend/               # React 18 + Vite + Tailwind CSS + shadcn/ui
  │   ├── src/
  │   │   ├── components/
  │   │   │   ├── ui/         # Generated shadcn/ui primitives
  │   │   │   └── medical/    # Custom Medical PACS components (XRayViewer, etc.)
  │   │   ├── lib/            # utils.ts (cn helper), api.ts (Axios client)
  │   │   ├── hooks/          # useEncode, useExtract, useForensics
  │   │   └── App.tsx         # Main Workstation Shell
  │   ├── package.json
  │   ├── tailwind.config.js
  │   └── vite.config.ts
  ├── docs/                   # Spesifikasi lengkap (PRD, TRD, APP_FLOW, dll.)
  └── run_system.py           # Unified launcher (starts backend & frontend)
  ```
- [ ] Siapkan Python virtual environment (`venv`) dengan pustaka:
  `numpy`, `PyWavelets`, `opencv-python-headless`, `cryptography`, `pydantic`, `fastapi`, `uvicorn`, `pytest`.
- [ ] Inisialisasi Frontend dengan Node.js (Vite + React + TypeScript):
  `npm create vite@latest frontend -- --template react-ts`

---

#### FASE 2: Core Compression & Entropy Engine (Pure Python)
- [ ] **Modul `entropy.py`:**
  - Fungsi `calculate_entropy(data: bytes) -> float` berbasis rumus Shannon.
  - Fungsi `calculate_image_entropy(image: np.ndarray) -> float`.
- [ ] **Modul `lz77.py`:**
  - Implementasi *Sliding Window* dengan Hash-Chaining untuk mencari *Longest Common Match*.
  - Parameter: $W_s = 32.768\text{ byte}$ (search buffer), $W_l = 256\text{ byte}$ (lookahead buffer), minimum match = 3 byte.
  - Fungsi `compress(raw_bytes: bytes) -> list[Token]`.
  - Fungsi `decompress(tokens: list[Token]) -> bytes`.
- [ ] **Modul `huffman.py`:**
  - Membangun *Min-Heap Priority Queue* berdasarkan frekuensi kemunculan token LZ77.
  - Memverifikasi aturan *Prefix Property* secara matematis.
  - Mengonversi pohon ke format *Canonical Huffman* untuk efisiensi serialisasi bitstream.
  - Bit-packer dan bit-unpacker untuk pembungkusan byte presisi tinggi.

---

#### FASE 3: Cryptographic & Binary Framing Engine
- [ ] **Modul `cipher.py`:**
  - Penurunan kunci dengan `PBKDF2HMAC` (SHA-256, 600.000 iterasi, 16-byte salt acak).
  - Enkripsi dan dekripsi menggunakan `AESGCM` (256-bit key, 12-byte nonce acak, 16-byte authentication tag).
- [ ] **Modul `framing.py`:**
  - Pembentukan paket biner 90-byte: Magic byte (`MCVT`), salt, nonce, compressed_size, original_size, auth_tag, SHA-256 hash.
  - Parser dan validator frame biner pada saat ekstraksi.

---

#### FASE 4: Medical Steganography Engine (2D-DWT)
- [ ] **Modul `dwt.py`:**
  - Fungsi transformasi 2D Haar DWT menghasilkan matriks sub-band $LL, LH, HL, HH$.
  - Fungsi rekonstruksi 2D Inverse DWT (IDWT) dengan pemotongan rentang $[0, 255]$ dan pembulatan uint8.
- [ ] **Modul `embedder.py`:**
  - Pemeriksa kapasitas (*Capacity Pre-Check*): Memastikan panjang payload biner $\le \text{panjang koefisien}(LH + HL)$.
  - Penyisipan adaptif dengan *Quantization Index Modulation (QIM)* pada sub-band $LH$ dan $HL$.
  - Proteksi penuh sub-band $LL$ agar tidak diubah sama sekali.
- [ ] **Modul `extractor.py`:**
  - Ekstraksi urutan bit dari koefisien sub-band $LH$ dan $HL$ citra stego.
  - Deteksi magic byte dan parsing frame payload biner.

---

#### FASE 5: Forensic & Quality Analytics Engine
- [ ] **Modul `quality.py`:**
  - Perhitungan Mean Squared Error (MSE).
  - Perhitungan Peak Signal-to-Noise Ratio (PSNR) dengan validasi $PSNR > 40\text{ dB}$.
  - Perhitungan Structural Similarity Index (SSIM) menggunakan jendela Gaussian $11 \times 11$.
  - Perhitungan Bit Error Rate (BER): Membandingkan bit asli vs bit terekskrak (target: $BER = 0.00\%$).
- [ ] **Modul `steganalysis.py`:**
  - Algoritma uji statistik $\chi^2$ (Chi-Square) pada histogram pasangan nilai piksel (PoVs).
  - Kalkulasi nilai $p\text{-value}$ dan derajat kebebasan (*degrees of freedom*).
  - Pembuatan peta selisih citra (*Amplified Difference Map* $|I - I'| \times 20$).

---

#### FASE 6: Backend Service & REST API Layer (FastAPI)
- [ ] Buat skema Pydantic v2 untuk formulir rekam medis pasien (`PatientRecordSchema`).
- [ ] Endpoint `POST /api/v1/pipeline/encode`: Menerima berkas citra medis, formulir rekam medis JSON, dan passphrase $\to$ menghasilkan citra stego PNG + metrik kompresi & kualitas.
- [ ] Endpoint `POST /api/v1/pipeline/extract`: Menerima berkas citra stego dan passphrase $\to$ mengembalikan JSON rekam medis utuh.
- [ ] Endpoint `POST /api/v1/forensics/compare`: Menerima citra cover & stego $\to$ mengembalikan data JSON kurva Chi-square, SSIM, PSNR, dan peta selisih citra.
- [ ] Endpoint `GET /api/v1/system/health`: Memeriksa status kesehatan server backend dan alokasi memori.

---

#### FASE 7: Interactive Medical PACS Frontend UI (shadcn/ui + Tailwind CSS)
- [ ] Konfigurasi Tailwind CSS dan Tailwind Animate pada proyek React Vite.
- [ ] Inisialisasi shadcn/ui dengan CLI:
  `npx shadcn@latest init`
- [ ] Pasang komponen shadcn/ui yang diperlukan:
  `npx shadcn@latest add button card tabs slider badge progress dialog sonner table input label textarea separator tooltip`
- [ ] Pasang pustaka pendukung UI:
  `npm install lucide-react recharts clsx tailwind-merge axios`
- [ ] Susun layout workstation medis:
  - Header dengan status backend dan navigasi tab.
  - Tab 1: Workflow Encode & Embed (Upload X-Ray, input formulir pasien, meteran kompresi, tombol eksekusi, unduh stego).
  - Tab 2: Workflow Extract & Restore (Upload stego, PIN dokter, dialog resume rekam medis pasien).
  - Tab 3: Forensic Lab (Slider perbandingan citra asli vs stego, visualizer 4 kuadran DWT, grafik interaktif Chi-Square & histogram Recharts).

---

#### FASE 8: Comprehensive Verification & Test Suite
- [ ] Uji coba otomatis via `pytest` mencakup:
  - 100% test pass pada kompresi-dekompresi LZ77 dan Huffman untuk berbagai jenis berkas teks.
  - Uji kekebalan enkripsi AES-GCM terhadap salah kunci (harus melempar exception otentikasi).
  - Uji round-trip embedding dan ekstraksi pada citra rontgen resolusi $512 \times 512$, $1024 \times 1024$, dan $2048 \times 2048$.
  - Verifikasi bahwa Bit Error Rate (**BER = 0.00%**) dan checksum SHA-256 cocok 100%.
  - Verifikasi bahwa rata-rata skor **PSNR $> 40\text{ dB}$** dan **SSIM $> 0.990$**.

---

#### FASE 9: Academic Presentation Package
- [ ] Siapkan dataset sampel citra radiologi (Chest X-Ray, Brain MRI, Dental X-Ray).
- [ ] Susun skrip panduan live demonstrasi untuk sesi presentasi di depan dosen dan kelas.
- [ ] Siapkan draf laporan akhir dan slide presentasi pendukung.
