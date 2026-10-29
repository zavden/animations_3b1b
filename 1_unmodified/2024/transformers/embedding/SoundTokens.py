# ==============================================================================
# Scene:      SoundTokens
# Source:     videos/_2024/transformers/embedding.py (lines 299-338)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SoundTokens.py SoundTokens -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SoundTokens(InteractiveScene):
    def construct(self):
        # Add wave form
        n_lines = 100
        wave_form = Line(UP, DOWN).replicate(n_lines)
        wave_form.arrange(RIGHT)
        wave_form.arrange_to_fit_width(5)
        wave_form.next_to(ORIGIN, RIGHT)

        def func(x):
            x *= 1.7
            return sum([
                math.sin(x),
                0.5 * math.sin(2 * x),
                0.3 * math.sin(3 * x),
                0.2 * math.sin(4 * x),
                0.1 * math.sin(5 * x),
                0.15 * math.sin(6 * x),
            ])

        for line in wave_form:
            line.set_height(abs(func(line.get_x())))

        wave_form.center()
        self.add(wave_form)

        # Subdivide
        step = 5
        chunks = VGroup(wave_form[i:i + step] for i in range(0, len(wave_form), step))

        self.add(chunks)
        self.wait()
        self.play(chunks.animate.space_out_submobjects(2.0).scale(0.75))
        self.play(LaggedStart(
            (chunk.animate.set_stroke(TEAL, 3).scale(1.5).set_anim_args(rate_func=there_and_back)
            for chunk in chunks),
            lag_ratio=2.0 / len(chunks),
            run_time=2
        ))
        self.wait()
