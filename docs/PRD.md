# Product Requirements Document (PRD)
## MedCrypt-Vault: Medical Electronic Health Record Compression & Frequency-Domain Steganography Platform

---

### 1. Project Overview & Vision

**MedCrypt-Vault** adalah platform perangkat lunak kelas medis (*enterprise-grade medical software*) yang mengintegrasikan teknik **Kompresi Data Hibrida (LZ77 + Huffman Coding)** dan **Penyamaran Data Domain Frekuensi (2D-Discrete Wavelet Transform / DWT)** untuk mengamankan Rekam Medis Elektronik (*Electronic Health Record* / EHR) langsung di dalam citra diagnostik radiologi (seperti X-Ray, CT-Scan, dan MRI).

Platform ini memecahkan dua masalah fundamental dalam informatika medis modern:
1. **Pemisahan Berkas (*Record Dissociation*):** Seringnya file rekam medis pasien terpisah dari file citra rontgen saat dikirim antar-departemen atau klinik, berisiko malpraktik diagnosis.
2. **Kerahasiaan & Efisiensi Transmisi (*Data Privacy & Bandwidth Bloat*):** Kebutuhan mengirim data medis sensitif sesuai regulasi privasi (UU PDP No. 27/2022 & HIPAA) di tengah keterbatasan bandwidth jaringan rumah sakit.

---

### 2. User Personas & Target Audiences

| Persona | Peran | Kebutuhan Utama |
| :--- | :--- | :--- |
| **Dr. Sp.Rad (Radiolog)** | Dokter spesialis pembaca citra diagnostik | Memerlukan citra rontgen yang **100% bebas distorsi klinis** (PSNR $>40$ dB, SSIM $>0.99$) tanpa artefak visual yang mengaburkan diagnosa, serta akses instan ke riwayat pasien. |
| **IT & Security Administrator RS** | Pengelola infrastruktur data rumah sakit | Mengurangi beban kapasitas penyimpanan cloud/server dan mengamankan transmisi data pasien dari penyadapan man-in-the-middle (MITM). |
| **Penerima / Pasien / Faskes Rujukan** | Pihak penerima data transfer | Membuka berkas stego citra menggunakan kunci otorisasi (*Secret Key*) dan mendapatkan kembali berkas rekam medis yang utuh tanpa korupsi bit (verifikasi SHA-256). |
| **Dosen & Penguji Akademik (TK-PD)** | Evaluator teknis mata kuliah | Menilai orisinalitas algoritma kompresi (Modul 1-6), algoritma steganografi (Modul 9-11), ketahanan steganalsis, serta kelengkapan metrik evaluasi matematis. |

---

### 3. Core Feature Requirements

#### F-01: Modul Kompresi Hibrida Rekam Medis (LZ77 + Canonical Huffman)
- **Deskripsi:** Mengompresi berkas rekam medis pasien (format JSON/PDF/Teks) secara bertahap:
  1. *Tahap 1 (Dictionary Transform):* Mencari pola repetisi frasa/istilah medis berulang menggunakan **LZ77 Sliding Window** (Search buffer 32 KB, Look-ahead buffer 256 B) menghasilkan token `[offset, length, literal]`.
  2. *Tahap 2 (Statistical Encoding):* Mengalokasikan bit variabel berdasarkan frekuensi kemunculan token menggunakan **Canonical Huffman Coding** dengan pemenuhan *Prefix Property*.
- **Metrik Sukses:** Mampu memangkas ukuran berkas rekam medis sebesar **50% – 70%** (Rasio Kompresi $CR \ge 2.0$).

#### F-02: Modul Kriptografi Berlapis (AES-256-GCM + PBKDF2)
- **Deskripsi:** Mengenkripsi payload sebelum disisipkan ke citra. Kunci enkripsi diturunkan dari passphrase dokter/klinik menggunakan **PBKDF2-HMAC-SHA256** dengan garam (*salt*) acak 16-byte dan 600.000 iterasi. Enkripsi menggunakan **AES-256-GCM** (Authenticated Encryption with Associated Data).
- **Metrik Sukses:** Muatan terenkripsi memiliki sifat *Zero-Knowledge* (secara matematis indistinguishable dari Gaussian random noise) sehingga tidak dapat dibedakan dari noise alami sensor rontgen.

#### F-03: Modul Steganografi Adaptif Domain Frekuensi (2D-DWT)
- **Deskripsi:** Citra medis pembawa (*cover*) didekomposisi 1 tingkat menggunakan **2D Discrete Wavelet Transform (Haar Wavelet)** menjadi 4 sub-band:
  - $LL$ (*Low-Low*): Memuat 95% energi dan struktur anatomis vital pasien $\to$ **DILINDUNGI & TIDAK DISENTUH**.
  - $LH$ (*Low-High*): Koefisien detail horizontal frekuensi menengah $\to$ **Tempat penyisipan bit payload**.
  - $HL$ (*High-Low*): Koefisien detail vertikal frekuensi menengah $\to$ **Tempat penyisipan bit payload**.
  - $HH$ (*High-High*): Koefisien detail diagonal frekuensi tinggi $\to$ Digunakan opsional jika kapasitas payload besar.
- **Metrik Sukses:** Rekonstruksi citra stego via Inverse DWT (IDWT) menghasilkan citra dengan **PSNR $>40$ dB** dan **SSIM $>0.990$**.

#### F-04: Modul Audit Kualitas & Steganalisis Forensik Real-Time
- **Deskripsi:** Dashboard evaluasi otomatis yang menghitung dan memvisualisasikan:
  1. **Shannon Entropy $\mathcal{H}(S)$:** Entropi citra cover vs citra stego vs payload bitstream.
  2. **Metrik Distorsi:** Mean Squared Error (MSE), Peak Signal-to-Noise Ratio (PSNR), dan Structural Similarity Index (SSIM).
  3. **Uji Ketahanan Forensik Chi-Square ($\chi^2$):** Analisis statistik *Pairs of Values* (PoVs) untuk membuktikan kurva deteksi berada di bawah ambang deteksi steganalsis ($p\text{-value} > 0.05$).
  4. **Visualizer Sub-Band Frekuensi & Bit-Plane Slicing:** Melihat visualisasi 4 kuadran DWT dan bit-plane 0-7.

#### F-05: Modul Ekstraksi & Verifikasi Integritas Data Medis
- **Deskripsi:** Panel pemulihan data untuk faskes penerima. Citra stego dimasukkan bersama kunci rahasia $\to$ mengekstrak bit dari sub-band frekuensi $\to$ mendekripsi AES-GCM $\to$ mendekompresi Huffman $\to$ memulihkan token LZ77 $\to$ memvalidasi hash SHA-256.
- **Metrik Sukses:** Bit Error Rate (**BER = 0.00%**). Data rekam medis terekstrak 100% sempurna tanpa ada 1 karakter pun yang rusak.

---

### 4. Non-Functional Requirements (NFR)

1. **Performa & Latensi:**
   - Proses kompresi & enkripsi rekam medis 50 KB selesai dalam waktu $< 300\text{ ms}$.
   - Proses dekomposisi 2D-DWT, embedding, dan IDWT citra resolusi $2048 \times 2048$ selesai dalam waktu $< 1.5\text{ detik}$.
2. **Kepatuhan Privasi & Regulasi:**
   - Memenuhi standar proteksi data medis: data di memori di-*zeroized* setelah diproses, tidak ada berkas sementara (*temp file*) yang tertinggal dalam keadaan tidak terenkripsi.
3. **Kompatibilitas Format Citra:**
   - Mendukung format standar citra medis: PNG (8-bit grayscale & 24-bit RGB), TIFF, BMP, dan emulasi DICOM payload.
4. **Reliabilitas:**
   - Sistem menolak embedding secara aman jika ukuran muatan terkompresi melebihi kapasitas maksimum yang diizinkan pada sub-band DWT (*Capacity Overflow Protection*).

---

### 5. Rubrik Penilaian Akademis & Nilai 100 Guarantee

| Kriteria Dosen (RTM) | Bobot | Pemenuhan pada MedCrypt-Vault |
| :--- | :--- | :--- |
| **1. Manfaat Nyata** | Tinggi | Menyelesaikan isu krusial rekam medis digital (kepatuhan UU PDP/HIPAA & pencegahan berkas tertukar). |
| **2. Berfungsi dengan Baik** | Tinggi | Pipeline end-to-end teruji dengan Unit Testing ketat (BER = 0%, PSNR $>40$ dB, SHA-256 integrity match). |
| **3. Orisinalitas** | Sangat Tinggi | Algoritma LZ77 sliding window dan Huffman tree dibangun dari *scratch* (bukan hanya memanggil wrapper pustaka hitam). |
| **4. Demonstrasi & Presentasi** | Sangat Tinggi | Antarmuka interaktif PACS Radiology berbasis **shadcn/ui** (React + Vite + Tailwind) dengan fitur side-by-side diff viewer, visualizer sub-band DWT, grafik Chi-square, dan live extraction. |
| **5. Integrasi Materi Kuliah** | Mutlak | Menghubungkan Modul 1, 2, 4, 6 (Kompresi & Entropi) dengan Modul 9, 10, 11 (Steganografi frekuensi & Steganalisis). |

---

### 6. Ruang Lingkup (Scope Boundaries)

- **In-Scope:**
  - Aplikasi lokal berbasis Web GUI interaktif (React 18 + Vite + Tailwind CSS + **shadcn/ui**).
  - Implementasi kompresi LZ77 + Huffman murni.
  - Implementasi 2D-DWT Haar Wavelet steganography murni dengan NumPy.
  - Enkripsi AES-256-GCM.
  - Modul evaluasi objektif (MSE, PSNR, SSIM, Entropi, Chi-square).
  - Ekstraksi dan verifikasi integritas data medis.
- **Out-of-Scope (Future Development):**
  - Integrasi PACS server cloud skala enterprise (DICOM C-STORE / DIMSE protokol tingkat rumah sakit nasional).
  - Pemrosesan video endoskopi streaming real-time (fokus proyek pada citra radiologi statis resolusi tinggi).
