# Security & Cryptography Skill (Inspired by BrochBuilds Skills)
## Guidelines for Zero-Trust Healthcare Data Protection

### 1. Cryptographic Principles
- **Authenticated Encryption with Associated Data (AEAD):** Always use `AES-256-GCM` to ensure simultaneous confidentiality and data integrity. Never use outdated or insecure modes like ECB or unauthenticated CBC.
- **Key Derivation (KDF):** Derive 256-bit AES keys from doctor passphrases using `PBKDF2HMAC` with SHA-256, a 16-byte cryptographically secure random salt, and a minimum of 600,000 iterations (OWASP recommendation).
- **Nonce / IV Uniqueness:** Generate a fresh 12-byte cryptographically secure random nonce (`os.urandom(12)`) for every single embedding operation. Never reuse a nonce with the same key.

### 2. Binary Framing & Kerckhoffs's Principle
- All system security relies exclusively on the secrecy of the doctor's passphrase, never on obscurity of algorithms (Kerckhoffs's Principle).
- Frame header (90 bytes) encapsulates public parameters necessary for standard decryption:
  `[Magic (4B) | Version (2B) | Salt (16B) | Nonce (12B) | Compressed_Len (4B) | Original_Len (4B) | Auth_Tag (16B) | SHA-256 Checksum (32B)]`.
- Tamper detection is instantaneous: if even 1 bit of the image sub-band is corrupted, the GCM authentication tag fails verification and decrypt halts immediately without disclosing partial plaintext.

### 3. Regulatory Compliance
- **UU PDP No. 27/2022:** Protection of specific personal medical data against unauthorized interception.
- **HIPAA Security Rule:** Encryption in transit and at rest, non-repudiation via SHA-256 integrity digest, and tamper-evident audit trails.
