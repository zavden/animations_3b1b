# ==============================================================================
# Scene:      ZetaSpiral
# Source:     videos/outside_videos/analysis.py (lines 178-219)
# Category:   2 · Renders with modifications
# Includes code copied from: _2016/zeta.py
#
# Run from this folder:
#     manimgl ZetaSpiral.py ZetaSpiral -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - np.complex no longer exists in numpy 2; complex is used
#   - ParametricCurve: t_min/t_max -> t_range=(min, max, step)
#   - background_stroke_width=0 is removed (it is no longer an OldTex parameter and 0 is the default behavior)
# ==============================================================================

from manim_imports_ext import *
import mpmath


# ----- From _2016/zeta.py -----

mpmath.mp.dps = 7


def zeta(z):
    max_norm = FRAME_X_RADIUS
    try:
        # CHANGE: np.complex no longer exists in numpy 2; complex is used
        return complex(mpmath.zeta(z))
    except:
        return complex(max_norm, 0)



# ----- From outside_videos/analysis.py -----

class ZetaSpiral(Scene):
    def construct(self):
        max_t = 50
        spiral = VGroup(*[
            ParametricCurve(
                lambda t: complex_to_R3(
                    zeta(complex(0.5, t))
                ),
                # CHANGE: ParametricCurve: t_min/t_max -> t_range=(min, max, step)
                t_range=(t1, t2 + 0.1, 0.01),
            )
            for t1, t2 in zip(it.count(), range(1, max_t))
        ])
        spiral.set_stroke(width=0, background=True)
        # spiral.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        # spiral.set_color_by_gradient(BLUE, YELLOW)
        spiral.set_color(YELLOW)

        width = 10
        for piece in spiral:
            piece.set_stroke(width=width)
            width *= 0.98
            dot = Dot()
            dot.scale(0.25)
            dot.match_color(piece)
            dot.set_stroke(BLACK, 1, background=True)
            dot.move_to(piece.get_start())
            # piece.add(dot)

        label = OldTex(
            "\\zeta\\left(0.5 + i{t}\\right)",
            # CHANGE: background_stroke_width=0 is removed (it is no longer an OldTex parameter and 0 is the default behavior)
            tex_to_color_map={"{t}": YELLOW},
        )
        label.scale(1.5)
        label.next_to(spiral, DOWN)

        group = VGroup(spiral, label)
        group.set_height(FRAME_HEIGHT - 1)
        group.center()

        self.add(group)
