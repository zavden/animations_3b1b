# ==============================================================================
# Scene:      PauseAndPlayOverlay
# Source:     videos/_2018/quat3d.py (lines 508-534)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PauseAndPlayOverlay.py PauseAndPlayOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PauseAndPlayOverlay(Scene):
    def construct(self):
        pause = OldTex("=").rotate(TAU / 4)
        pause.stretch(2, 0)
        pause.scale(1.5)
        arrow = Vector(RIGHT, color=WHITE)
        interact = OldTexText("Interact...")
        group = VGroup(pause, arrow, interact)
        group.arrange(RIGHT)
        group.scale(2)

        not_yet = OldTexText("...well, not yet")
        not_yet.scale(2)
        not_yet.next_to(group, DOWN, MED_LARGE_BUFF)

        self.play(Write(pause))
        self.play(
            GrowFromPoint(
                interact, arrow.get_left(),
                rate_func=squish_rate_func(smooth, 0.3, 1)
            ),
            VFadeIn(interact),
            GrowArrow(arrow),
        )
        self.wait(2)
        self.play(Write(not_yet))
        self.wait()
