# ==============================================================================
# Scene:      ExperienceProblemSolver
# Source:     videos/_2018/eop/combinations.py (lines 83-196)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExperienceProblemSolver.py ExperienceProblemSolver -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PascalsTriangle(VGroup):
    CONFIG = {
        "n_rows" : 9,
        "distance" : 0.8,
        "max_width_to_distance_ratio" : 0.7,
        "angle" : 0.2*np.pi,
    }
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)

        distance = self.distance
        angle = self.angle
        max_width = self.max_width_to_distance_ratio * distance
        t_down = rotate_vector(distance*DOWN, -angle)
        t_right = 2*distance*np.sin(angle)*RIGHT

        for n in range(self.n_rows):
            row = VGroup()
            for k in range(n+1):
                num = OldTex(str(choose(n, k)))
                num.shift(n*t_down + k*t_right)
                row.add(num)
            self.add(row)
        self.center()


class ExperienceProblemSolver(PiCreatureScene):
    def construct(self):
        self.add_equation()
        self.jenny_solves()
        self.no_genius()
        self.think_about_patterns()

    def add_equation(self):
        equation = OldTex(
            "\\frac{x^3 + y^3}{(x+y)^2} + \\frac{3xy}{x+y}"
        )
        equation.to_edge(UP)

        self.play(Write(equation))
        self.wait()

        self.equation = equation

    def jenny_solves(self):
        randy, jenny = self.randy, self.jenny
        jenny_words = OldTexText("It's just $x+y$")
        randy_words = OldTexText("...wait...")
        randy_words.next_to(randy.get_corner(UP+RIGHT), RIGHT)

        self.pi_creature_says(
            jenny, jenny_words, 
            target_mode = "hooray",
            bubble_config = {"height" : 2, "width" : 3}
        )
        self.wait()
        self.play(
            randy.change, "confused", self.equation,
            Write(randy_words)
        )
        self.play(randy.look_at, self.equation.get_left())
        self.play(randy.look_at, jenny.eyes)
        self.play(jenny.change, "happy")
        self.play(randy.change, "tired")
        self.wait()
        self.play(*list(map(FadeOut, [
            jenny.bubble, jenny_words, randy_words
        ])))

    def no_genius(self):
        randy, jenny = self.randy, self.jenny

        lightbulb = Lightbulb()
        lightbulb.next_to(jenny, UP)
        cross = Cross(lightbulb)
        cross.set_stroke(RED, 8)

        self.play(LaggedStartMap(ShowCreation, lightbulb))
        self.play(
            ShowCreation(cross),
            jenny.change, "sassy", cross,
            randy.change, "happy"
        )
        self.wait(2)

        self.to_fade = VGroup(lightbulb, cross)

    def think_about_patterns(self):
        randy, jenny = self.randy, self.jenny
        rows = PascalsTriangle(
            n_rows = 6,
            distance = 0.6,
        )
        rows.scale(0.8)
        for row in rows:
            for num in row:
                n = float(num.get_tex())
                num.set_color(interpolate_color(
                    BLUE, YELLOW, n/10.0
                ))

        self.pi_creature_thinks(
            jenny, "",
            bubble_config = {"width" : 5, "height" : 4.2},
            added_anims = [
                FadeOut(self.to_fade),
                FadeOut(self.equation),
                randy.change, "plain"
            ]
        )
        rows.move_to(
            jenny.bubble.get_bubble_center() + \
            MED_SMALL_BUFF*(UP+LEFT)
        )
        self.play(FadeIn(rows[0]))
        for last_row, curr_row in zip(rows, rows[1:]):
            self.play(*[
                Transform(
                    last_row.copy(), VGroup(*mobs),
                    remover = True
                )
                for mobs in (curr_row[1:], curr_row[:-1])
            ])
            self.add(curr_row)
        self.wait(3)




    ############

    def create_pi_creatures(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        randy.shift(4*LEFT)
        jenny = PiCreature(color = BLUE_C).flip()
        jenny.to_edge(DOWN)
        jenny.shift(4*RIGHT)
        self.randy, self.jenny = randy, jenny
        return randy, jenny
