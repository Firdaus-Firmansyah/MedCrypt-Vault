# MedCrypt-Vault 🏥🔒
### Medical Electronic Health Record Compression & Frequency-Domain Steganography Platform

> **Proyek Tugas Akhir Mata Kuliah:** Teknik Kompresi dan Penyamaran Data (TK-PD) — Kelas 7A  
> **Institusi:** Program Studi Teknik Informatika, Fakultas Teknologi Industri dan Informatika (FTII), Universitas Muhammadiyah Prof. DR. HAMKA (UHAMKA)  
> **Dosen Pengampu:** Ir. Dimas Febriawan, S.Kom., M.T.I.  
> **Target Capaian:** Nilai Sempurna (100 Poin) sesuai Rubrik RTM

---

## 📌 Ringkasan Eksekutif Proyek

**MedCrypt-Vault** adalah sistem workstation rekam medis dan radiologi aman yang dirancang untuk fasilitas kesehatan modern. Platform ini mengintegrasikan dua pilar utama mata kuliah secara harmonis:
1. **Pilar Kompresi Data (Modul 1, 2, 3, 4, 5, 6):**
   - Algoritma hibrida **LZ77 (Sliding Window Dictionary Transform)** + **Canonical Huffman Coding**, memangkas ukuran riwayat medis pasien sebesar **50% – 70%**.
   - Evaluasi batas teoritis entropi via **Shannon Entropy**.
2. **Pilar Penyamaran Data (Modul 9 & Tugas Presentasi):**
   - **Steganografi 2D Discrete Wavelet Transform (2D-DWT)** pada domain frekuensi sub-band $LH$ dan $HL$.
   - Menyembunyikan seluruh berkas rekam medis terenkripsi (**AES-256-GCM**) langsung di dalam citra rontgen medis (Chest X-Ray / Brain MRI / Dental).
3. **Kualitas Klinis & Forensik:**
   - Rekonstruksi citra stego mencapai **PSNR > 40 dB** dan **SSIM > 0.990** (bebas distorsi kasat mata, anatomi organ vital pada sub-band $LL$ 100% terlindungi).
   - Lolos dari audit uji steganalsis statistik **Chi-Square ($\chi^2$, $p > 0.05$)**.
4. **Antarmuka Medis Berstandar Industri:**
   - Dibangun menggunakan **React 18 + Vite + TypeScript + Tailwind CSS** dan pustaka komponen berstandar profesional **[shadcn/ui](https://ui.shadcn.com/)** (Radix UI primitives).

---

## 🛠️ Tech Stack Arsitektur

- **Backend / Core Engine:**
  - Bahasa: Python 3.12 (Algoritma murni / *Pure Python* tanpa library instan *blackbox*)
  - Komputasi & Sinyal: `numpy` (vektorisasi matriks), `PyWavelets` (dekomposisi Haar 2D-DWT), `opencv-python-headless`
  - Keamanan: `cryptography` (AES-256-GCM, PBKDF2 with HMAC-SHA-256, 600.000 iterasi)
  - Web API: `fastapi` & `uvicorn` (skema Pydantic v2, RESTful, OpenAPI doc)
- **Frontend / Medical Workstation UI:**
  - Framework: `React 18` + `TypeScript` + `Vite`
  - Design System: `Tailwind CSS` + **`shadcn/ui`** (Tabs, Cards, Sliders, Badges, Progress, Dialogs, Sonner Toasts, Tables)
  - Visualisasi & Ikonografi: `Recharts` (grafik Chi-Square & histogram interaktif), `lucide-react`

---

## 📚 Dokumentasi Spesifikasi Arsitektur Lengkap

Seluruh dokumen rekayasa perangkat lunak telah disusun secara komprehensif di dalam folder [`docs/`](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/):

| Dokumen | Deskripsi & Isi Utama |
| :--- | :--- |
| 📄 **[PRD.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/PRD.md)** | **Product Requirements Document:** Visi produk, profil pengguna, 5 fitur inti berstandar shadcn/ui, matriks pemenuhan nilai 100 rubrik RTM. |
| 📄 **[TRD.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/TRD.md)** | **Technical Requirements Document:** Arsitektur teknis C4, rumus matematis (Entropi, LZ77, Canonical Huffman, Haar 2D-DWT, QIM, MSE, PSNR, SSIM, Chi-Square), dan spesifikasi frame biner 90-byte. |
| 🔀 **[APP_FLOW.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/APP_FLOW.md)** | **Application Flow & User Journey:** Alur navigasi antarmuka, diagram state transition, wireframe layar pengirim, penerima, dan laboratorium forensik dengan pemetaan komponen shadcn/ui. |
| 🛠️ **[IMPLEMENTATION_PLAN.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/IMPLEMENTATION_PLAN.md)** | **Implementation Plan:** Peta jalan pengerjaan 9 fase terstruktur dari inisialisasi monorepo, engine murni, hingga frontend React + shadcn/ui. |
| 🧪 **[TESTING.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/TESTING.md)** | **Test Strategy & QA:** Matriks kasus uji unit testing, integrasi end-to-end, ambang batas kualitas (PSNR $\ge 40$ dB, SSIM $\ge 0.990$, BER = 0.00%), dan uji ketahanan forensik Chi-Square. |
| 🔐 **[SECURITY.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/SECURITY.md)** | **Security & Cryptography:** Model ancaman STRIDE, spesifikasi AES-256-GCM AEAD, KDF PBKDF2 (600k iterasi), kepatuhan Prinsip Kerckhoffs, UU PDP No. 27/2022, dan HIPAA. |
| 💻 **[CODE_STYLE.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/CODE_STYLE.md)** | **Code Style Guidelines:** Standar PEP 8, Type Hints, Clean Architecture, hirarki custom exception, aturan vektorisasi NumPy, serta pedoman React 18, TypeScript & shadcn/ui. |
| 🗄️ **[DATABASE.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/DATABASE.md)** | **Database Architecture:** Konsep Zero-Plaintext storage, skema SQLite WAL mode untuk tabel `audit_logs` dan `doctor_sessions`. |
| 🔗 **[API.md](file:///c:/FIRDAUS/LOCAL%20DISK%20D/ALL%20ABOUT%20UHAMKA/SEMESTER%207/Tek.%20Kompresi%20dan%20Penyamaran%20Data/TUGAS%20AKHIR/docs/API.md)** | **API Contracts & Endpoints:** Spesifikasi RESTful FastAPI (`/pipeline/encode`, `/pipeline/extract`, `/forensics/compare`, `/audit/logs`), skema request/response Pydantic v2, dan error RFC 7807. |

---

## 👥 Rencana Pembagian Tugas Kelompok (Maksimal 4 Orang)

Sesuai ketentuan RTM kelas 7A, kelompok dapat membagi peran teknis sebagai berikut:

1. **Anggota 1 — Spesialis Kompresi Teks & Entropi:**
   - Bertanggung jawab pada modul `backend/core/compression/lz77.py`, `huffman.py`, dan `entropy.py`.
   - Menguasai materi Modul 1, 2, 4, 6 (Pohon Huffman kanonikal, prefix property, dan tokenisasi sliding window).
2. **Anggota 2 — Spesialis Steganografi Domain Frekuensi:**
   - Bertanggung jawab pada modul `backend/core/steganography/dwt.py`, `embedder.py`, dan `extractor.py`.
   - Menguasai dekomposisi 2D-DWT Haar, modulasi koefisien sub-band LH/HL, dan rekonstruksi IDWT.
3. **Anggota 3 — Spesialis Kriptografi & Evaluasi Forensik:**
   - Bertanggung jawab pada modul `backend/core/security/cipher.py`, `backend/core/metrics/quality.py`, dan `steganalysis.py`.
   - Menguasai enkripsi AES-256-GCM, KDF PBKDF2, perhitungan PSNR/SSIM, dan uji statistik Chi-Square.
4. **Anggota 4 — Spesialis UI/UX, API & Dokumentasi:**
   - Bertanggung jawab pada `backend/api/` (FastAPI orkestrator), antarmuka `frontend/` (**React 18 + Vite + Tailwind CSS + shadcn/ui** Medical PACS Dashboard), dan penyusunan laporan serta slide presentasi.

---

## 🚀 Status Kesiapan Eksekusi
Seluruh cetak biru teknis dan dokumen rekayasa perangkat lunak telah selesai dan terintegrasi 100%. Kita siap memulai eksekusi **Fase 1 (Scaffolding)** dan **Fase 2 (Algoritma Core Kompresi LZ77 + Huffman)**.
