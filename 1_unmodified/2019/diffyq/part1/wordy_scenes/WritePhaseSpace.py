# ==============================================================================
# Scene:      WritePhaseSpace
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 312-339)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WritePhaseSpace.py WritePhaseSpace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WritePhaseSpace(Scene):
    def construct(self):
        word = OldTexText("Phase space")
        word.scale(2)
        word.shift(FRAME_WIDTH * LEFT / 4)
        word.to_edge(UP)
        word.add_background_rectangle()

        lines = VGroup(*[
            Line(v, 1.3 * v)
            for v in compass_directions(50)
        ])
        lines.replace(word, stretch=True)
        lines.scale(1.5)
        lines.set_stroke(YELLOW)
        lines.shuffle()

        self.add(word)
        self.play(
            ShowPassingFlashWithThinningStrokeWidth(
                lines,
                lag_ratio=0.002,
                run_time=1.5,
                time_width=0.9,
                n_segments=5,
            )
        )
        self.wait()
