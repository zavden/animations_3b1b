# ==============================================================================
# Scene:      RotationAnnotation
# Source:     videos/_2022/puzzles/subsets.py (lines 4596-4615)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationAnnotation.py RotationAnnotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RotationAnnotation(InteractiveScene):
    def construct(self):
        arc = Arc(0, PI, radius=0.5)
        label = Integer(180, unit="^\\circ", font_size=24)
        label.next_to(arc.pfp(0.25), UR, SMALL_BUFF)

        morty = Mortimer(height=1.5)
        morty.next_to(arc, RIGHT, LARGE_BUFF, aligned_edge=DOWN)

        self.play(
            CountInFrom(label, 0),
            ShowCreation(arc),
            PiCreatureSays(
                morty, OldTexText("Think about\\\\the half turn", font_size=24),
                look_at=arc,
                bubble_config=dict(width=2, height=1.5)
            )
        )
        self.play(Blink(morty))
        self.wait()
