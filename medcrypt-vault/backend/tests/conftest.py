import sys
from pathlib import Path

# Add medcrypt-vault directory and backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
vault_dir = backend_dir.parent

for p in [str(vault_dir), str(backend_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)
