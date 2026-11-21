# Research & Science Skill (Compression & Steganography Theory)
## Mathematical Foundations for MedCrypt-Vault

### 1. Information Theory & Compression Bounds
- **Shannon Entropy ($\mathcal{H}$):**
  $$\mathcal{H}(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i) \quad [\text{bits/symbol}]$$
  - Represents the theoretical minimum average code length achievable for lossless compression without loss of information.
- **Compression Metrics:**
  - Compression Ratio: $CR = \frac{\text{Original Size}}{\text{Compressed Size}}$
  - Space Saving: $SS = \left(1 - \frac{\text{Compressed Size}}{\text{Original Size}}\right) \times 100\%$

### 2. Frequency Domain Wavelet Transformation (2D Haar DWT)
- An image $I(x, y)$ is decomposed into four orthogonal frequency sub-bands:
  - $LL_1$: Low-frequency approximation (contains $>95\%$ energy, patient anatomy). **Must remain untouched.**
  - $LH_1$: Horizontal detail (vertical edges). Embedded with payload bitstream.
  - $HL_1$: Vertical detail (horizontal edges). Embedded with payload bitstream.
  - $HH_1$: Diagonal high-frequency detail. Reserved / secondary.
- **Quantization Index Modulation (QIM):**
  - Given quantization step $\Delta$:
    $$c' = \begin{cases} \text{round}\left(\frac{c}{\Delta}\right) \cdot \Delta + \frac{\Delta}{4}, & \text{if bit } b = 0 \\ \text{round}\left(\frac{c}{\Delta}\right) \cdot \Delta - \frac{\Delta}{4}, & \text{if bit } b = 1 \end{cases}$$
  - Extraction rule:
    $$b = \begin{cases} 0, & \text{if } \left(c' - \text{round}\left(\frac{c'}{\Delta}\right) \cdot \Delta\right) \ge 0 \\ 1, & \text{otherwise} \end{cases}$$

### 3. Image Fidelity & Steganalysis
- **Peak Signal-to-Noise Ratio (PSNR):**
  $$PSNR = 10 \cdot \log_{10}\left(\frac{MAX_I^2}{MSE}\right) \quad [\text{dB}]$$
  Target: $PSNR \ge 40\text{ dB}$ (Imperceptible distortion for medical diagnostics).
- **Structural Similarity Index (SSIM):**
  Evaluates luminance, contrast, and structural degradation using local Gaussian windows. Target: $SSIM \ge 0.990$.
- **Chi-Square ($\chi^2$) Steganalysis:**
  Tests whether pairs of values (PoVs) in the pixel histogram have been equalized by steganographic modification:
  $$\chi^2 = \sum_{k=1}^{128} \frac{(h_{2k} - h^*_{2k})^2}{h^*_{2k}}, \quad h^*_{2k} = \frac{h_{2k} + h_{2k+1}}{2}$$
  Target: $p\text{-value} > 0.05$ (Fail to reject null hypothesis; image appears natural and free of statistical anomalies).
