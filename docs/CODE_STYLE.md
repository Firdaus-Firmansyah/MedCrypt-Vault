# Code Style & Engineering Standards (CODE_STYLE)
## MedCrypt-Vault: Coding Conventions & Architectural Guidelines

---

### 1. Core Engineering Principles

1. **Clean Architecture & Separation of Concerns:**
   - Modul `backend/core/` (kompresi, kriptografi, steganografi) bersifat **independen murni** dari framework web atau antarmuka UI. Modul core harus dapat dijalankan melalui CLI, script Python mandiri, maupun diimpor sebagai pustaka.
   - Lapisan API (`backend/api/`) hanya bertindak sebagai orkestrator dan validator I/O.
   - Lapisan antarmuka (`frontend/`) terpisah secara modular menggunakan stack modern React 18 + Vite + TypeScript + Tailwind CSS + **shadcn/ui**.
2. **Explicit is Better than Implicit (PEP 20 & Strict TypeScript):**
   - Python: Wajib menggunakan **Type Hints (`typing`)** penuh pada setiap parameter fungsi, return type, dan atribut kelas.
   - TypeScript: Aktifkan `strict: true` di `tsconfig.json`. Hindari penggunaan tipe `any`.
3. **Mathematical Precision & Performance:**
   - Hindari perulangan `for` bersarang (*nested loops*) dalam pemrosesan piksel citra. Wajib memanfaatkan **vektorisasi NumPy** dan operasi matriks teroptimasi C.

---

### 2. Konvensi Penamaan (*Naming Conventions*)

| Bahasa / Komponen | Format | Contoh |
| :--- | :--- | :--- |
| **Python Modules / Files** | `snake_case` | `huffman.py`, `dwt_stego.py`, `quality_metrics.py` |
| **Python Classes** | `PascalCase` | `LZ77Compressor`, `DWTWaveletEngine`, `PatientRecord` |
| **Python Functions / Methods** | `snake_case` | `calculate_entropy()`, `embed_payload()`, `decompress()` |
| **Python Constants** | `UPPER_SNAKE_CASE` | `MAGIC_HEADER = b"MCVT"`, `DEFAULT_QUANT_STEP = 4` |
| **React Components** | `PascalCase` | `XRayViewer.tsx`, `CompressionMeter.tsx`, `ForensicChart.tsx` |
| **shadcn/ui Primitives** | `kebab-case` | `button.tsx`, `tabs.tsx`, `card.tsx`, `progress.tsx` |
| **TypeScript Types / Interfaces** | `PascalCase` | `PatientData`, `EncodeResponse`, `MetricsResult` |
| **TS Hooks / Helpers** | `camelCase` | `useCompression()`, `formatBytes()`, `calculatePsnr()` |

---

### 3. Standar Dokumentasi Kode Python (*Google Style Docstring*)

Setiap fungsi dan kelas pada modul backend core wajib memiliki docstring berstandar Google:

```python
def calculate_shannon_entropy(data: bytes) -> float:
    """Calculates the theoretical Shannon Entropy of a byte sequence.

    Args:
        data (bytes): The raw input byte array to evaluate.

    Returns:
        float: The Shannon entropy value measured in bits per byte (0.0 to 8.0).

    Raises:
        ValueError: If the input data byte array is empty.

    Example:
        >>> calculate_shannon_entropy(b"AAAAABBBCC")
        1.4854752972273344
    """
```

---

### 4. Hirarki Penanganan Eksepsi Python (*Custom Domain Exceptions*)

Gunakan custom exceptions yang terstruktur untuk memudahkan pelacakan error dan pemetaan ke RFC 7807 HTTP errors:

```python
class MedCryptError(Exception):
    """Base exception for all MedCrypt-Vault operations."""
    pass

class CapacityExceededError(MedCryptError):
    """Raised when the compressed payload exceeds cover image embedding capacity."""
    pass

class AuthenticationFailedError(MedCryptError):
    """Raised when decryption fails due to invalid secret passphrase or tampered data."""
    pass

class CorruptFrameHeaderError(MedCryptError):
    """Raised when extracted binary stream does not match the MCVT magic header."""
    pass
```

---

### 5. Aturan Kinerja Pemrosesan Citra (*NumPy Vectorization Rules*)

- **Jangan Pernah Menggunakan:**
  ```python
  # BURUK & LAMBAT (O(N*M) loop di Python)
  for i in range(height):
      for j in range(width):
          pixel = image[i, j]
          # modifikasi nilai piksel satu per satu
  ```
- **Wajib Menggunakan:**
  ```python
  # BAIK & SANGAT CEPAT (Operasi Vektor NumPy)
  # Kuantisasi seluruh matriks sub-band dalam satu instruksi C terkompilasi
  quantized = np.round(subband / delta) * delta + (delta / 4)
  ```

---

### 6. Standar Frontend: React 18, TypeScript & shadcn/ui

1. **Organisasi Direktori UI:**
   - `src/components/ui/`: Berisi komponen murni hasil generate dari CLI shadcn/ui (`button.tsx`, `card.tsx`, `tabs.tsx`, dll.). Jangan ubah logika dasar komponen ini kecuali penyesuaian tema.
   - `src/components/medical/`: Berisi komponen domain spesifik MedCrypt-Vault (`DwtExplorer.tsx`, `XRayUploader.tsx`, `PatientForm.tsx`, `ForensicView.tsx`).
   - `src/lib/utils.ts`: Utilitas fungsi penggabung kelas CSS dengan `clsx` dan `tailwind-merge`:
     ```typescript
     import { clsx, type ClassValue } from "clsx"
     import { twMerge } from "tailwind-merge"

     export function cn(...inputs: ClassValue[]) {
       return twMerge(clsx(inputs))
     }
     ```

2. **Penggunaan Komponen shadcn/ui yang Konsisten:**
   - Gunakan selalu fungsi `cn()` untuk conditional styling pada komponen UI.
   - Manfaatkan Radix UI primitives yang terpasang di dalam shadcn/ui untuk aksesibilitas penuh (keyboard navigation, ARIA attributes).
   - Terapkan dark theme medis berbasis palet warna Slate (`bg-slate-950`, `border-slate-800`, `text-slate-100`, dan aksen `cyan-500` / `emerald-500`).
