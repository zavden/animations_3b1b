# ==============================================================================
# Scene:      SevenHourMarker
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 208-217)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SevenHourMarker.py SevenHourMarker -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SevenHourMarker(InteractiveScene):
    def construct(self):
        brace = Brace(Line(2 * LEFT, 2 * RIGHT))
        label = Tex(R"\sim 7 \text{ hours}")
        label[0].next_to(label[1], LEFT, buff=0.025)
        label.next_to(brace, DOWN)
        VGroup(brace, label).set_fill(BLACK)

        self.play(GrowFromCenter(brace), Write(label))
        self.wait()
