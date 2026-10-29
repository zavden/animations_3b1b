# ==============================================================================
# Scene:      SetAsideSeekingSolution
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 425-470)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl SetAsideSeekingSolution.py SetAsideSeekingSolution -w -m --fps 15
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



# ----- From _2019/diffyq/part1/wordy_scenes.py -----

class SetAsideSeekingSolution(Scene):
    def construct(self):
        ode = get_ode()
        ode.to_edge(UP)
        q1 = OldTexText("Find an exact solution")
        q1.set_color(YELLOW)
        q2 = OldTex(
            "\\text{What is }", "\\theta", "(t)",
            "\\text{'s personality?}",
            tex_to_color_map={"\\theta": BLUE},
            arg_separator="",
        )
        theta = q2.get_part_by_tex("\\theta")

        for q in q1, q2:
            q.scale(1.5)
            q.next_to(ode, DOWN, MED_LARGE_BUFF)
        eyes = Eyes(theta, height=0.1)

        self.add(ode)
        self.add(q1)
        self.wait()
        self.play(
            q1.scale, 0.3,
            q1.to_corner, UR, MED_SMALL_BUFF,
        )
        self.play(FadeIn(q2, DOWN))
        self.play(
            eyes.blink,
            rate_func=lambda t: smooth(1 - t),
        )
        self.play(eyes.look_at, q2.get_left())
        self.play(eyes.look_at, q2.get_right())
        self.play(
            eyes.blink,
            rate_func=squish_rate_func(there_and_back)
        )
        self.wait()
        self.play(
            eyes.change_mode, "confused",
            eyes.look_at, ode.get_left(),
        )
        self.play(
            eyes.blink,
            rate_func=squish_rate_func(there_and_back)
        )
