# ==============================================================================
# Scene:      OverlayToPointIn3d
# Source:     videos/_2019/hyperdarts.py (lines 1434-1469)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OverlayToPointIn3d.py OverlayToPointIn3d -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OverlayToPointIn3d(Scene):
    def construct(self):
        t2c = {
            "{x}": GREEN,
            "{y}": RED,
            "{z}": BLUE,
        }
        ineq = OldTex(
            "{x}^2 + {y}^2 + {z}^2 < 1",
            tex_to_color_map=t2c,
        )
        ineq.scale(1.5)
        ineq.move_to(FRAME_WIDTH * LEFT / 4)
        ineq.to_edge(UP)

        equiv = OldTex("\\Leftrightarrow")
        equiv.scale(2)
        equiv.match_y(ineq)

        rhs = OldTexText(
            "$({x}, {y}, {z})$",
            " lies within a\\\\sphere with radius 1"
        )
        rhs[0][1].set_color(GREEN)
        rhs[0][3].set_color(RED)
        rhs[0][5].set_color(BLUE)
        rhs.scale(1.3)
        rhs.next_to(equiv, RIGHT)
        rhs.to_edge(UP)

        self.add(ineq)
        self.wait()
        self.play(Write(equiv))
        self.wait()
        self.play(FadeIn(rhs))
        self.wait()
