# ==============================================================================
# Scene:      ConnectingArrow
# Source:     videos/_2023/clt_proof/main.py (lines 1548-1574)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConnectingArrow.py ConnectingArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConnectingArrow(InteractiveScene):
    def construct(self):
        # Test
        arrow = CubicBezier(
            np.array([-0.5, -3.33, 0]),
            np.array([3, -3.33, 0]),
            np.array([-1, 1.0, 0]),
            np.array([0.7, 1.85, 0]),
        )
        arrow.set_stroke(RED_E, 8)
        line = Line(*arrow.get_points()[-2:])
        line.add_tip()
        tip = line.tip
        tip.shift(0.25 * line.get_vector())
        tip.set_fill(RED_E, 1)

        label = TexText(R"$m^{\text{th}}$ cumulant of $\frac{X_1 + \cdots + X_n}{\sigma \sqrt{n}}$")
        label.set_fill(RED_E)
        label.set_stroke(BLACK, 2, background=True)
        label.next_to(arrow.pfp(0.5), RIGHT, SMALL_BUFF)

        self.play(
            ShowCreation(arrow),
            FadeIn(tip, time_span=(0.8, 1.0))
        )
        self.play(Write(label, stroke_color=BLACK, lag_ratio=0.2))
        self.wait()
