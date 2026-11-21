# Engineering Workflow Skill (Inspired by BrochBuilds Skills)
## Guidelines for High-Velocity, Production-Grade Engineering

### 1. Architectural Integrity & Clean Boundaries
- **Core Isolation:** The core mathematical algorithms (entropy calculation, LZ77 sliding window, canonical Huffman coding, 2D Haar DWT, QIM modulation) must have **zero dependencies** on web frameworks (FastAPI) or UI layers (React/shadcn).
- **Inversion of Control:** Core functions accept plain data structures (`bytes`, `np.ndarray`, dataclasses) and return deterministic outputs.
- **Fail-Fast with Domain Errors:** Always throw explicit domain exceptions (`CapacityExceededError`, `AuthenticationFailedError`, `CorruptFrameHeaderError`) rather than returning ambiguous `None` or boolean `False`.

### 2. Implementation Execution Cycle
1. **Spec Alignment:** Read corresponding specification in `docs/` (`TRD.md`, `CODE_STYLE.md`) before writing any algorithm.
2. **Pure Implementation:** Implement algorithms from mathematical first principles (educational, inspectable, fully vector-optimized).
3. **Unit Verification:** Write and run isolated pytest tests covering normal behavior, edge cases (empty bytes, single-character repetitions, high-entropy random bytes), and error boundaries.
4. **Integration Verification:** Chain modules end-to-end (Raw EHR $\to$ LZ77 $\to$ Huffman $\to$ AES-GCM $\to$ 2D-DWT $\to$ Stego Image $\to$ Reverse $\to$ Exact Raw EHR with BER 0.00%).

### 3. Git & Team Collaboration Etiquette
- Atomic commits with conventional commits: `feat(compression): implement canonical huffman bit-packer`, `test(stego): verify PSNR threshold on 512x512 x-ray`.
- Every pull request / milestone must pass automated pytest suites without regression.
