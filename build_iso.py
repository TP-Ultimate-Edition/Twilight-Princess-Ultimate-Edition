#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path

print("=== Twilight Princess Ultimate Edition ISO Build (Linux) ===")
print("⚠️  MAKE SURE YOU COMPLETED THE ORIGINAL BUILD INSTRUCTIONS FIRST ⚠️\n")

# Ask user for the original ISO path
iso_input = input("Enter path to your GameCube USA ISO (GCN USA | 60Hz .iso): ").strip().strip('"')
iso_src = Path(iso_input)

if not iso_src.exists():
    print("❌ ISO not found. Exiting.")
    exit(1)

# Copy ISO into orig/GZ2E01/baserom.iso (same folder structure as Windows BAT)
orig_iso = Path("orig/GZ2E01/baserom.iso")
orig_iso.parent.mkdir(parents=True, exist_ok=True)

print(f"\nCopying ISO → {orig_iso}")
shutil.copy2(iso_src, orig_iso)

# Run the build using ninja
print("\nRunning ninja build...\n")
build = subprocess.run(["ninja"], capture_output=True, text=True)
print(build.stdout)

if build.returncode != 0:
    print("❌ Compilation failed.")
    print(build.stderr)
    exit(1)

# Ask user for the output ISO path + filename
output_input = input("Enter output path + filename for your rebuilt ISO (example: /home/user/rebuilt_tp.iso): ").strip().strip('"')
output_iso = Path(output_input)

print("\nBuilding 60FPS patched ISO...\n")

# Run the upstream rebuild script to create the new ISO
rebuild = subprocess.run([
    "python3",
    "tools/rebuild-decomp-tp.py",
    str(orig_iso),
    str(output_iso),
    str(Path().resolve()),
    "3"
], capture_output=True, text=True)

print(rebuild.stdout)

if rebuild.returncode != 0:
    print("❌ ISO build failed.")
    print(rebuild.stderr)
    exit(1)

print("\n✅ ISO Build Complete!")
print(f"Modded ISO is ready at: {output_iso}")
