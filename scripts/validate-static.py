#!/usr/bin/env python3
"""Valide la syntaxe des fichiers YAML et du Vagrantfile."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
try:
    import yaml
except ImportError:
    print("PyYAML manque : python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

errors = []
paths = list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.yaml"))
for path in sorted(paths):
    if any(part in {".git", ".vagrant"} for part in path.parts):
        continue
    try:
        list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")

vagrantfile = ROOT / "Vagrantfile"
if vagrantfile.exists():
    result = subprocess.run(["ruby", "-c", str(vagrantfile)], text=True, capture_output=True)
    if result.returncode:
        errors.append(f"Vagrantfile: {result.stdout}{result.stderr}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

print(f"Validation statique OK : {len(paths)} fichiers YAML/YML.")
