import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from common import (
    NASA_BLUE, NASA_RED, HEALTHY_GREEN, UNHEALTHY_RED, DATA_GOLD,
    LAYER_PURPLE, LAYER_TEAL, BG_DARK,
    TITLE_SIZE, LABEL_SIZE, SUBLABEL_SIZE, NODE_RADIUS,
    create_layer_block, create_output_badge, create_title_banner,
    create_node_layer, draw_connections, create_pulse_dots,
)


class MLPScene(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        # --- Title ---
        banner = create_title_banner("Multi-Layer Perceptron (MLP)")
        self.play(FadeIn(banner), run_time=1)
        self.wait(0.5)

        # --- Input: Biomarker table ---
        biomarkers = [
            ["pH", "6.2"],
            ["Protein", "30 mg/dL"],
            ["Glucose", "Normal"],
            ["Sp. Gravity", "1.020"],
            ["Leukocytes", "Positive"],
        ]
        table = Table(
            [[row[1]] for row in biomarkers],
            row_labels=[Text(row[0], font_size=SUBLABEL_SIZE) for row in biomarkers],
            col_labels=[Text("Value", font_size=SUBLABEL_SIZE)],
            top_left_entry=Text("Biomarker", font_size=SUBLABEL_SIZE, color=DATA_GOLD),
            include_outer_lines=True,
            line_config={"color": GRAY, "stroke_width": 1},
            element_to_mobject_config={"font_size": SUBLABEL_SIZE},
        ).scale(0.5)

        table_label = Text("Urine Sample", font_size=LABEL_SIZE, color=DATA_GOLD)
        table_group = VGroup(table_label, table).arrange(DOWN, buff=0.2)
        table_group.move_to(LEFT * 5.5 + DOWN * 0.5)

        self.play(FadeIn(table_group), run_time=1.5)
        self.wait(0.5)

        # --- Input layer (5 nodes) ---
        input_layer = create_node_layer(5, color=DATA_GOLD)
        input_layer.move_to(LEFT * 2.8 + DOWN * 0.5)
        input_label = Text("Input\n(5 features)", font_size=SUBLABEL_SIZE, color=DATA_GOLD)
        input_label.next_to(input_layer, DOWN, buff=0.3)

        # Arrows from table to input nodes
        table_arrows = VGroup()
        for node in input_layer:
            arrow = Arrow(
                table.get_right(), node.get_left(),
                buff=0.15, color=DATA_GOLD, stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            )
            table_arrows.add(arrow)

        self.play(
            Create(input_layer),
            FadeIn(input_label),
            *[Create(a) for a in table_arrows],
            run_time=1.5,
        )
        self.wait(0.3)

        # --- Hidden Layer 1 (8 nodes) ---
        hidden1 = create_node_layer(8, color=LAYER_PURPLE)
        hidden1.move_to(LEFT * 0.5 + DOWN * 0.5)
        h1_block = create_layer_block("Hidden 1 (ReLU)", width=1.2, height=3.2, color=LAYER_PURPLE)
        h1_block.move_to(hidden1.get_center())
        h1_label = Text("8 neurons", font_size=SUBLABEL_SIZE - 2, color=LAYER_PURPLE)
        h1_label.next_to(h1_block, DOWN, buff=0.15)

        conn_1 = draw_connections(input_layer, hidden1, color=LAYER_PURPLE, opacity=0.15)

        self.play(
            Create(h1_block), Create(hidden1),
            FadeIn(h1_label),
            Create(conn_1),
            run_time=1.5,
        )

        # --- Hidden Layer 2 (6 nodes) ---
        hidden2 = create_node_layer(6, color=LAYER_TEAL)
        hidden2.move_to(RIGHT * 1.8 + DOWN * 0.5)
        h2_block = create_layer_block("Hidden 2 (ReLU)", width=1.2, height=2.6, color=LAYER_TEAL)
        h2_block.move_to(hidden2.get_center())
        h2_label = Text("6 neurons", font_size=SUBLABEL_SIZE - 2, color=LAYER_TEAL)
        h2_label.next_to(h2_block, DOWN, buff=0.15)

        conn_2 = draw_connections(hidden1, hidden2, color=LAYER_TEAL, opacity=0.12)

        self.play(
            Create(h2_block), Create(hidden2),
            FadeIn(h2_label),
            Create(conn_2),
            run_time=1.5,
        )

        # --- Output layer (2 nodes) ---
        output_healthy = Circle(
            radius=NODE_RADIUS * 1.3, color=HEALTHY_GREEN,
            fill_opacity=0.3, stroke_width=2,
        )
        output_unhealthy = Circle(
            radius=NODE_RADIUS * 1.3, color=UNHEALTHY_RED,
            fill_opacity=0.3, stroke_width=2,
        )
        output_layer = VGroup(output_healthy, output_unhealthy)
        output_layer.arrange(DOWN, buff=0.6)
        output_layer.move_to(RIGHT * 4.0 + DOWN * 0.5)

        label_healthy = Text("Healthy", font_size=SUBLABEL_SIZE - 2, color=HEALTHY_GREEN)
        label_healthy.next_to(output_healthy, RIGHT, buff=0.15)
        label_unhealthy = Text("Unhealthy", font_size=SUBLABEL_SIZE - 2, color=UNHEALTHY_RED)
        label_unhealthy.next_to(output_unhealthy, RIGHT, buff=0.15)

        conn_3 = draw_connections(hidden2, output_layer, color=WHITE, opacity=0.15)

        out_label = Text("Output", font_size=SUBLABEL_SIZE, color=WHITE)
        out_label.next_to(output_layer, DOWN, buff=0.4)

        self.play(
            Create(output_layer),
            FadeIn(label_healthy), FadeIn(label_unhealthy),
            FadeIn(out_label),
            Create(conn_3),
            run_time=1.5,
        )
        self.wait(0.3)

        # --- Data flow animation (pulses) ---
        # Pulse 1: input -> hidden1
        dots1, paths1 = create_pulse_dots(input_layer, hidden1, color=DATA_GOLD, count=6)
        self.add(*dots1)
        self.play(
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(dots1, paths1)],
            run_time=1.0,
        )
        self.remove(*dots1)

        # Pulse 2: hidden1 -> hidden2
        dots2, paths2 = create_pulse_dots(hidden1, hidden2, color=LAYER_PURPLE, count=6)
        self.add(*dots2)
        self.play(
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(dots2, paths2)],
            run_time=1.0,
        )
        self.remove(*dots2)

        # Pulse 3: hidden2 -> output
        dots3, paths3 = create_pulse_dots(hidden2, output_layer, color=LAYER_TEAL, count=4)
        self.add(*dots3)
        self.play(
            *[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(dots3, paths3)],
            run_time=1.0,
        )
        self.remove(*dots3)

        # --- Highlight output ---
        self.play(
            output_unhealthy.animate.set_fill(UNHEALTHY_RED, opacity=0.8).set_stroke(UNHEALTHY_RED, width=4),
            Indicate(output_unhealthy, color=UNHEALTHY_RED),
            run_time=1.0,
        )

        badge = create_output_badge("Prediction: UTI Detected", UNHEALTHY_RED)
        badge.next_to(output_layer, DOWN, buff=1.0)

        self.play(FadeIn(badge, shift=UP * 0.3), run_time=1.0)
        self.wait(2)
