# Design & UI Skill (shadcn/ui + Tailwind CSS + Medical PACS)
## Guidelines for World-Class Healthcare Workstation Interface

### 1. Design System & Component Library
- **Primary Library:** [shadcn/ui](https://ui.shadcn.com/) powered by Radix UI Primitives and Tailwind CSS.
- **Visual Identity:** Modern Medical PACS (Picture Archiving and Communication System) Dark Theme.
  - Palette: Deep Slate (`slate-950` background, `slate-900` card surfaces, `slate-800` subtle borders).
  - Accents: Clinical Cyan (`cyan-500` / `cyan-400` for active state, primary buttons, and wavelets), Emerald Green (`emerald-500` for security verified badges and high PSNR ratings), Crimson Red (`rose-500` for tamper alerts).
  - Typography: Clean sans-serif (`Inter` or `Geist Sans`), tabular numbers for bytes, bitrates, and coordinate matrices.

### 2. Component Construction Hierarchy
- Use `cn()` helper from `lib/utils.ts` for all class composition.
- UI elements must utilize standard shadcn/ui components:
  - `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` for workspace navigation.
  - `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter` for data grouping.
  - `Button` with distinct variants (`default`, `secondary`, `outline`, `ghost`, `destructive`).
  - `Badge` for status tags (`Lossless BER 0.00%`, `PSNR: 42.8 dB`, `AES-256-GCM`).
  - `Slider` for continuous fine-tuning (DWT quantization step $\Delta$, diff viewer split).
  - `Progress` for 5-step pipeline execution visualization.
  - `Dialog` for secure, modal display of decrypted patient records.
  - `Sonner` toast for immediate, non-intrusive operational feedback.
  - `Table` for statistical and efficiency comparisons.

### 3. Medical Imaging UX Principles
- **Side-by-Side Synchronized Viewing:** Original cover vs. stego image with interactive split-slider.
- **Sub-Band Exploration:** Interactive visual grid of the 4 DWT quadrants ($LL, LH, HL, HH$).
- **Responsive Layout:** Optimized for desktop / clinical workstation displays (min-width: 1280px) while maintaining fluid responsive behavior down to mobile.
