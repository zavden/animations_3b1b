# ==============================================================================
# Scene:      ShowDotProductChanging
# Source:     videos/_2018/cramer.py (lines 1137-1201)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDotProductChanging.py ShowDotProductChanging -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDotProductChanging(LinearTransformationScene):
    CONFIG = {
        "matrix": [[2, -5.0 / 3], [-5.0 / 3, 2]],
        "v": [1, 2],
        "w": [2, 1],
        "v_label": "v",
        "w_label": "w",
        "v_color": YELLOW,
        "w_color": MAROON_B,
        "rhs1": "> 0",
        "rhs2": "< 0",
        "foreground_plane_kwargs": {
            "x_radius": 2 * FRAME_WIDTH,
            "y_radius": 2 * FRAME_HEIGHT,
        },
        "equation_scale_factor": 1.5,
    }

    def construct(self):
        v_mob = self.add_vector(self.v, self.v_color, animate=False)
        w_mob = self.add_vector(self.w, self.w_color, animate=False)
        kwargs = {
            "transformation_name": "T",
            "at_tip": True,
            "animate": False,
        }
        v_label = self.add_transformable_label(v_mob, self.v_label, **kwargs)
        w_label = self.add_transformable_label(w_mob, self.w_label, **kwargs)

        start_equation = self.get_equation(v_label, w_label, self.rhs1)
        start_equation.to_corner(UR)
        self.play(
            Write(start_equation[0::2]),
            ReplacementTransform(v_label.copy(), start_equation[1]),
            ReplacementTransform(w_label.copy(), start_equation[3]),
        )
        self.wait()
        self.add_foreground_mobject(start_equation)
        self.apply_matrix(self.matrix)
        self.wait()

        end_equation = self.get_equation(v_label, w_label, self.rhs2)
        end_equation.next_to(start_equation, DOWN, aligned_edge=RIGHT)
        self.play(
            FadeIn(end_equation[0]),
            ReplacementTransform(
                start_equation[2::2].copy(),
                end_equation[2::2],
            ),
            ReplacementTransform(v_label.copy(), end_equation[1]),
            ReplacementTransform(w_label.copy(), end_equation[3]),
        )
        self.wait(2)

    def get_equation(self, v_label, w_label, rhs):
        equation = VGroup(
            v_label.copy(),
            OldTex("\\cdot"),
            w_label.copy(),
            OldTex(rhs),
        )
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.add_to_back(BackgroundRectangle(equation))
        equation.scale(self.equation_scale_factor)
        return equation
