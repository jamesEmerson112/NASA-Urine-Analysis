#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCENES_DIR="$SCRIPT_DIR/manim_scenes"
MEDIA_DIR="$SCRIPT_DIR/web/media"

# Activate venv if it exists
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Check dependencies
echo "Checking dependencies..."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: ffmpeg is required. Install with: brew install ffmpeg"; exit 1; }
command -v manim  >/dev/null 2>&1 || { echo "ERROR: manim is required. Run: python3 -m venv .venv && source .venv/bin/activate && pip install manim"; exit 1; }
echo "All dependencies found."

mkdir -p "$MEDIA_DIR"

# Quality flag: pass "l" for low (fast dev), "m" for medium, default is "h" (high)
QUAL="${1:-h}"
case "$QUAL" in
    l|low)     QUALITY_FLAG="-ql" ;;
    m|medium)  QUALITY_FLAG="-qm" ;;
    h|high)    QUALITY_FLAG="-qh" ;;
    *)         QUALITY_FLAG="-qh" ;;
esac

echo "Rendering with quality: $QUAL ($QUALITY_FLAG)"
echo ""

echo "[1/3] Rendering MLP scene..."
manim render "$QUALITY_FLAG" "$SCENES_DIR/mlp_scene.py" MLPScene
echo ""

echo "[2/3] Rendering CNN scene..."
manim render "$QUALITY_FLAG" "$SCENES_DIR/cnn_scene.py" CNNScene
echo ""

echo "[3/3] Rendering Transformer scene..."
manim render "$QUALITY_FLAG" "$SCENES_DIR/transformer_scene.py" TransformerScene
echo ""

# Copy rendered videos to web/media
echo "Copying videos to $MEDIA_DIR..."
find "$SCRIPT_DIR/media" -name "MLPScene.mp4" -exec cp {} "$MEDIA_DIR/mlp.mp4" \; 2>/dev/null || true
find "$SCRIPT_DIR/media" -name "CNNScene.mp4" -exec cp {} "$MEDIA_DIR/cnn.mp4" \; 2>/dev/null || true
find "$SCRIPT_DIR/media" -name "TransformerScene.mp4" -exec cp {} "$MEDIA_DIR/transformer.mp4" \; 2>/dev/null || true

# Also check manim_scenes/media (depending on where manim outputs)
find "$SCENES_DIR" -name "MLPScene.mp4" -exec cp {} "$MEDIA_DIR/mlp.mp4" \; 2>/dev/null || true
find "$SCENES_DIR" -name "CNNScene.mp4" -exec cp {} "$MEDIA_DIR/cnn.mp4" \; 2>/dev/null || true
find "$SCENES_DIR" -name "TransformerScene.mp4" -exec cp {} "$MEDIA_DIR/transformer.mp4" \; 2>/dev/null || true

echo ""
echo "Done! Videos saved to:"
ls -lh "$MEDIA_DIR"/*.mp4 2>/dev/null || echo "WARNING: No MP4 files found in $MEDIA_DIR"
echo ""
echo "Open web/index.html in your browser to view the interactive comparison."
