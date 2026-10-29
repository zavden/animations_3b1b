# ==============================================================================
# Scene:      ExampleTypicalODE
# Source:     videos/_2019/diffyq/part1/staging.py (lines 1200-1239)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ExampleTypicalODE.py ExampleTypicalODE -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/staging.py -----

class ExampleTypicalODE(TeacherStudentsScene):
    def construct(self):
        examples = VGroup(
            OldTex(
                "{\\dot x}(t) = k{x}(t)",
                tex_to_color_map={
                    "{\\dot x}": BLUE,
                    "{x}": BLUE,
                },
            ),
            get_ode(),
            OldTex(
                "{\\partial T", "\\over", "\\partial t} = ",
                "{\\partial^2 T", "\\over", "\\partial x^2}", "+",
                "{\\partial^2 T", "\\over", "\\partial y^2}", "+",
                "{\\partial^2 T", "\\over", "\\partial z^2}",
                tex_to_color_map={
                    "T": RED,
                }
            ),
        )
        examples[1].get_parts_by_tex("theta").set_color(GREEN)
        examples.arrange(DOWN, buff=MED_LARGE_BUFF)
        examples.to_edge(UP)

        self.play(
            FadeIn(examples[0], UP),
            self.teacher.change, "raise_right_hand",
        )
        self.play(
            FadeIn(examples[1], UP),
            self.change_students(
                *3 * ["pondering"],
                look_at=examples,
            ),
        )
        self.play(
            FadeIn(examples[2], UP)
        )
        self.wait(5)
