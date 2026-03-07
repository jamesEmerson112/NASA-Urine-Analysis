# NASA Urine Analysis - Neural Network Architecture Comparison

An educational animation comparing three neural network architectures (MLP, CNN, Transformer) applied to medical urine/biomarker analysis. Each animation shows how the architecture processes medical data differently, rendered with [Manim](https://www.manim.community/) and served as an interactive web page.

## Architectures Compared

| Architecture | Input Type | Use Case |
|---|---|---|
| **MLP** | Tabular biomarker readings | Classifying urine samples from numeric features |
| **CNN** | Urine test strip images | Detecting patterns in reagent pad colors |
| **Transformer** | Sequential readings over time | Analyzing longitudinal patient biomarker trends |

## Setup

### System Dependencies (macOS)

```bash
brew install cairo pango ffmpeg
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Render Animations

```bash
# Low quality (fast, for development)
bash render.sh l

# Medium quality
bash render.sh m

# High quality (default)
bash render.sh
```

### View the Interactive Comparison

After rendering, open the web page:

```bash
open web/index.html
```

The interactive page supports:
- **Tabbed view** - focus on one architecture at a time
- **Side-by-side** - compare two or three architectures
- **Synchronized playback** - play all videos in sync
- Custom video controls with step-through (+/- 1 second)

## Project Structure

```
manim_scenes/         # Manim animation source code
  common.py           # Shared colors, helpers, reusable components
  mlp_scene.py        # Multi-Layer Perceptron animation
  cnn_scene.py        # Convolutional Neural Network animation
  transformer_scene.py # Transformer animation
web/                  # Interactive web viewer
  index.html          # Main comparison page
  css/styles.css      # NASA-inspired dark theme
  js/app.js           # Video controls and view switching
  media/              # Rendered video files (generated)
render.sh             # Build script to render all scenes
```
