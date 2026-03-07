from manim import *

# NASA-inspired color palette
NASA_BLUE = "#0B3D91"
NASA_RED = "#FC3D21"
HEALTHY_GREEN = "#2ECC71"
UNHEALTHY_RED = "#E74C3C"
DATA_GOLD = "#F39C12"
LAYER_PURPLE = "#9B59B6"
LAYER_TEAL = "#1ABC9C"
BG_DARK = "#0B1D3A"

# Font sizes
TITLE_SIZE = 40
LABEL_SIZE = 22
SUBLABEL_SIZE = 16
NODE_RADIUS = 0.18


def create_layer_block(label, width=1.8, height=2.5, color=NASA_BLUE):
    rect = RoundedRectangle(
        corner_radius=0.15,
        width=width,
        height=height,
        color=color,
        fill_opacity=0.15,
        stroke_width=2,
    )
    text = Text(label, font_size=SUBLABEL_SIZE, color=color)
    text.move_to(rect.get_top() + DOWN * 0.25)
    return VGroup(rect, text)


def create_output_badge(label, color=HEALTHY_GREEN):
    rect = RoundedRectangle(
        corner_radius=0.2,
        width=len(label) * 0.18 + 1.0,
        height=0.55,
        color=color,
        fill_opacity=0.25,
        stroke_width=2,
    )
    text = Text(label, font_size=SUBLABEL_SIZE, color=color, weight=BOLD)
    text.move_to(rect.center())
    return VGroup(rect, text)


def create_title_banner(title_text, color=WHITE):
    text = Text(title_text, font_size=TITLE_SIZE, color=color, weight=BOLD)
    underline = Line(
        text.get_left() + DOWN * 0.3,
        text.get_right() + DOWN * 0.3,
        color=NASA_RED,
        stroke_width=3,
    )
    banner = VGroup(text, underline)
    banner.to_edge(UP, buff=0.5)
    return banner


def create_node_layer(n_nodes, color=WHITE, radius=NODE_RADIUS):
    nodes = VGroup()
    for _ in range(n_nodes):
        c = Circle(radius=radius, color=color, fill_opacity=0.3, stroke_width=2)
        nodes.add(c)
    nodes.arrange(DOWN, buff=0.15)
    return nodes


def draw_connections(layer1, layer2, color=WHITE, opacity=0.3, stroke_width=1):
    lines = VGroup()
    for n1 in layer1:
        for n2 in layer2:
            line = Line(
                n1.get_right(), n2.get_left(),
                color=color,
                stroke_opacity=opacity,
                stroke_width=stroke_width,
            )
            lines.add(line)
    return lines


def create_pulse_dots(layer1, layer2, color=DATA_GOLD, count=5):
    """Create dots and paths for pulse animation between two layers."""
    import random
    dots = VGroup()
    paths = []
    pairs = [(n1, n2) for n1 in layer1 for n2 in layer2]
    selected = random.sample(pairs, min(count, len(pairs)))
    for n1, n2 in selected:
        dot = Dot(radius=0.06, color=color)
        dot.move_to(n1.get_right())
        path = Line(n1.get_right(), n2.get_left())
        dots.add(dot)
        paths.append(path)
    return dots, paths
