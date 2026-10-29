# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/qa_round_two.py (lines 167-186)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/efvgt.py
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/efvgt.py -----

class ConfettiSpiril(Animation):
    CONFIG = {
        "x_start" : 0,
        "spiril_radius" : 0.5,
        "num_spirils" : 4,
        "run_time" : 10,
        "rate_func" : None,
    }
    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        mobject.next_to(self.x_start*RIGHT + FRAME_Y_RADIUS*UP, UP)
        self.total_vert_shift = \
            FRAME_HEIGHT + mobject.get_height() + 2*MED_SMALL_BUFF
        
        Animation.__init__(self, mobject, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.set_points(starting_submobject.get_points())

    def interpolate_mobject(self, alpha):
        Animation.interpolate_mobject(self, alpha)
        angle = alpha*self.num_spirils*2*np.pi
        vert_shift = alpha*self.total_vert_shift

        start_center = self.mobject.get_center()
        self.mobject.shift(self.spiril_radius*OUT)
        self.mobject.rotate(angle, axis = UP, about_point = start_center)
        self.mobject.shift(vert_shift*DOWN)


def get_confetti_animations(num_confetti_squares):
    colors = [RED, YELLOW, GREEN, BLUE, PURPLE, RED]
    confetti_squares = [
        Square(
            side_length = 0.2,
            stroke_width = 0,
            fill_opacity = 0.75,
            fill_color = random.choice(colors),
        )
        for x in range(num_confetti_squares)
    ]
    confetti_spirils = [
        ConfettiSpiril(
            square,
            x_start = 2*random.random()*FRAME_X_RADIUS - FRAME_X_RADIUS,
            rate_func = squish_rate_func(rush_from, a, a+0.5)
        )
        for a, square in zip(
            np.linspace(0, 0.5, num_confetti_squares),
            confetti_squares
        )
    ]
    return confetti_spirils


class Thumbnail(Scene):
    def construct(self):
        formula = OldTex("e^", "{\\pi i}", "=", "-1")
        formula[1].set_color(GREEN_B)
        formula[3].set_color(YELLOW)
        formula.scale(4)
        formula.to_edge(UP, buff = LARGE_BUFF)
        self.add(formula)

        via = OldTexText("via")
        via.scale(2)
        groups = OldTexText("Group theory")
        groups.scale(3)
        groups.to_edge(DOWN)
        via.move_to(VGroup(formula, groups))
        self.add(via, groups)



# ----- From _2017/qa_round_two.py -----

class Thumbnail(Scene):
    def construct(self):
        equation = OldTex("2^{19} = " + "{:,}".format(2**19))
        equation.set_width(FRAME_X_RADIUS)
        equation.to_edge(DOWN, buff = LARGE_BUFF)

        q_and_a = OldTexText("Q\\&A \\\\ Round 2")
        q_and_a.set_color_by_gradient(BLUE, YELLOW)
        q_and_a.set_width(FRAME_X_RADIUS)
        q_and_a.to_edge(UP, buff = LARGE_BUFF)

        eater = ImageMobject("eater", height = 3)
        eater.to_corner(UP+RIGHT, buff = 0)

        confetti_anims = get_confetti_animations(100)
        for anim in confetti_anims:
            anim.update(0.5)
        confetti = VGroup(*[a.mobject for a in confetti_anims])

        self.add(equation, q_and_a, eater)
