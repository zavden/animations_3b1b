# ==============================================================================
# Scene:      GroverTimeline
# Source:     videos/_2025/grover/runtime.py (lines 802-958)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroverTimeline.py GroverTimeline -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GroverTimeline(InteractiveScene):
    def construct(self):
        # Test
        timeline = NumberLine(
            (1990, 2025, 1),
            big_tick_spacing=5,
            width=FRAME_WIDTH - 1
        )
        timeline.set_y(-2)
        timeline.add_numbers(
            range(1990, 2030, 5),
            group_with_commas=False,
            font_size=24,
        )
        self.add(timeline)

        # BBBV
        bbbv_statement = VGroup(
            Text("Quantum Search", font_size=36),
            Tex(R"\ge", font_size=42),
            Tex(R"\mathcal{O}(\sqrt{N})", font_size=36),
        )
        bbbv_statement.arrange(RIGHT, SMALL_BUFF)
        bbbv_statement.to_corner(UL)
        bbbv_statement.set_color(RED)

        bbbv_attribution = TexText("BBBV$^*$ Theorem (1994)", font_size=36)
        bbbv_attribution.next_to(bbbv_statement, DOWN, aligned_edge=LEFT)
        bbbv_attribution.set_color(RED_B)

        bbbv_attribution.to_corner(UL)
        bbbv_statement.next_to(bbbv_attribution, DOWN, MED_SMALL_BUFF)
        bbbv_statement.set_x(-3.5)

        footnote = Text("*Bennett, Bernstein, Brassard, Vazirani", font_size=24)
        footnote.set_color(GREY_C)
        footnote.to_corner(DL, buff=MED_SMALL_BUFF)

        bbbv_dots = VGroup(
            Dot(timeline.n2p(1994)),
            Dot().next_to(bbbv_attribution, LEFT, SMALL_BUFF),
        )
        bbbv_dots.set_color(RED_B)
        arc = -45 * DEG
        bbbv_line = Line(
            bbbv_dots[0].get_center(),
            bbbv_dots[1].get_center(),
            path_arc=arc,
        )
        bbbv_line.set_stroke(RED_B)

        self.play(
            GrowFromCenter(bbbv_dots[0]),
            TransformFromCopy(*bbbv_dots, path_arc=arc),
            ShowCreation(bbbv_line),
            FadeIn(bbbv_attribution, UP),
            FadeIn(footnote),
        )
        self.play(
            FadeIn(bbbv_statement, 0.5 * DOWN)
        )
        self.wait()

        # Lov Grover
        grover_name = TexText("Grover's Algorithm (1996)", font_size=36)
        grover_name.next_to(bbbv_statement, DOWN, buff=0.75)
        grover_name.set_color(BLUE)
        grover_name.shift(0.5 * LEFT)

        grover_statement = bbbv_statement.copy()
        eq = Tex(R"=").replace(grover_statement[1], dim_to_match=0)
        grover_statement[1].become(eq)
        grover_statement.set_color(BLUE_D)
        grover_statement.next_to(grover_name, DOWN)
        grover_statement.match_x(bbbv_statement)

        grover_dots = VGroup(
            Dot(timeline.n2p(1996)),
            Dot().next_to(grover_name, LEFT, SMALL_BUFF),
        )
        arc = -35 * DEG
        grover_line = Line(
            grover_dots[0].get_center(),
            grover_dots[1].get_center(),
            path_arc=arc,
        )
        VGroup(grover_dots, grover_line).set_color(BLUE_B)

        self.play(TransformFromCopy(bbbv_dots[0], grover_dots[0], path_arc=-PI))
        self.play(
            TransformFromCopy(*grover_dots, path_arc=arc),
            ShowCreation(grover_line),
            FadeIn(grover_name, UP),
        )
        self.wait()
        self.play(
            TransformFromCopy(bbbv_statement, grover_statement),
        )
        self.wait()

        # Show examples
        examples = VGroup()
        for n in [6, 12]:
            n_eq = VGroup(Tex(R"N = "), Integer(10**n))
            n_eq.arrange(RIGHT, SMALL_BUFF)
            n_eq.to_corner(UR, buff=MED_LARGE_BUFF)
            steps = VGroup(Tex(R"\sim"), Integer(10**(n / 2)), Dot().set_fill(opacity=0), Text("Steps"))
            steps.arrange(RIGHT, buff=0.05)
            steps.next_to(n_eq, DOWN, LARGE_BUFF)

            arrow = Arrow(n_eq, steps, buff=0.15)

            examples.add(VGroup(n_eq, arrow, steps))

        sqrt_N = grover_statement[2][2:4]

        for n, example in enumerate(examples):
            if n == 0:
                self.play(
                    CountInFrom(example[0][1], 0),
                    VFadeIn(example[0]),
                )
            elif n == 1:
                self.play(
                    ReplacementTransform(examples[0][0], examples[1][0]),
                    FadeOut(examples[0][1:])
                )
            sqrt_rect = SurroundingRectangle(sqrt_N, buff=SMALL_BUFF)
            sqrt_rect.set_stroke(WHITE, 2)
            self.play(ShowCreation(sqrt_rect))
            self.play(
                GrowArrow(example[1]),
                sqrt_rect.animate.surround(example[2][1]).set_stroke(opacity=0),
                FadeTransform(sqrt_N.copy(), example[2][1]),
                FadeIn(example[2][0]),
                FadeIn(example[2][-1]),
            )
            self.add(example)
            self.wait()

        # Show the π / 4
        big_O = grover_statement[2]
        runtime = Tex(R"\left\lceil \frac{\pi}{4} \right\rceil \sqrt{N}", font_size=36)
        runtime.move_to(big_O, LEFT)
        runtime.set_color(BLUE_B)

        rect = SurroundingRectangle(big_O)
        rect.set_stroke(WHITE, 2)

        self.play(ShowCreation(rect))
        self.wait()
        self.play(
            VGroup(rect, big_O).animate.shift(DOWN),
            FadeIn(runtime, scale=2)
        )
        self.wait()
        self.play(rect.animate.surround(runtime[1], buff=0.05))
