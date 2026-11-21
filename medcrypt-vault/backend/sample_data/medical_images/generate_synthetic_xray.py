"""Generates a synthetic 512x512 grayscale medical chest phantom X-Ray image.

Simulates anatomical structures:
- Lung cavities (darker radiolucent regions)
- Rib cage / rib contours (curved radiopaque structures)
- Spine / vertebral column (central dense structure)
- Mediastinum and cardiac silhouette (central radiopaque shadow)
- Soft tissue background gradient
"""

import numpy as np
import cv2
from pathlib import Path


def generate_chest_phantom(width: int = 512, height: int = 512) -> np.ndarray:
    """Create a realistic synthetic Chest X-Ray phantom with smooth textures."""
    img = np.zeros((height, width), dtype=np.float32)

    # 1. Background soft-tissue gradient
    y, x = np.ogrid[:height, :width]
    center_y, center_x = height // 2, width // 2
    radial_dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) / (width / 1.4)
    img += 70.0 * (1.0 - np.clip(radial_dist, 0.0, 1.0))

    # 2. Lung fields (left and right dark radiolucent lobes)
    # Right lung (viewer's left)
    lung_r = ((x - width * 0.35) ** 2) / (75 ** 2) + ((y - height * 0.45) ** 2) / (130 ** 2)
    img[lung_r < 1.0] += 30.0 * (1.0 - lung_r[lung_r < 1.0])

    # Left lung (viewer's right, shifted by heart)
    lung_l = ((x - width * 0.65) ** 2) / (70 ** 2) + ((y - height * 0.42) ** 2) / (120 ** 2)
    img[lung_l < 1.0] += 28.0 * (1.0 - lung_l[lung_l < 1.0])

    # 3. Spine column (vertical bright strip)
    spine = np.exp(-((x - center_x) ** 2) / (2 * 14 ** 2)) * 140.0
    img += spine

    # 4. Cardiac silhouette (heart shadow in lower left-center)
    heart = ((x - width * 0.54) ** 2) / (55 ** 2) + ((y - height * 0.56) ** 2) / (65 ** 2)
    heart_mask = heart < 1.0
    img[heart_mask] += 90.0 * (1.0 - heart[heart_mask])

    # 5. Rib cage arches (subtle curved radiopaque bands)
    for i in range(7):
        rib_y = int(height * 0.22 + i * 36)
        curvature = 0.0008 * (x - center_x) ** 2
        rib_band = np.exp(-((y - (rib_y + curvature)) ** 2) / (2 * 6 ** 2)) * 45.0
        img += rib_band

    # 6. Add realistic Poisson-Gaussian medical noise
    noise = np.random.normal(0, 3.5, (height, width))
    img += noise

    # Clip to valid 8-bit range
    img = np.clip(img, 10.0, 245.0).astype(np.uint8)

    # Apply slight bilateral filter for organic anatomical smoothness
    img = cv2.bilateralFilter(img, d=5, sigmaColor=20, sigmaSpace=20)
    return img


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "chest_xray_512.png"
    img = generate_chest_phantom(512, 512)
    cv2.imwrite(str(out_path), img)
    print(f"[SUCCESS] Synthetic Chest X-Ray phantom created: {out_path} ({img.shape}, dtype={img.dtype})")
