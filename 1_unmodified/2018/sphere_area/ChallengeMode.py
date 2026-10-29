# ==============================================================================
# Scene:      ChallengeMode
# Source:     videos/_2018/sphere_area.py (lines 2746-2752)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChallengeMode.py ChallengeMode -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ChallengeMode(Scene):
    def construct(self):
        words = OldTexText("Challenge mode: Predict the proof")
        words.scale(1.5)
        words.to_edge(UP)
        self.play(Write(words))
        self.wait()
