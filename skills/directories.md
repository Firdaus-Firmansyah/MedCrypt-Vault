# Directories & File Organization Skill
## Standard Monorepo Structure for MedCrypt-Vault

```
TUGAS AKHIR/
├── docs/                        # 9 Complete Architecture Specification Documents
│   ├── PRD.md
│   ├── TRD.md
│   ├── APP_FLOW.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── TESTING.md
│   ├── SECURITY.md
│   ├── CODE_STYLE.md
│   ├── DATABASE.md
│   └── API.md
├── skills/                      # BrochBuilds-inspired Project Engineering Skills
│   ├── engineering-workflow.md
│   ├── design-and-ui.md
│   ├── security.md
│   ├── codebase-understanding.md
│   ├── research-and-science.md
│   └── directories.md
├── medcrypt-vault/              # Master Monorepo Application
│   ├── backend/                 # Python 3.12 Backend & Core Algorithms
│   │   ├── core/
│   │   │   ├── compression/     # Pure Python LZ77, Huffman, Shannon Entropy
│   │   │   ├── security/        # AES-256-GCM, PBKDF2, Binary Framing
│   │   │   ├── steganography/   # 2D Haar DWT, IDWT, QIM Embedder/Extractor
│   │   │   └── metrics/         # PSNR, SSIM, MSE, Chi-Square
│   │   ├── api/                 # FastAPI REST API layer
│   │   │   ├── routes/
│   │   │   ├── schemas/
│   │   │   └── services/
│   │   ├── tests/               # Pytest suite
│   │   ├── sample_data/         # Sample medical images & patient EHRs
│   │   ├── requirements.txt     # Python backend dependencies
│   │   └── main.py              # Backend entrypoint
│   ├── frontend/                # React 18 + Vite + Tailwind CSS + shadcn/ui
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── ui/          # Generated shadcn/ui primitives
│   │   │   │   └── medical/     # Custom medical PACS components
│   │   │   ├── lib/             # utils.ts, api.ts
│   │   │   ├── hooks/           # custom react hooks
│   │   │   ├── App.tsx
│   │   │   └── main.tsx
│   │   ├── package.json
│   │   └── vite.config.ts
│   └── run_system.py            # Unified single-command launcher
├── Proposal_Opsi_Tugas_Akhir_TKPD_7A.docx
└── README.md                    # Master Project Portal & Team Assignment
```
