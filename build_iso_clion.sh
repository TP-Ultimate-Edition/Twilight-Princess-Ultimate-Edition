#!/bin/bash
# Twilight Princess Build for CLion
# Boofener: CLion-optimized build script with auto-close

# Change to the directory where this script is located
cd "$(dirname "$0")"

clear
echo "========================================"
echo "Twilight Princess ISO Builder"
echo "========================================"
echo ""

# Find Python 3.10+
PYTHON=""
for cmd in python3.13 python3.12 python3.11 python3.10; do
    if command -v $cmd >/dev/null 2>&1; then
        PYTHON=$cmd
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ ERROR: Python 3.10 or newer required"
    echo ""
    echo "Install with: brew install python@3.11"
    echo "Terminal will close in 30 seconds..."
    sleep 30
    exit 1
fi

echo "✓ Using $PYTHON"

# Check for ninja
if ! command -v ninja >/dev/null 2>&1; then
    echo "❌ ERROR: ninja not found"
    echo "Install with: brew install ninja"
    echo "Terminal will close in 30 seconds..."
    sleep 30
    exit 1
fi

echo "✓ ninja found"
echo ""

# Set paths
VANILLA_ISO="orig/GZ2E01/baserom.iso"
OUTPUT_ISO="output_iso/modified.iso"
DOLPHIN_PATH="/Applications/Dolphin.app"

# Check for ISO
if [ ! -f "$VANILLA_ISO" ]; then
    echo "❌ ERROR: ISO not found at $VANILLA_ISO"
    echo "Please place your Twilight Princess ISO at: $VANILLA_ISO"
    echo "Terminal will close in 30 seconds..."
    sleep 30
    exit 1
fi

echo "Using ISO: $VANILLA_ISO"
echo "Output: $OUTPUT_ISO"
echo ""

# Close Dolphin if running
if pgrep -x "Dolphin" > /dev/null; then
    echo "Closing Dolphin..."
    killall Dolphin 2>/dev/null
    sleep 2
fi

# Build
echo "[1/3] Configuring..."
$PYTHON configure.py --non-matching --map
if [ $? -ne 0 ]; then
    echo "❌ Configure failed"
    echo "Terminal will close in 30 seconds..."
    sleep 30
    exit 1
fi

echo ""
echo "[2/3] Building..."
ninja
if [ $? -ne 0 ]; then
    echo "Cleaning and retrying..."
    rm -rf build/GZ2E01
    $PYTHON configure.py --non-matching --map
    ninja
    if [ $? -ne 0 ]; then
        echo "❌ Build failed"
        echo "Terminal will close in 30 seconds..."
        sleep 30
        exit 1
    fi
fi

echo ""
echo "[3/3] Creating ISO..."

# Check if ISO needs rebuilding
NEEDS_REBUILD=0
if [ ! -f "$OUTPUT_ISO" ]; then
    echo "ISO doesn't exist, building..."
    NEEDS_REBUILD=1
elif [ -d "build/GZ2E01" ]; then
    # Check if any build files are newer than the ISO
    NEWER_FILES=$(find build/GZ2E01 -type f -newer "$OUTPUT_ISO" 2>/dev/null | head -1)
    if [ ! -z "$NEWER_FILES" ]; then
        echo "Build files changed, rebuilding ISO..."
        NEEDS_REBUILD=1
    else
        echo "No changes detected, skipping ISO rebuild"
    fi
else
    echo "Build directory missing, rebuilding..."
    NEEDS_REBUILD=1
fi

if [ $NEEDS_REBUILD -eq 1 ]; then
    mkdir -p output_iso
    export PYTHONPATH="$(pwd)/tools:$PYTHONPATH"
    $PYTHON tools/rebuild-decomp-tp.py "$VANILLA_ISO" "$OUTPUT_ISO" "."

    if [ $? -ne 0 ]; then
        echo "❌ ISO build failed"
        echo "Terminal will close in 30 seconds..."
        sleep 30
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "✓ BUILD COMPLETE!"
echo "Output: $OUTPUT_ISO"
echo "========================================"
echo ""

# Launch Dolphin
if [ -e "$DOLPHIN_PATH" ]; then
    echo "Launching Dolphin..."
    open -a "$DOLPHIN_PATH" "$OUTPUT_ISO"
fi

echo ""
echo "Done! Closing in 2 seconds..."
sleep 2
exit 0
