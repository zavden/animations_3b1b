# ==============================================================================
# Scene:      QuarterTurn
# Source:     videos/_2018/pi_day.py (lines 646-676)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuarterTurn.py QuarterTurn -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_circle_drawing_terms(radius = 1, positioning_func = lambda m : m.center()):
    circle = Circle(color = YELLOW, radius = 1.25)
    positioning_func(circle)
    radius = Line(circle.get_center(), circle.get_points()[0])
    radius.set_color(WHITE)
    one = OldTex("1")
    one.scale(0.75)
    one_update = UpdateFromFunc(
        one, lambda m : m.move_to(
            radius.get_center() + \
            0.25*rotate_vector(radius.get_vector(), TAU/4)
        ),
    )
    decimal = DecimalNumber(0, num_decimal_places = 4, show_ellipsis = True)
    decimal.scale(0.75)
    def reposition_decimal(decimal):
        vect = radius.get_vector()
        unit_vect = vect/get_norm(vect)
        angle = radius.get_angle()
        alpha = (-np.cos(2*angle) + 1)/2
        interp_length = interpolate(decimal.get_width(), decimal.get_height(), alpha)
        buff = interp_length/2 + MED_SMALL_BUFF
        decimal.move_to(radius.get_end() + buff*unit_vect)
        decimal.shift(UP*decimal.get_height()/2)
        return decimal

    kwargs = {"run_time" : 3, "rate_func" : bezier([0, 0, 1, 1])} 
    changing_decimal = ChangingDecimal(
        decimal, lambda a : a*TAU,
        position_update_func = reposition_decimal,
        **kwargs
    )

    terms = VGroup(circle, radius, one, decimal)
    generate_anims1 = lambda : [ShowCreation(radius), Write(one)]
    generate_anims2 = lambda : [
        ShowCreation(circle, **kwargs),
        Rotating(radius, about_point = radius.get_start(), **kwargs),
        changing_decimal,
        one_update,
    ]

    return terms, generate_anims1, generate_anims2


class QuarterTurn(Scene):
    def construct(self):
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 2,
            positioning_func = lambda circ : circ.move_to(4*RIGHT)
        )
        circle, radius, one, decimal = terms
        circle_ghost = circle.copy().set_stroke(YELLOW_E, 1)
        radius_ghost = radius.copy().set_stroke(WHITE, 1)

        self.add(circle_ghost, radius_ghost)
        self.play(
            *generate_anims2(),
            rate_func = lambda t : 0.25*smooth(t)
        )
        self.wait()

        pi_halves = OldTex("\\pi", "/2")
        pi_halves[0].set_color(RED)
        tau_fourths = OldTex("\\tau", "/4")
        tau_fourths[0].set_color(GREEN)
        for mob in pi_halves, tau_fourths:
            mob.next_to(decimal, UP)

        self.play(FadeInFromDown(pi_halves))
        self.wait()
        self.play(
            pi_halves.shift, 0.75*UP,
            FadeInFromDown(tau_fourths)
        )
        self.wait()
