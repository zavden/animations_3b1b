# ==============================================================================
# Scene:      ComparePhysicsToLove
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2855-2888)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ComparePhysicsToLove.py ComparePhysicsToLove -w -m --fps 15
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

class ComparePhysicsToLove(Scene):
    def construct(self):
        ode = get_ode()
        ode.to_edge(UP)
        thetas = ode.get_parts_by_tex("theta")

        love = VGroup(
            get_love_equation1(),
            get_love_equation2(),
        )
        love.scale(0.5)
        love.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        love.move_to(DOWN)
        hearts = VGroup(*filter(
            lambda sm: isinstance(sm, SuitSymbol),
            love.get_family()
        ))

        arrow = DoubleArrow(love.get_top(), ode.get_bottom())

        self.play(FadeIn(ode, DOWN))
        self.play(FadeIn(love, UP))
        self.wait()
        self.play(LaggedStartMap(
            ShowCreationThenFadeAround,
            thetas,
        ))
        self.play(LaggedStartMap(
            ShowCreationThenFadeAround,
            hearts,
        ))
        self.wait()
        self.play(ShowCreation(arrow))
        self.wait()
