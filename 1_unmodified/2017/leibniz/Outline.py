# ==============================================================================
# Scene:      Outline
# Source:     videos/_2017/leibniz.py (lines 494-715)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Outline.py Outline -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def chi_func(n):
    if n%2 == 0:
        return 0
    if n%4 == 1:
        return 1
    else:
        return -1


class Outline(PiCreatureScene):
    def construct(self):
        self.generate_list()
        self.wonder_at_pi()
        self.count_lattice_points()
        self.write_steps_2_and_3()
        self.show_chi()
        self.show_complicated_formula()
        self.show_last_step()

    def generate_list(self):
        steps = VGroup(
            OldTexText("1. Count lattice points"),
            OldTex("2. \\text{ Things like }17 = ", "4", "^2 + ", "1", "^2"),
            OldTex("3. \\text{ Things like }17 = (", "4", " + ", "i", ")(", "4", " - ", "i", ")"),
            OldTexText("4. Introduce $\\chi$"),
            OldTexText("5. Shift perspective"),
        )
        for step in steps[1:3]:
            step.set_color_by_tex("1", RED, substring = False)
            step.set_color_by_tex("i", RED, substring = False)
            step.set_color_by_tex("4", GREEN, substring = False)
        steps.arrange(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        steps.to_corner(UP+LEFT)

        self.steps = steps

    def wonder_at_pi(self):
        question = OldTex("\\pi", "=???")
        pi = question.get_part_by_tex("pi")
        pi.scale(2, about_point = pi.get_right())
        pi.set_color(YELLOW)
        question.next_to(self.pi_creature.body, LEFT, aligned_edge = UP)
        self.think(
            "Who am I really?",
            look_at = question,
            added_anims = [
                FadeIn(question)
            ]
        )
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(self.pi_creature),
            question.to_corner, UP+RIGHT
        )

        self.question = question
        self.pi = question.get_part_by_tex("pi")

    def count_lattice_points(self):
        step = self.steps[0]
        plane = NumberPlane(
            x_radius = 10, y_radius = 10,
            secondary_line_ratio = 0,
            color = BLUE_E,
        )
        plane.set_height(6)
        plane.next_to(step, DOWN)
        plane.to_edge(LEFT)
        circle = Circle(
            color = YELLOW,
            radius = get_norm(
                plane.coords_to_point(10, 0) - \
                plane.coords_to_point(0, 0)
            )
        )
        plane_center = plane.coords_to_point(0, 0)
        circle.move_to(plane_center)
        lattice_points = VGroup(*[
            Dot(
                plane.coords_to_point(a, b), 
                radius = 0.05,
                color = PINK,
            )
            for a in range(-10, 11)
            for b in range(-10, 11)
            if a**2 + b**2 <= 10**2
        ])
        lattice_points.sort(
            lambda p : get_norm(p - plane_center)
        )
        lattice_group = VGroup(plane, circle, lattice_points)

        self.play(ShowCreation(circle))
        self.play(Write(plane, run_time = 2), Animation(circle))
        self.play(
            *[
                DrawBorderThenFill(
                    dot,
                    stroke_width = 4,
                    stroke_color = YELLOW,
                    run_time = 4,
                    rate_func = squish_rate_func(
                        double_smooth, a, a + 0.25
                    )
                )
                for dot, a in zip(
                    lattice_points, 
                    np.linspace(0, 0.75, len(lattice_points))
                )
            ]
        )
        self.play(
            FadeIn(step)
        )
        self.wait()
        self.play(
            lattice_group.set_height, 2.5,
            lattice_group.next_to, self.question, DOWN,
            lattice_group.to_edge, RIGHT
        )

    def write_steps_2_and_3(self):
        for step in self.steps[1:3]:
            self.play(FadeIn(step))
            self.wait(2)
        self.wait()

    def show_chi(self):
        input_range = list(range(1, 7))
        chis = VGroup(*[
            OldTex("\\chi(%d)"%n)
            for n in input_range
        ])
        chis.arrange(RIGHT, buff = LARGE_BUFF)
        chis.set_stroke(WHITE, width = 1)
        numerators = VGroup()
        arrows = VGroup()
        for chi, n in zip(chis, input_range):
            arrow = OldTex("\\Downarrow")
            arrow.next_to(chi, DOWN, SMALL_BUFF)
            arrows.add(arrow)
            value = OldTex(str(chi_func(n)))
            value.set_color_by_tex("1", BLUE)
            value.set_color_by_tex("-1", GREEN)
            value.next_to(arrow, DOWN)
            numerators.add(value)
        group = VGroup(chis, arrows, numerators)
        group.set_width(1.3*FRAME_X_RADIUS)
        group.to_corner(DOWN+LEFT)

        self.play(FadeIn(self.steps[3]))
        self.play(*[
            FadeIn(
                mob, 
                run_time = 3,
                lag_ratio = 0.5
            )
            for mob in [chis, arrows, numerators]
        ])
        self.change_mode("pondering")
        self.wait()

        self.chis = chis
        self.arrows = arrows
        self.numerators = numerators

    def show_complicated_formula(self):
        rhs = OldTex(
            " = \\lim_{N \\to \\infty}",
            " \\frac{4}{N}",
            "\\sum_{n = 1}^N",
            "\\sum_{d | n} \\chi(d)",
        )
        pi = self.pi 
        self.add(pi.copy())
        pi.generate_target()
        pi.target.next_to(self.steps[3], RIGHT, MED_LARGE_BUFF)
        pi.target.shift(MED_LARGE_BUFF*DOWN)
        rhs.next_to(pi.target, RIGHT)

        self.play(
            MoveToTarget(pi),
            Write(rhs)
        )
        self.change_mode("confused")
        self.wait(2)

        self.complicated_formula = rhs

    def show_last_step(self):
        expression = OldTex(
            "=", "\\frac{\\quad}{1}",
            *it.chain(*[
                ["+", "\\frac{\\quad}{%d}"%d]
                for d in range(2, len(self.numerators)+1)
            ] + [["+ \\cdots"]])
        )
        over_four = OldTex("\\quad \\over 4")
        over_four.to_corner(DOWN+LEFT)
        over_four.shift(UP)
        pi = self.pi
        pi.generate_target()
        pi.target.scale(0.75)
        pi.target.next_to(over_four, UP)
        expression.next_to(over_four, RIGHT, align_using_submobjects = True)
        self.numerators.generate_target()
        for num, denom in zip(self.numerators.target, expression[1::2]):
            num.scale(1.2)
            num.next_to(denom, UP, MED_SMALL_BUFF)

        self.play(
            MoveToTarget(self.numerators),
            MoveToTarget(pi),
            Write(over_four),
            FadeOut(self.chis),
            FadeOut(self.arrows),
            FadeOut(self.complicated_formula),
        )
        self.play(
            Write(expression),
            self.pi_creature.change_mode, "pondering"
        )
        self.wait(3)

    ########
    def create_pi_creature(self):
        return Randolph(color = BLUE_C).flip().to_corner(DOWN+RIGHT)
