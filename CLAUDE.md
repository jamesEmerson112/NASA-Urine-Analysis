# CLAUDE.md

## Project Overview

**IMULAS** (Integrated Microfluidic & ML Urine Analysis System) — a NASA NPWEE Spring 2026 educational project. This repository contains animated visualizations comparing three neural network architectures (MLP, CNN, Transformer) applied to astronaut urine/biomarker analysis for health monitoring in microgravity.

## Repository Structure

```
NASA-Urine-Analysis/
├── CLAUDE.md                  # This file
├── README.md                  # Project overview
├── resources.md               # Dataset references and ML strategy
├── NASA_NPWEE_SPRING_2026.md  # Full proposal
├── animation/                 # Main codebase
│   ├── requirements.txt       # Python deps (manim>=0.18.0)
│   ├── render.sh              # Renders all 3 scenes and copies to web/
│   ├── manim_scenes/
│   │   ├── common.py          # Shared colors, helpers, reusable components
│   │   ├── mlp_scene.py       # Multi-Layer Perceptron animation
│   │   ├── cnn_scene.py       # CNN animation
│   │   ├── transformer_scene.py # Transformer animation
│   │   └── manim.cfg          # Manim render config (30fps, high quality)
│   └── web/                   # Interactive web viewer
│       ├── index.html         # Comparison page with 3 viewing modes
│       ├── js/app.js          # Video controls and view switching
│       └── css/styles.css     # NASA-inspired dark theme
```

## Setup

```bash
cd animation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

System dependencies: `ffmpeg`, `cairo`, `pango` (on macOS: `brew install ffmpeg cairo pango`).

## Common Commands

```bash
# Render all animations (from animation/ directory)
bash render.sh          # High quality (default)
bash render.sh l        # Low quality (fast, for development)
bash render.sh m        # Medium quality

# Render a single scene directly
cd animation
manim render -ql manim_scenes/mlp_scene.py MLPScene

# View the web app
open animation/web/index.html
```

## Architecture & Key Patterns

### Animation Scenes (Manim)
- Each neural network type is a separate `Scene` subclass: `MLPScene`, `CNNScene`, `TransformerScene`
- Shared utilities live in `common.py`: NASA color palette, helper functions for layer blocks, node networks, animated pulses, and badges
- NASA color palette: blue `#0B3D91`, red `#FC3D21`, white `#FFFFFF`, light gray `#C0C0C0`
- Scenes follow a consistent structure: title → input visualization → architecture walkthrough → output/classification

### Web Viewer
- Vanilla HTML/CSS/JS (no build tools, no frameworks)
- Three viewing modes: tabbed (single), side-by-side (two), all-three
- Synchronized video playback with custom controls (play/pause, seek, +/-1s stepping)
- Responsive design with mobile breakpoint at 900px

## Conventions

- **Python style**: Follow Manim library conventions. Use descriptive names. Keep reusable components in `common.py`.
- **No build system** for the web frontend — edit files directly.
- **Rendered videos** (MP4) are gitignored. The `render.sh` script outputs them to `animation/web/media/`.
- **Virtual environment** (`.venv/`) is gitignored — always set up locally.

## What's Not Here (Yet)

- No automated tests or CI/CD
- No linter/formatter configuration
- No Docker setup
- No pre-commit hooks
