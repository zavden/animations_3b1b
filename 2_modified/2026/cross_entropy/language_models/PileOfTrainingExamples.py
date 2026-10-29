# ==============================================================================
# Scene:      PileOfTrainingExamples
# Source:     videos/_2026/cross_entropy/language_models.py (lines 758-800)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PileOfTrainingExamples.py PileOfTrainingExamples -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - text_data/quotes.txt and training_data_examples.txt: original text and public-domain quotes (_lib/assets/generated/2026/cross_entropy/text_data/) instead of 3b1b's, which quoted copyrighted works
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np
from pathlib import Path

def get_training_text_examples(file_name="training_data_examples.txt"):
    data_file = Path(__file__).parent / "text_data" / file_name
    return data_file.read_text().splitlines()


class PileOfTrainingExamples(InteractiveScene):
    def construct(self):
        # Load training examples
        examples = VGroup(
            Text(text, font_size=24)
            for text in get_training_text_examples()
        )
        examples.set_fill(GREY_A, 1)

        # Show training examples
        frame = self.frame

        examples.arrange(DOWN, aligned_edge=LEFT)
        examples.to_edge(DOWN)

        def camera_rate_func(t):
            return np.mean([smooth(t), t])

        frame.set_height(16)
        frame.move_to(examples, UP).shift(0.25 * UP)
        self.add(examples)
        self.play(
            LaggedStartMap(Write, examples, lag_ratio=0.08),
            frame.animate.move_to(examples, DOWN).shift(DOWN).set_anim_args(time_span=(1, 25), rate_func=camera_rate_func),
            run_time=25
        )
        self.wait()

        # Shift perspective
        self.play(
            frame.animate.reorient(32, 63, 0, (-2.09, 2.53, 0.23), 10.39),
            run_time=3
        )
        self.wait()

        # Pull out one example and tokenize
        example = examples[-1]
        self.play(
            LaggedStartMap(FadeOut, examples[-2::-1], shift=RIGHT, lag_ratio=0.01),
            example.animate.center().fix_in_frame().scale(2).set_color(WHITE),
            run_time=2
        )
        self.wait()
