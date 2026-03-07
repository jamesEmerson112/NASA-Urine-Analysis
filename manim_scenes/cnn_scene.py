import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from common import (
    NASA_BLUE, NASA_RED, HEALTHY_GREEN, UNHEALTHY_RED, DATA_GOLD,
    LAYER_PURPLE, LAYER_TEAL, BG_DARK,
    TITLE_SIZE, LABEL_SIZE, SUBLABEL_SIZE, NODE_RADIUS,
    create_layer_block, create_output_badge, create_title_banner,
    create_node_layer, draw_connections,
)


class CNNScene(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        # --- Title ---
        banner = create_title_banner("Convolutional Neural Network (CNN)")
        self.play(FadeIn(banner), run_time=1)
        self.wait(0.5)

        # --- Input: Urine test strip (colored reagent pads) ---
        pad_colors = ["#E8D44D", "#8BC34A", "#FF9800", "#9C27B0", "#F44336",
                       "#2196F3", "#795548", "#E91E63", "#00BCD4", "#CDDC39"]
        pad_labels = ["LEU", "NIT", "URO", "PRO", "pH",
                       "BLO", "SG", "KET", "BIL", "GLU"]

        strip_bg = RoundedRectangle(
            corner_radius=0.1, width=1.2, height=5.5,
            color=WHITE, fill_color="#F5F0E0", fill_opacity=0.9, stroke_width=1,
        )

        pads = VGroup()
        pad_texts = VGroup()
        for i, (col, lbl) in enumerate(zip(pad_colors, pad_labels)):
            pad = Square(side_length=0.4, color=col, fill_opacity=0.85, stroke_width=1)
            pads.add(pad)
            txt = Text(lbl, font_size=10, color=WHITE, weight=BOLD)
            txt.move_to(pad.get_center())
            pad_texts.add(txt)

        pads.arrange(DOWN, buff=0.08)
        strip_bg.move_to(pads.get_center())

        strip = VGroup(strip_bg, pads, pad_texts)
        for txt, pad in zip(pad_texts, pads):
            txt.move_to(pad.get_center())

        strip_label = Text("Urine Test Strip", font_size=LABEL_SIZE, color=DATA_GOLD)
        strip_group = VGroup(strip_label, strip).arrange(DOWN, buff=0.2)
        strip_group.move_to(LEFT * 5.2 + DOWN * 0.3)

        self.play(FadeIn(strip_group), run_time=1.5)
        self.wait(0.5)

        # --- Convolutional layer: sliding filter ---
        # Show a simplified 2D representation
        conv_label = Text("Conv2D Filters", font_size=SUBLABEL_SIZE, color=LAYER_PURPLE)
        conv_label.move_to(LEFT * 2.5 + UP * 2.5)

        # Kernel indicator
        kernel = Square(
            side_length=0.55, color=LAYER_PURPLE,
            fill_opacity=0.2, stroke_width=3,
        )
        kernel.move_to(pads[0].get_center())

        self.play(FadeIn(conv_label), Create(kernel), run_time=0.8)

        # Feature map outputs (build as kernel slides)
        feature_maps = VGroup()
        fm_colors = [LAYER_PURPLE, LAYER_TEAL, NASA_BLUE]
        for j in range(3):
            fm_stack = VGroup()
            for i in range(5):
                rect = Rectangle(
                    width=0.35, height=0.35,
                    color=fm_colors[j], fill_opacity=0.3 + i * 0.1,
                    stroke_width=1,
                )
                fm_stack.add(rect)
            fm_stack.arrange(DOWN, buff=0.04)
            feature_maps.add(fm_stack)
        feature_maps.arrange(RIGHT, buff=0.15)
        feature_maps.move_to(LEFT * 1.8 + DOWN * 0.3)

        fm_label = Text("Feature Maps", font_size=SUBLABEL_SIZE, color=LAYER_PURPLE)
        fm_label.next_to(feature_maps, DOWN, buff=0.3)

        # Animate kernel sliding down the strip
        for i in range(1, min(5, len(pads))):
            self.play(
                kernel.animate.move_to(pads[i].get_center()),
                run_time=0.4,
            )

        self.play(
            FadeOut(kernel),
            FadeIn(feature_maps),
            FadeIn(fm_label),
            run_time=1.0,
        )
        self.wait(0.3)

        # --- Pooling layer ---
        pool_block = create_layer_block("MaxPool", width=1.0, height=1.8, color=LAYER_TEAL)
        pool_block.move_to(RIGHT * 0.2 + DOWN * 0.3)

        pool_arrow = Arrow(
            feature_maps.get_right(), pool_block.get_left(),
            buff=0.15, color=LAYER_TEAL, stroke_width=2,
        )

        pooled_maps = VGroup()
        for j in range(3):
            fm_small = VGroup()
            for i in range(3):
                rect = Rectangle(
                    width=0.25, height=0.25,
                    color=fm_colors[j], fill_opacity=0.4 + i * 0.15,
                    stroke_width=1,
                )
                fm_small.add(rect)
            fm_small.arrange(DOWN, buff=0.03)
            pooled_maps.add(fm_small)
        pooled_maps.arrange(RIGHT, buff=0.1)
        pooled_maps.move_to(pool_block.get_center())

        self.play(
            Create(pool_arrow),
            FadeIn(pool_block),
            run_time=1.0,
        )
        self.play(
            FadeIn(pooled_maps),
            run_time=0.8,
        )
        self.wait(0.3)

        # --- Flatten ---
        flatten_label = Text("Flatten", font_size=SUBLABEL_SIZE, color=WHITE)
        flatten_label.move_to(RIGHT * 2.0 + UP * 1.5)

        flat_dots = create_node_layer(6, color=WHITE, radius=0.1)
        flat_dots.move_to(RIGHT * 2.0 + DOWN * 0.3)

        flatten_arrow = Arrow(
            pool_block.get_right(), flat_dots.get_left(),
            buff=0.15, color=WHITE, stroke_width=2,
        )

        self.play(
            Create(flatten_arrow),
            FadeIn(flatten_label),
            Transform(pooled_maps.copy(), flat_dots),
            run_time=1.2,
        )
        self.add(flat_dots)
        self.wait(0.3)

        # --- Dense layer ---
        dense_block = create_layer_block("Dense (128)", width=1.2, height=2.2, color=NASA_BLUE)
        dense_block.move_to(RIGHT * 3.8 + DOWN * 0.3)

        dense_nodes = create_node_layer(5, color=NASA_BLUE, radius=0.12)
        dense_nodes.move_to(dense_block.get_center())

        dense_arrow = Arrow(
            flat_dots.get_right(), dense_block.get_left(),
            buff=0.15, color=NASA_BLUE, stroke_width=2,
        )

        self.play(
            Create(dense_arrow),
            FadeIn(dense_block),
            Create(dense_nodes),
            run_time=1.0,
        )
        self.wait(0.3)

        # --- Output ---
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
        output_layer.move_to(RIGHT * 5.8 + DOWN * 0.3)

        lbl_h = Text("Healthy", font_size=SUBLABEL_SIZE - 2, color=HEALTHY_GREEN)
        lbl_h.next_to(output_healthy, RIGHT, buff=0.1)
        lbl_u = Text("Unhealthy", font_size=SUBLABEL_SIZE - 2, color=UNHEALTHY_RED)
        lbl_u.next_to(output_unhealthy, RIGHT, buff=0.1)

        out_arrow = Arrow(
            dense_block.get_right(), output_layer.get_left(),
            buff=0.15, color=WHITE, stroke_width=2,
        )

        self.play(
            Create(out_arrow),
            Create(output_layer),
            FadeIn(lbl_h), FadeIn(lbl_u),
            run_time=1.0,
        )

        # Highlight healthy output
        self.play(
            output_healthy.animate.set_fill(HEALTHY_GREEN, opacity=0.8),
            Indicate(output_healthy, color=HEALTHY_GREEN),
            run_time=1.0,
        )

        badge = create_output_badge("Prediction: Normal", HEALTHY_GREEN)
        badge.next_to(output_layer, DOWN, buff=0.8)

        self.play(FadeIn(badge, shift=UP * 0.3), run_time=1.0)
        self.wait(2)
