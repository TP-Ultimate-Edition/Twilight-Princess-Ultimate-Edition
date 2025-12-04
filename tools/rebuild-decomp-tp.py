import argparse
import os
from pathlib import Path
import sys
import time

# Check for DOLPHIN_MAPS_PATH environment variable first
DOLPHIN_MAPS_PATH = os.getenv('DOLPHIN_MAPS_PATH')
if DOLPHIN_MAPS_PATH:
    DEFAULT_DOLPHIN_MAPS_PATH = Path(DOLPHIN_MAPS_PATH).expanduser()
else:
    # Fall back to default Dolphin config path
    if os.name == "nt":
        DEFAULT_DOLPHIN_CONFIG_PATH = Path(os.getenv('APPDATA')) / "Dolphin Emulator"
    else:
        # macOS Dolphin paths
        mac_paths = [
            Path("~/Library/Application Support/Dolphin/Maps").expanduser(),
            Path("~/.dolphin-emu/Maps").expanduser(),
            Path("~/.var/app/org.DolphinEmu.dolphin-emu/data/dolphin-emu/Maps").expanduser()
        ]
        # Find first existing path or use first one
        DEFAULT_DOLPHIN_MAPS_PATH = None
        for p in mac_paths:
            if p.parent.exists():
                DEFAULT_DOLPHIN_MAPS_PATH = p
                break
        if DEFAULT_DOLPHIN_MAPS_PATH is None:
            DEFAULT_DOLPHIN_MAPS_PATH = mac_paths[0]
    DEFAULT_DOLPHIN_MAPS_PATH = Path(DEFAULT_DOLPHIN_CONFIG_PATH) / "Maps" if os.name == "nt" else DEFAULT_DOLPHIN_MAPS_PATH

def expanded_path(path_str: str):
    path = Path(path_str)
    path = path.expanduser()
    return path

parser = argparse.ArgumentParser()
parser.add_argument("vanilla_iso_path", type=expanded_path, help="Path to a vanilla Twilight Princess ISO to use as a base.")
parser.add_argument("output_iso_path", type=expanded_path, help="Path to put the modified ISO.")
parser.add_argument("decomp_repo_path", type=expanded_path, help="Path to the root of the git repository containing the tp decompilation.")
parser.add_argument("--map", type=expanded_path, default=DEFAULT_DOLPHIN_MAPS_PATH, help="Folder to place the symbol map for the modified ISO.")

args = parser.parse_args()
decomp_build_path = args.decomp_repo_path / "build/GZ2E01"

print("Loading GameCube ISO libraries...")
sys.stdout.flush()

from gclib.gcm import GCM
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0
from io import BytesIO
import shutil

print("Reading vanilla ISO... (this may take a minute)")
sys.stdout.flush()
gcm = GCM(args.vanilla_iso_path)
gcm.read_entire_disc()
print("✓ Vanilla ISO loaded")
sys.stdout.flush()

print("Processing RELS archive...")
sys.stdout.flush()
rels_arc = RARC(gcm.read_file_data("files/RELS.arc"))
rels_arc.read()

print("Patching REL files...")
sys.stdout.flush()
rel_count = 0
for rel_name in os.listdir(decomp_build_path):
    if os.path.isfile(decomp_build_path / rel_name):
        continue
    if not os.path.isfile(decomp_build_path / rel_name / (rel_name + ".rel")):
        continue
    decomp_rel_path = decomp_build_path / rel_name / (rel_name + ".rel")
    with open(decomp_rel_path, "rb") as f:
        decomp_rel_data = BytesIO(f.read())
    rel_file_entry = rels_arc.get_file_entry(rel_name.lower() + ".rel")
    if rel_file_entry:
        print(f"  → Compressing {rel_name}.rel...")
        sys.stdout.flush()
        rel_file_entry.data = Yaz0.compress(decomp_rel_data)
        rel_count += 1
    else:
        gcm_rel_file_path = f"files/rel/Final/Release/{rel_name}.rel"
        assert gcm_rel_file_path in gcm.files_by_path, f"Invalid REL path: {gcm_rel_file_path}"
        gcm.changed_files[gcm_rel_file_path] = decomp_rel_data
        rel_count += 1

print(f"✓ Patched {rel_count} REL files")
sys.stdout.flush()

rels_arc.save_changes()
gcm.changed_files["files/RELS.arc"] = rels_arc.data

print("Replacing main.dol...")
sys.stdout.flush()
with open(decomp_build_path / "framework.dol", "rb") as f:
    gcm.changed_files["sys/main.dol"] = BytesIO(f.read())

print("Adding symbol map...")
sys.stdout.flush()
with open(decomp_build_path / "framework.elf.MAP", "rb") as f:
    gcm.changed_files["files/map/Final/Release/frameworkF.map"] = BytesIO(f.read())

# Create Maps directory if it doesn't exist
args.map.mkdir(parents=True, exist_ok=True)
shutil.copy(decomp_build_path / "framework.elf.MAP", args.map)
print(f"✓ Symbol map copied to {args.map}")
sys.stdout.flush()

print("")
print("=" * 60)
print("Exporting modified ISO...")
print("This will take 5-10 minutes. Please be patient!")
print("=" * 60)
print("")
sys.stdout.flush()

last_percent = -1
last_update_time = time.time()
iteration_count = 0

for progress_info in gcm.export_disc_to_iso_with_changed_files(args.output_iso_path):
    iteration_count += 1
    current_time = time.time()
    if current_time - last_update_time >= 2.0 or iteration_count % 50 == 0:
        dots = "." * ((iteration_count // 50) % 4)
        print(f"\rWriting ISO{dots}   ", end='', flush=True)
        last_update_time = current_time
    if isinstance(progress_info, (int, float)):
        percent = int(progress_info)
        if percent != last_percent and percent % 10 == 0:
            print(f"\rProgress: {percent}%", flush=True)
            last_percent = percent

print("\r" + " " * 60)
print("")
print("=" * 60)
print("✓ SUCCESS! Modified ISO created")
print(f"Output: {args.output_iso_path}")
print("=" * 60)
sys.stdout.flush()
