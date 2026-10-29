# ==============================================================================
# Scene:      PowersOfTwo
# Source:     videos/_2017/qa_round_two.py (lines 47-127)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/efvgt.py
#
# Run from this folder:
#     manimgl PowersOfTwo.py PowersOfTwo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo iterated a mobject with points as [itself]+submobjects; GL iterates only the submobjects (a bare Rectangle gave an empty group)
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



# ----- From _2017/qa_round_two.py -----

class PowersOfTwo(Scene):
    def construct(self):
        powers_of_2 = VGroup(*[
            OldTex("2^{%d}"%n, "=", "{:,}".format(2**n))
            for n in range(20)
        ])
        powers_of_2.to_edge(UP)
        max_height = 6
        center = MED_LARGE_BUFF*DOWN

        mob = Dot(color = BLUE)
        mob.move_to(center)
        vects = it.cycle(5*[UP] + 5*[RIGHT])
        curr_po2 = powers_of_2[0]

        for i, vect, po2 in zip(it.count(), vects, powers_of_2[1:]):
            if i == 10:
                rect = SurroundingRectangle(mob, color = GREEN)
                group = VGroup(mob, rect)
                two_to_ten = group.copy()
                group.generate_target()
                group.target.set_height(0.2)
                group.target[1].set_fill(BLUE, 1)

                self.play(ShowCreation(rect))
                self.play(MoveToTarget(group))
                self.remove(group)
                mob = rect
                self.add(mob)
            m1, m2 = mob.copy(), mob.copy()
            group = VGroup(m1, m2)
            group.arrange(
                vect, buff = SMALL_BUFF
            )
            if group.get_height() > max_height:
                group.set_height(max_height)
            group.move_to(center)
            pa = np.pi/3
            self.play(
                Transform(curr_po2, po2),
                ReplacementTransform(mob, m1, path_arc = pa),
                ReplacementTransform(mob.copy(), m2, path_arc = pa),
            )
            # CHANGE: Cairo iterated a mobject with points as [itself]+submobjects; GL iterates only the submobjects (a bare Rectangle gave an empty group)
            mob = VGroup(*it.chain(*[[m] if m.has_points() else m for m in (m1, m2)]))

        #Show two_to_ten for comparrison
        self.play(
            mob.space_out_submobjects, 1.1,
            mob.to_edge, RIGHT
        )
        two_to_ten.to_edge(LEFT)
        lines = VGroup(*[
            Line(
                two_to_ten.get_corner(vect+RIGHT),
                mob[0].get_corner(vect+LEFT),
            )
            for vect in (UP, DOWN)
        ])
        two_to_ten.save_state()
        two_to_ten.replace(mob[0])
        self.play(
            two_to_ten.restore,
            *list(map(ShowCreation, lines))
        )

        curr_po2_outline = curr_po2[-1].copy()
        curr_po2_outline.set_fill(opacity = 0)
        curr_po2_outline.set_stroke(width = 2)
        curr_po2_outline.set_color_by_gradient(
            YELLOW, RED, PINK, PURPLE, BLUE, GREEN
        )

        self.play(
            LaggedStartMap(
                FadeIn, curr_po2_outline,
                rate_func = lambda t : wiggle(t, 8),
                run_time = 2,
                lag_ratio = 0.75,
            ),
            *get_confetti_animations(50)
        )
