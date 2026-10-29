# ==============================================================================
# Scene:      PiTauDebate
# Source:     videos/_2018/pi_day.py (lines 266-352)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiTauDebate.py PiTauDebate -w -m --fps 15
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


class PiTauDebate(PiCreatureScene):
    def construct(self):
        pi, tau = self.pi, self.tau
        self.add(pi, tau)

        pi_value = OldTexText("3.1415...!")
        pi_value.set_color(BLUE)
        tau_value = OldTexText("6.2831...!")
        tau_value.set_color(GREEN)

        self.play(PiCreatureSays(
            pi, pi_value,
            target_mode = "angry",
            look_at = tau.eyes,
            # bubble_config = {"width" : 3}
        ))
        self.play(PiCreatureSays(
            tau, tau_value,
            target_mode = "angry",
            look_at = pi.eyes,
            bubble_config = {"width" : 3, "height" : 2},
        ))
        self.wait()

        # Show tau
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 1.25,
            positioning_func = lambda m : m.to_edge(RIGHT, buff = 2).to_edge(UP, buff = 1)
        )
        circle, radius, one, decimal = terms

        self.play(
            RemovePiCreatureBubble(pi),
            RemovePiCreatureBubble(tau),
            *generate_anims1()
        )
        self.play(
            tau.change, "hooray",
            pi.change, "sassy",
            *generate_anims2()
        )
        self.wait()


        # Show pi
        circle = Circle(color = RED, radius = 1.25/2)
        circle.rotate(TAU/4)
        circle.move_to(pi)
        circle.to_edge(UP, buff = MED_LARGE_BUFF)
        diameter = Line(circle.get_left(), circle.get_right())
        one = OldTex("1")
        one.scale(0.75)
        one.next_to(diameter, UP, SMALL_BUFF)

        circum_line = diameter.copy().scale(np.pi)
        circum_line.match_style(circle)
        circum_line.next_to(circle, DOWN, buff = MED_LARGE_BUFF)
        # circum_line.to_edge(LEFT)
        brace = Brace(circum_line, DOWN, buff = SMALL_BUFF)
        decimal = DecimalNumber(np.pi, num_decimal_places = 4, show_ellipsis = True)
        decimal.scale(0.75)
        decimal.next_to(brace, DOWN, SMALL_BUFF)

        self.play(
            FadeIn(VGroup(circle, diameter, one)),
            tau.change, "confused",
            pi.change, "hooray"
        )
        self.add(circle.copy().fade(0.5))
        self.play(
            ReplacementTransform(circle, circum_line, run_time = 2)
        )
        self.play(GrowFromCenter(brace), Write(decimal))
        self.wait(3)
        # self.play()


    def create_pi_creatures(self):
        pi = self.pi = Randolph()
        pi.to_edge(DOWN).shift(4*LEFT)
        tau = self.tau = TauCreature(
            # mode = "angry",
            file_name_prefix = "TauCreatures",
            color = GREEN_E
        ).flip()
        tau.to_edge(DOWN).shift(4*RIGHT)
        return VGroup(pi, tau)
