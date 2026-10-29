# ==============================================================================
# Scene:      MathematicalWebOfConnections
# Source:     videos/_2018/basel/basel2.py (lines 631-904)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MathematicalWebOfConnections.py MathematicalWebOfConnections -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
#   - random.sample needs a real sequence (Python 3.14); a VGroup is not one
# ==============================================================================

# CHANGE: import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class MathematicalWebOfConnections(PiCreatureScene):
    def construct(self):
        self.complain_that_pi_is_not_about_circles()
        self.show_other_pi_formulas()
        self.question_fundamental()
        self.draw_circle()
        self.remove_all_but_basel_sum()
        self.show_web_of_connections()
        self.show_light()

    def complain_that_pi_is_not_about_circles(self):
        jerk, randy = self.pi_creatures

        words = self.words = OldTexText(
            "I am not",
            "fundamentally \\\\", 
            "about circles"
        )
        words.set_color_by_tex("fundamentally", YELLOW)

        self.play(PiCreatureSays(
            jerk, words,
            target_mode = "angry"
        ))
        self.play(randy.change, "guilty")
        self.wait(2)

    def show_other_pi_formulas(self):
        jerk, randy = self.pi_creatures
        words = self.words

        basel_sum = OldTex(
            "1 + {1 \\over 4} + {1 \\over 9} + {1 \\over 16} + \\cdots", 
            "=", "{\\pi^2 \\over 6}"
        )
        leibniz_sum = OldTex(
            "1-{1\\over 3}+{1\\over 5}-{1\\over 7}+{1\\over 9}-\\cdots",
            "=", "{\\pi \\over 4}")

        wallis_product = OldTex(
            "{2\\over 1} \\cdot {2\\over 3} \\cdot {4\\over 3} \\cdot {4\\over 5}" +
             "\\cdot {6\\over 5} \\cdot {6\\over 7} \\cdots",
             "=", "{\\pi \\over 2}")

        basel_sum.move_to(randy)
        basel_sum.to_edge(UP)
        basel_equals = basel_sum.get_part_by_tex("=")

        formulas = VGroup(basel_sum, leibniz_sum, wallis_product)
        formulas.scale(0.75)
        formulas.arrange(DOWN, buff = MED_LARGE_BUFF)
        for formula in formulas:
            basel_equals_x = basel_equals.get_center()[0]
            formula_equals_x = formula.get_part_by_tex("=").get_center()[0]
            formula.shift((basel_equals_x - formula_equals_x)*RIGHT)

        formulas.to_corner(UP+RIGHT)
        formulas.shift(2*LEFT)
        self.formulas = formulas

        self.play(
            jerk.change, "sassy",
            randy.change, "raise_right_hand",
            FadeOut(jerk.bubble),
            words.next_to, jerk, UP,
            FadeIn(basel_sum, lag_ratio = 0.5, run_time = 3)
        )
        for formula in formulas[1:]:
            self.play(
                FadeIn(
                    formula, 
                    lag_ratio = 0.5, 
                    run_time = 3
                ),
            )
        self.wait()

    def question_fundamental(self):
        jerk, randy = self.pi_creatures
        words = self.words
        fundamentally = words.get_part_by_tex("fundamentally")
        words.remove(fundamentally)

        self.play(
            fundamentally.move_to, self.pi_creatures,
            fundamentally.shift, UP,
            FadeOut(words),
            jerk.change, "pondering",
            randy.change, "pondering",
        )
        self.wait()

        question = OldTexText("Does this mean \\\\ anything?")
        question.scale(0.8)
        question.set_stroke(WHITE, 0.5)
        question.next_to(fundamentally, DOWN, LARGE_BUFF)
        arrow = Arrow(question, fundamentally)
        arrow.set_color(WHITE)

        self.play(
            FadeIn(question),
            GrowArrow(arrow)
        )
        self.wait()

        fundamentally.add(question, arrow)
        self.fundamentally = fundamentally

    def draw_circle(self):
        semi_circle = Arc(angle = np.pi, radius = 2)
        radius = Line(ORIGIN, semi_circle.get_points()[0])
        radius.set_color(BLUE)
        semi_circle.set_color(YELLOW)

        VGroup(radius, semi_circle).move_to(
            FRAME_X_RADIUS*LEFT/2 + FRAME_Y_RADIUS*UP/2,
        )

        decimal = DecimalNumber(0)
        def decimal_position_update_func(decimal):
            decimal.move_to(semi_circle.get_points()[-1])
            decimal.shift(0.3*radius.get_vector())

        one = OldTex("1")
        one.next_to(radius, UP)

        self.play(ShowCreation(radius), FadeIn(one))
        self.play(
            Rotate(radius, np.pi, about_point = radius.get_start()),
            ShowCreation(semi_circle),
            ChangeDecimalToValue(
                decimal, np.pi, 
                position_update_func = decimal_position_update_func
            ),
            MaintainPositionRelativeTo(one, radius),
            run_time = 3,
        )
        self.wait(2)

        self.circle_group = VGroup(semi_circle, radius, one, decimal)

    def remove_all_but_basel_sum(self):
        to_shift_down = VGroup(
            self.circle_group, self.pi_creatures,
            self.fundamentally, self.formulas[1:],
        )
        to_shift_down.generate_target()
        for part in to_shift_down.target:
            part.move_to(FRAME_HEIGHT*DOWN)

        basel_sum = self.formulas[0]

        self.play(
            MoveToTarget(to_shift_down),
            basel_sum.scale, 1.5,
            basel_sum.move_to, 1.5*DOWN,
        )

        self.basel_sum = basel_sum

    def show_web_of_connections(self):
        self.remove(self.pi_creatures)
        title = OldTexText("Interconnected web of mathematics")
        title.to_edge(UP)
        basel_sum = self.basel_sum

        dots = VGroup(*[
            Dot(radius = 0.1).move_to(
                (j - 0.5*(i%2))*RIGHT + \
                (np.sqrt(3)/2.0)* i*DOWN + \
                0.5*(random.random()*RIGHT + random.random()*UP),
            )
            for i in range(4)
            for j in range(7+(i%2))
        ])
        dots.set_height(3)
        dots.next_to(title, DOWN, MED_LARGE_BUFF)
        edges = VGroup()
        for x in range(100):
            # CHANGE: random.sample needs a real sequence (Python 3.14); a VGroup is not one
            d1, d2 = random.sample(list(dots), 2)
            edge = Line(d1.get_center(), d2.get_center())
            edge.set_stroke(YELLOW, 0.5)
            edges.add(edge)

        ## Choose special path
        path_dots = VGroup(
            dots[-7],
            dots[-14],
            dots[9],
            dots[19],
            dots[14],
        )
        path_edges = VGroup(*[
            Line(
                d1.get_center(), d2.get_center(),
                color = RED
            )
            for d1, d2 in zip(path_dots, path_dots[1:])
        ])

        circle = Circle(color = YELLOW, radius = 1)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_color(BLUE)
        VGroup(circle, radius).next_to(path_dots[-1], RIGHT)

        self.play(
            Write(title),
            LaggedStartMap(ShowCreation, edges, run_time = 3),
            LaggedStartMap(GrowFromCenter, dots, run_time = 3)
        )
        self.play(path_dots[0].set_color, RED)
        for dot, edge in zip(path_dots[1:], path_edges):
            self.play(
                ShowCreation(edge),
                dot.set_color, RED
            )
        self.play(ShowCreation(radius))
        radius.set_points_as_corners(radius.get_anchors())
        self.play(
            ShowCreation(circle),
            Rotate(radius, angle = 0.999*TAU, about_point = radius.get_start()),
            run_time = 2
        )
        self.wait()

        graph = VGroup(dots, edges, path_edges, title)
        circle.add(radius)
        basel_sum.generate_target()
        basel_sum.target.to_edge(UP)

        arrow = Arrow(
            UP, DOWN, 
            rectangular_stem_width = 0.1,
            tip_length = 0.45,
            color = RED,
        )
        arrow.next_to(basel_sum.target, DOWN, buff = MED_LARGE_BUFF)

        self.play(
            MoveToTarget(basel_sum),
            graph.next_to, basel_sum.target, UP, LARGE_BUFF,
            circle.next_to, arrow, DOWN, MED_LARGE_BUFF,
        )
        self.play(GrowArrow(arrow))
        self.wait()

        self.arrow = arrow
        self.circle = circle

    def show_light(self):
        light = AmbientLight(
            num_levels = 500, radius = 13,
            opacity_function = lambda r : 1.0/(r+1),
        )
        pi = self.basel_sum[-1][0]
        pi.set_stroke(BLACK, 0.5)
        light.move_to(pi)
        self.play(
            SwitchOn(light, run_time = 3),
            Animation(self.arrow),
            Animation(self.circle),
            Animation(self.basel_sum),
        )
        self.wait()

    ###

    def create_pi_creatures(self):
        jerk = PiCreature(color = GREEN_D)
        randy = Randolph().flip()
        jerk.move_to(0.5*FRAME_X_RADIUS*LEFT).to_edge(DOWN)
        randy.move_to(0.5*FRAME_X_RADIUS*RIGHT).to_edge(DOWN)

        return VGroup(jerk, randy)
