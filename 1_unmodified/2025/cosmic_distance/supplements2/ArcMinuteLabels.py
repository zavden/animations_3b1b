# ==============================================================================
# Scene:      ArcMinuteLabels
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 574-589)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArcMinuteLabels.py ArcMinuteLabels -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArcMinuteLabels(InteractiveScene):
    def construct(self):
        # Test
        brace = Brace(Line(3 * DOWN, 3 * UP), LEFT)
        am_label = brace.get_text("60 arc-minutes")
        as_label = Text("60 arc-seconds", t2s={"seconds": ITALIC})
        as_label["seconds"].set_color(YELLOW)
        as_label.move_to(am_label, RIGHT)

        for label in [am_label, as_label]:
            self.clear()
            self.play(
                GrowFromCenter(brace),
                FadeIn(label, scale=3, shift=1 * LEFT)
            )
            self.wait()
