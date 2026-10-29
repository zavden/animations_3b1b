# ==============================================================================
# Scene:      HammingThinking
# Source:     videos/_2020/hamming.py (lines 6143-6158)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HammingThinking.py HammingThinking -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HammingThinking(Scene):
    def construct(self):
        hamming = ImageMobject("Richard_Hamming")
        hamming.set_height(3)
        hamming.to_corner(DL)
        randy = Randolph()
        randy.set_opacity(0)
        randy.move_to(hamming)

        self.add(hamming)
        self.wait()
        self.play(PiCreatureBubbleIntroduction(
            randy, "What's the most efficient\\\\I could conceivably be?",
            bubble_type=ThoughtBubble,
        ))
        self.wait()
