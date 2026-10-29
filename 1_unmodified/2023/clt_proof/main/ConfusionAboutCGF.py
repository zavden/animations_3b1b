# ==============================================================================
# Scene:      ConfusionAboutCGF
# Source:     videos/_2023/clt_proof/main.py (lines 1051-1177)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusionAboutCGF.py ConfusionAboutCGF -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConfusionAboutCGF(TeacherStudentsScene):
    def construct(self):
        # Setup
        morty = self.teacher
        stds = self.students
        kw = dict(t2c={
            "t": PINK,
            R"\frac{t^2}{2}": PINK,
            R"\frac{t^3}{6}": PINK,
            R"\frac{t^m}{m!}": PINK,
            R"\log": BLUE_B
        })
        equation = Tex(
            R"""
            K_X(t)
            = \log\left(\mathds{E}[e^{tX}]\right)
            = \sum_{m=1}^\infty K_m[X] \frac{t^m}{m!}
            """,
            **kw
        )
        equation.next_to(morty.get_corner(UL), UP)
        equation.shift_onto_screen()

        # React
        self.play(
            morty.change("raise_right_hand"),
            FadeIn(equation, UP),
            self.change_students("confused", "maybe", "confused", look_at=equation),
        )
        self.wait(3)

        # Another way...
        equation.generate_target()
        equation.target.scale(0.7)
        equation.target.to_corner(UR)
        eq_rect = SurroundingRectangle(equation.target)

        words = Text("Another language to\ndescribe distributions")
        words.move_to(self.hold_up_spot, DOWN)
        arrow = Arrow(words, eq_rect, stroke_color=YELLOW)

        self.play(
            morty.change("tease"),
            MoveToTarget(equation),
            self.change_students("hesitant", "sassy", "erm", look_at=words)
        )
        self.play(
            Write(words),
            ShowCreation(arrow),
        )
        self.wait(3)

        # Back and forth
        words.generate_target()
        words.target.scale(0.7)
        words.target.next_to(equation, LEFT, buff=1.5)
        words.target.shift_onto_screen()
        arrow.target = Arrow(words.target, equation, stroke_color=YELLOW)

        self.play(
            morty.says("I'm thinking of\na distribution", run_time=1),
            MoveToTarget(words),
            MoveToTarget(arrow),
        )
        self.wait()
        self.play(
            stds[0].says("Oh cool, what\nis it?", mode="coin_flip_2", run_time=1),
            stds[1].change("happy"),
            stds[1].change("tease"),
        )
        self.wait()

        # Show pdf
        axes = Axes((0, 10), (0, 0.3), width=4, height=1.25)
        axes.move_to(self.hold_up_spot, DOWN)
        graph = axes.get_graph(lambda x: np.exp(-x) * x**3 / 6)
        graph.set_stroke(YELLOW, 2)

        label = Tex(R"p_X(x) = e^{-x} x^3 / 6", font_size=36)
        label.move_to(axes, UL)
        label.shift(0.5 * UP)

        plot = VGroup(axes, graph, label)

        self.play(
            morty.debubble(mode="raise_right_hand"),
            FadeIn(plot, UP),
        )
        self.wait()

        # Show CGF
        cgf = Tex(R"""
            K_{X}(t) = 4t + 4 \frac{t^2}{2} + 8 \frac{t^3}{6} + \cdots
            """,
            **kw
        )
        cgf.move_to(self.hold_up_spot, DOWN)

        self.play(
            morty.change("tease"),
            stds[0].change("sassy"),
            stds[1].change("hesitant"),
            plot.animate.set_width(2).to_corner(UL),
            FadeIn(cgf, UP),
        )
        self.wait(2)

        # Term by term
        words = VGroup(Text("Expected value"), Text("Variance"))
        coefs = cgf["4"]
        arrows = VGroup(*(Vector(0.5 * DOWN).next_to(coef, UP) for coef in coefs))
        arrows.set_color(YELLOW)
        words.set_color(YELLOW)

        for word, arrow in zip(words, arrows):
            word.next_to(arrow, UP, SMALL_BUFF)

        self.play(
            FadeIn(words[0]),
            FadeIn(arrows[0]),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(*words),
            ReplacementTransform(*arrows),
        )
        self.wait(5)
