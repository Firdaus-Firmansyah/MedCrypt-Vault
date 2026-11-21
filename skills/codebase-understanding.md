# Codebase Understanding & Architecture Skill
## Guidelines for Modular, Inspectable Engineering

### 1. Monorepo Structure & Separation of Concerns
```
medcrypt-vault/
├── backend/
│   ├── core/           # PURE ALGORITHMS (zero web/UI dependencies)
│   │   ├── compression/    # LZ77 (sliding window), Huffman (canonical), Shannon Entropy
│   │   ├── security/       # AES-256-GCM, PBKDF2, 90-byte Binary Framing
│   │   ├── steganography/  # 2D Haar DWT, IDWT, QIM Embedder/Extractor
│   │   └── metrics/        # PSNR, SSIM, MSE, Chi-Square Steganalysis
│   ├── api/            # REST API (FastAPI orchestration, schemas, routing)
│   ├── tests/          # Comprehensive Pytest test cases
│   ├── sample_data/    # Sample DICOM/PNG medical images & dummy patient EHRs
│   ├── requirements.txt
│   └── main.py
├── frontend/           # REACT 18 + VITE + TAILWIND CSS + SHADCN/UI
│   ├── src/
│   │   ├── components/ui/       # Standard shadcn/ui primitives
│   │   ├── components/medical/  # Medical PACS custom UI modules
│   │   ├── lib/                 # utils.ts, api client, formatting helpers
│   │   └── App.tsx
│   ├── package.json
│   └── tailwind.config.js
├── skills/             # BrochBuilds-inspired developer & agent skills
├── docs/               # 9 complete architectural specification documents
└── run_system.py       # One-command dual-service launcher
```

### 2. Inspectable, Educational Algorithms (No Blackbox Crutches)
- **LZ77:** Must implement an explicit search buffer ($32\text{ KB}$) and lookahead buffer ($256\text{ B}$), tokenizing into `(offset, length, next_char)`.
- **Huffman:** Must explicitly construct a priority queue (min-heap), compute frequency tables, build binary prefix trees, verify prefix property, and convert to canonical code lengths.
- **2D-DWT:** Must compute 2D Haar wavelet transformation via horizontal and vertical low-pass ($[1, 1]/\sqrt{2}$) and high-pass ($[-1, 1]/\sqrt{2}$) filtering, yielding exact sub-bands ($LL, LH, HL, HH$).
- **Lecturer Defense Readiness:** Every function must be clean and clearly documented so any team member can trace variable transformations step-by-step during project examination.
