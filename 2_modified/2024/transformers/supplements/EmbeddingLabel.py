# ==============================================================================
# Scene:      EmbeddingLabel
# Source:     videos/_2024/transformers/supplements.py (lines 1466-1502)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EmbeddingLabel.py EmbeddingLabel -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/EmbeddingStill.jpg (placeholder; Grant's Dropbox path, which _lib resolves by name)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class EmbeddingLabel(InteractiveScene):
    def construct(self):
        # Background
        bg = ImageMobject("/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2024/transformers/images/EmbeddingStill.jpg")
        bg.set_height(FRAME_HEIGHT)
        # self.add(bg)

        # Label
        ghost_vect = Rectangle()
        ghost_vect.set_shape(0.8, 4)
        ghost_vect.move_to([4.25, -1.0, 0])

        brace = Brace(ghost_vect, LEFT)
        name = brace.get_text("Embedding")
        length = Integer(12288)
        length.next_to(brace, LEFT, buff=0.5).shift(0.25 * UP)
        numbers_label = Text("Numbers")
        numbers_label.next_to(length, DOWN)
        gpt3_label = Text("(Length in GPT-3)", font_size=24)
        gpt3_label.next_to(length, UP, buff=1.0),
        gpt3_label.set_color(YELLOW)
        arrow = Arrow(gpt3_label.get_bottom(), length.get_top(), buff=0.1)

        self.play(
            GrowFromCenter(brace),
            Write(name)
        )
        self.wait()
        self.play(
            FadeTransform(name, numbers_label),
            CountInFrom(length, 0, run_time=1.5),
        )
        self.play(
            FadeIn(gpt3_label, lag_ratio=0.1),
            GrowFromCenter(arrow),
        )
        self.wait(1.5)
