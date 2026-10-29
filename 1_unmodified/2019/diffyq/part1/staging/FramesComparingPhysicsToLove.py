# ==============================================================================
# Scene:      FramesComparingPhysicsToLove
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2891-2927)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl FramesComparingPhysicsToLove.py FramesComparingPhysicsToLove -w -m --fps 15
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


def get_heart_var(index):
    heart = SuitSymbol("hearts")
    if index == 1:
        heart.set_color(BLUE_C)
    elif index == 2:
        heart.set_color(GREEN)
    heart.set_height(0.7)
    index = Integer(index)
    index.move_to(heart.get_corner(DR))
    heart.add(index)
    return heart


def get_heart_var_deriv(index):
    heart = get_heart_var(index)
    filler_tex = "T"
    deriv = OldTex("{d", filler_tex, "\\over", "dt}")
    deriv.scale(2)
    filler = deriv.get_part_by_tex(filler_tex)
    heart.match_height(filler)
    heart.move_to(filler)
    heart.scale(1.5, about_edge=UL)
    deriv.remove(filler)
    deriv.add(heart)
    deriv.heart = heart
    return deriv


def get_love_equation1():
    equation = VGroup(
        get_heart_var_deriv(1),
        OldTex("=").scale(2),
        OldTex("a").scale(2),
        get_heart_var(2)
    )
    equation.arrange(RIGHT)
    equation[-1].shift(SMALL_BUFF * DL)
    return equation


def get_love_equation2():
    equation = VGroup(
        get_heart_var_deriv(2),
        OldTex("=").scale(2),
        OldTex("-b").scale(2),
        get_heart_var(1),
    )
    equation.arrange(RIGHT)
    equation[-1].shift(SMALL_BUFF * DL)
    return equation



# ----- From _2019/diffyq/part1/staging.py -----

class FramesComparingPhysicsToLove(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY_E}
    }

    def construct(self):
        ode = get_ode()
        ode.to_edge(UP)

        love = VGroup(
            get_love_equation1(),
            get_love_equation2(),
        )
        love.scale(0.5)
        love.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        frames = VGroup(*[
            ScreenRectangle(
                height=3.5,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)
        frames.shift(DOWN)

        animated_frames = AnimatedBoundary(frames)

        ode.next_to(frames[0], UP)
        love.next_to(frames[1], UP)

        self.add(frames, animated_frames)
        self.add(ode, love)

        self.wait(15)
