import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from common import (
    NASA_BLUE, NASA_RED, HEALTHY_GREEN, UNHEALTHY_RED, DATA_GOLD,
    LAYER_PURPLE, LAYER_TEAL, BG_DARK,
    TITLE_SIZE, LABEL_SIZE, SUBLABEL_SIZE, NODE_RADIUS,
    create_layer_block, create_output_badge, create_title_banner,
)


class TransformerScene(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        # --- Title ---
        banner = create_title_banner("Transformer (Self-Attention)")
        self.play(FadeIn(banner), run_time=1)
        self.wait(0.5)

        # --- Input: Sequential biomarker readings ---
        readings = [
            ("Day 1", "pH 6.5"),
            ("Day 2", "pH 6.0"),
            ("Day 3", "pH 5.8"),
            ("Day 4", "Pro 45"),
            ("Day 5", "Pro 80"),
            ("Day 6", "Pro 95"),
        ]

        tokens = VGroup()
        for day, val in readings:
            box = RoundedRectangle(
                corner_radius=0.1, width=1.1, height=0.85,
                color=DATA_GOLD, fill_opacity=0.15, stroke_width=2,
            )
            day_text = Text(day, font_size=12, color=DATA_GOLD, weight=BOLD)
            val_text = Text(val, font_size=11, color=WHITE)
            content = VGroup(day_text, val_text).arrange(DOWN, buff=0.06)
            content.move_to(box.get_center())
            tokens.add(VGroup(box, content))

        tokens.arrange(RIGHT, buff=0.15)
        tokens.move_to(DOWN * 2.2)

        seq_label = Text("Sequential Biomarker Readings", font_size=LABEL_SIZE, color=DATA_GOLD)
        seq_label.next_to(tokens, DOWN, buff=0.3)

        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tokens], lag_ratio=0.15),
            FadeIn(seq_label),
            run_time=2.0,
        )
        self.wait(0.3)

        # --- Positional Encoding ---
        pe_indicators = VGroup()
        for i, token in enumerate(tokens):
            wave = Text(f"+PE{i+1}", font_size=10, color=LAYER_TEAL)
            wave.next_to(token, UP, buff=0.08)
            pe_indicators.add(wave)

        pe_label = Text("Positional Encoding", font_size=SUBLABEL_SIZE, color=LAYER_TEAL)
        pe_label.next_to(pe_indicators, UP, buff=0.15)

        self.play(
            LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in pe_indicators], lag_ratio=0.1),
            FadeIn(pe_label),
            run_time=1.2,
        )

        # Move tokens + PE up to make room
        token_group = VGroup(tokens, pe_indicators, pe_label, seq_label)
        self.play(token_group.animate.shift(DOWN * 0.3), run_time=0.5)
        self.wait(0.3)

        # --- Self-Attention Mechanism ---
        attn_label = Text("Self-Attention", font_size=LABEL_SIZE, color=LAYER_PURPLE)
        attn_label.move_to(UP * 0.2)

        self.play(FadeIn(attn_label), run_time=0.5)

        # Draw attention arrows with varying strength
        # Day 5 (Pro 80) attends strongly to Day 4 (Pro 45) and Day 6 (Pro 95)
        # Day 3 (pH 5.8) attends to Day 1 and Day 2
        attention_pairs = [
            (4, 3, 0.9),   # Day5 -> Day4 (strong)
            (4, 5, 0.85),  # Day5 -> Day6 (strong)
            (5, 3, 0.8),   # Day6 -> Day4 (strong)
            (2, 0, 0.6),   # Day3 -> Day1 (moderate)
            (2, 1, 0.7),   # Day3 -> Day2 (moderate)
            (1, 0, 0.5),   # Day2 -> Day1 (moderate)
            (3, 2, 0.4),   # Day4 -> Day3 (weak)
            (0, 5, 0.2),   # Day1 -> Day6 (weak)
        ]

        attn_arrows = VGroup()
        for src, tgt, weight in attention_pairs:
            src_pos = tokens[src].get_top() + UP * 0.3
            tgt_pos = tokens[tgt].get_top() + UP * 0.3

            if src == tgt:
                continue

            arrow = CurvedArrow(
                src_pos, tgt_pos,
                angle=PI * 0.4 * (1 if src > tgt else -1),
                color=LAYER_PURPLE,
                stroke_opacity=weight,
                stroke_width=1.5 + weight * 2.5,
                tip_length=0.15,
            )
            attn_arrows.add(arrow)

        self.play(
            LaggedStart(*[Create(a) for a in attn_arrows], lag_ratio=0.12),
            run_time=2.5,
        )
        self.wait(0.5)

        # --- Attention heatmap (small matrix) ---
        heatmap_size = 6
        cell_size = 0.28
        heatmap = VGroup()

        # Attention weight matrix (simplified)
        weights = [
            [0.5, 0.2, 0.1, 0.05, 0.05, 0.1],
            [0.5, 0.3, 0.1, 0.05, 0.03, 0.02],
            [0.3, 0.35, 0.2, 0.1, 0.03, 0.02],
            [0.1, 0.1, 0.2, 0.3, 0.2, 0.1],
            [0.05, 0.05, 0.05, 0.45, 0.2, 0.2],
            [0.03, 0.02, 0.05, 0.4, 0.2, 0.3],
        ]

        for r in range(heatmap_size):
            for c in range(heatmap_size):
                cell = Square(
                    side_length=cell_size,
                    color=LAYER_PURPLE,
                    fill_opacity=weights[r][c],
                    stroke_width=0.5,
                    stroke_color=GRAY,
                )
                cell.move_to(
                    RIGHT * (c * cell_size) + DOWN * (r * cell_size)
                )
                heatmap.add(cell)

        heatmap.move_to(RIGHT * 4.5 + UP * 0.2)
        hm_label = Text("Attention Weights", font_size=SUBLABEL_SIZE - 2, color=LAYER_PURPLE)
        hm_label.next_to(heatmap, UP, buff=0.15)

        # Axis labels
        q_label = Text("Q", font_size=12, color=WHITE)
        q_label.next_to(heatmap, LEFT, buff=0.15)
        k_label = Text("K", font_size=12, color=WHITE)
        k_label.next_to(heatmap, UP, buff=0.02).shift(LEFT * 0.05)

        self.play(
            FadeIn(heatmap), FadeIn(hm_label),
            FadeIn(q_label), FadeIn(k_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # --- Feed-Forward + LayerNorm ---
        ffn_block = create_layer_block("FFN + LayerNorm", width=2.5, height=0.7, color=LAYER_TEAL)
        ffn_block.move_to(UP * 1.8)

        ffn_arrow = Arrow(
            attn_label.get_top(), ffn_block.get_bottom(),
            buff=0.15, color=LAYER_TEAL, stroke_width=2,
        )

        self.play(
            FadeOut(attn_arrows),
            Create(ffn_arrow),
            FadeIn(ffn_block),
            run_time=1.2,
        )
        self.wait(0.3)

        # --- Classification Head ---
        cls_block = create_layer_block("Classification Head", width=2.2, height=0.6, color=NASA_BLUE)
        cls_block.next_to(ffn_block, UP, buff=0.5)

        cls_arrow = Arrow(
            ffn_block.get_top(), cls_block.get_bottom(),
            buff=0.1, color=NASA_BLUE, stroke_width=2,
        )

        self.play(
            Create(cls_arrow),
            FadeIn(cls_block),
            run_time=1.0,
        )
        self.wait(0.3)

        # --- Output badge ---
        badge = create_output_badge("Kidney Disease Risk: Elevated", UNHEALTHY_RED)
        badge.next_to(cls_block, RIGHT, buff=0.5)

        self.play(
            Indicate(cls_block, color=UNHEALTHY_RED),
            run_time=0.8,
        )
        self.play(FadeIn(badge, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2)
