# ==============================================================================
# Scene:      PredictorCompressorTitle
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 650-661)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PredictorCompressorTitle.py PredictorCompressorTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PredictorCompressorTitle(InteractiveScene):
    def construct(self):
        group = VGroup(
            Text("Predictor", font_size=72, fill_color="#951FF4").set_x(-FRAME_WIDTH / 4),
            Tex(R"\longleftrightarrow", font_size=120),
            Text("Compressor", font_size=72, fill_color="#74F9BB").set_x(FRAME_WIDTH / 4),
        )
        group.to_edge(UP)
        self.add(group[::2])
        self.wait()
        self.play(GrowFromCenter(group[1]))
        self.wait()
