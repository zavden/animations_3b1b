# ==============================================================================
# Scene:      TankAnnotations
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 256-266)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TankAnnotations.py TankAnnotations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TankAnnotations(InteractiveScene):
    def construct(self):
        # self.add(ImageMobject("TankStill").set_height(FRAME_HEIGHT))
        point = LEFT
        words = Text("First contact!", font_size=24)
        words.next_to(point, DOWN)
        self.play(
            Flash(point),
            FadeIn(words, run_time=0.5)
        )
        self.wait()
