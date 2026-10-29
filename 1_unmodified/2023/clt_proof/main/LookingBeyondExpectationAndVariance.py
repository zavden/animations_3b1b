# ==============================================================================
# Scene:      LookingBeyondExpectationAndVariance
# Source:     videos/_2023/clt_proof/main.py (lines 121-315)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookingBeyondExpectationAndVariance.py LookingBeyondExpectationAndVariance -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.integrate as integrate

class LookingBeyondExpectationAndVariance(InteractiveScene):
    def construct(self):
        # Only E[X] and Var(X) matter
        kw = dict(t2c={
            R"\mu": PINK,
            R"\sigma": RED,
            R"\mathds{E}[X]": PINK,
            R"\text{Var}(X)": RED,
        })
        top_words1 = TexText(R"Only $\mu$ and $\sigma$ matter", **kw)
        top_words2 = TexText(R"Only $\mathds{E}[X]$ and $\text{Var}(X)$ matter", **kw)
        for words in [top_words1, top_words2]:
            words.to_edge(UP)
            words.set_backstroke(width=2)

        self.play(Write(top_words1, run_time=1))
        self.wait()
        self.remove(top_words1)
        self.play(LaggedStart(*(
            ReplacementTransform(
                top_words1[t1][0], top_words2[t2][0],
            )
            for t1, t2 in [
                ("Only", "Only"),
                (R"$\mu$", R"$\mathds{E}[X]$"),
                ("and", "and"),
                (R"$\sigma$", R"$\text{Var}(X)$"),
                ("matter", "matter"),
            ]
        )))
        self.wait()

        # Add distribution
        axes = Axes((-4, 4), (0, 0.75, 0.25), width=10, height=3)
        axes.to_edge(DOWN)

        def func(x):
            return (np.exp(-(x - 1)**2) + 0.5 * np.exp(-(x + 1)**2)) / 2.66

        graph = axes.get_graph(func)
        graph.set_stroke(TEAL, 3)
        mu = integrate.quad(lambda x: x * func(x), -4, 4)[0]
        mu_line = Line(axes.c2p(mu, 0), axes.c2p(mu, 0.5))
        mu_line.set_stroke(PINK, 2)
        exp_label = Tex(R"\mathds{E}[X]", font_size=30)
        exp_label.next_to(mu_line, UP, SMALL_BUFF)
        exp_label.set_color(PINK)
        sigma_arrows = VGroup(Vector(LEFT), Vector(RIGHT))
        sigma_arrows.arrange(RIGHT)
        sigma_arrows.move_to(mu_line.pfp(0.2))
        sigma_arrows.set_color(RED)

        plot = VGroup(axes, graph, mu_line, exp_label, sigma_arrows)

        self.play(LaggedStartMap(Write, plot))
        self.wait()

        # What else is there
        moment_list = Tex(R"""
            \mathds{E}\left[X\right],\quad
            \mathds{E}\left[X^2\right],\quad
            \mathds{E}\left[X^3\right],\quad
            \mathds{E}\left[X^4\right],\quad
            \mathds{E}\left[X^5\right],\quad
            \dots
        """)
        moment_list.next_to(top_words2, DOWN, LARGE_BUFF)
        moments = moment_list[re.compile(r"\\mathds{E}\\left\[X.*\\right\]")]
        commas = moment_list[","]

        commas.shift(SMALL_BUFF * RIGHT)
        moments[1:].shift(SMALL_BUFF * LEFT)
        for moment in moments:
            y = moment[0].get_y()
            moment[0].next_to(moment[1], LEFT, SMALL_BUFF)
            moment[0].set_y(y)

        moment_boxes = VGroup(*(
            SurroundingRectangle(moment, buff=0.05)
            for moment in moments
        ))
        moment_boxes.set_stroke(TEAL, 2)
        moment_boxes.set_fill(GREY_E, 1)
        var_sub = Tex(R"\text{Var}(X)")
        var_sub.move_to(commas[:2]).align_to(moments[0], DOWN)

        question = Text("What else is there?")
        question.next_to(moment_boxes[2:], DOWN)

        self.play(LaggedStart(
            TransformFromCopy(top_words2[R"\mathds{E}[X]"][0], moments[0]),
            Write(commas[0]),
            TransformFromCopy(top_words2[R"\text{Var}(X)"][0], var_sub),
            Write(commas[1]),
            lag_ratio=0.5,
        ))
        self.play(
            LaggedStartMap(FadeIn, moment_boxes[2:]),
            LaggedStartMap(FadeIn, commas[2:]),
            Write(question)
        )
        self.play(Write(moment_list[R"\dots"][0]))
        self.wait()

        # Expand variance
        var_equation = Tex(R"\text{Var}(X) = \mathds{E}[X^2] - \mathds{E}[X]^2")
        full_var_equation = Tex(R"""
            \text{Var}(X)
            &= \mathds{E}[(X - \mu)^2] \\
            &= \mathds{E}[X^2 - 2\mu X + \mu^2] \\
            &= \mathds{E}[X^2] - 2 \mu \mathds{E}[X] + \mu^2] \\
            &= \mathds{E}[X^2] - \mathds{E}[X]^2 \\
        """, font_size=32, t2c={R"\mu": PINK})
        var_equation.to_edge(UP)
        full_var_equation.to_corner(DL)
        full_var_equation.shift(UP)
        full_var_equation.set_fill(GREY_A)
        second_moment = var_equation[R"\mathds{E}[X^2]"][0]
        second_moment_rect = SurroundingRectangle(second_moment)

        self.play(
            TransformFromCopy(var_sub, var_equation[:len(var_sub)]),
            FadeIn(var_equation[len(var_sub):], UP),
            FadeOut(top_words2, UP),
        )
        self.wait()
        self.play(FadeIn(full_var_equation))
        self.wait()
        self.play(
            ShowCreation(second_moment_rect),
            FlashAround(second_moment, run_time=1.5)
        )
        self.play(
            TransformFromCopy(second_moment, moments[1]),
            FadeOut(var_sub, DOWN),
        )
        self.wait()
        self.play(
            FadeOut(second_moment_rect),
            var_equation.animate.scale(0.7).to_corner(UL),
            FadeOut(full_var_equation, DOWN)
        )

        # Show the moments
        self.add(moment_list, moment_boxes[2:])
        for box in moment_boxes[2:]:
            self.play(
                FadeOut(box, UP),
                question.animate.set_opacity(0),
            )
        self.remove(question)
        self.wait()

        # Name the moments
        moment_name = TexText("Moments of $X$")
        moment_name.to_edge(UP, buff=MED_SMALL_BUFF)
        moment_name.match_x(moments)
        moment_name.set_color(BLUE)
        points = np.linspace(moment_name.get_corner(DL), moment_name.get_corner(DR), len(moments))
        arrows = VGroup(*(
            Arrow(point, moment.get_top() + 0.1 * UP)
            for point, moment in zip(points, moments)
        ))
        arrows.set_color(BLUE)

        self.play(
            FadeIn(moment_name, UP),
            FadeOut(var_equation, UL),
        )
        self.play(LaggedStartMap(GrowArrow, arrows))
        self.wait()

        # Hypothesis
        rect = SurroundingRectangle(VGroup(moments[2], moment_list[R"\dots"]))
        rect.set_stroke(RED, 3)
        hyp = TexText(R"""
            Hypothesis: These have no \\
            influence on $X_1 + \cdots + X_n$
        """, font_size=42)
        hyp["Hypothesis"].set_color(RED)
        hyp.next_to(rect, DOWN).shift(LEFT)
        correction = Text("diminishing", font_size=42)
        correction.set_color(YELLOW)
        correction.next_to(hyp["no"], RIGHT)
        cross = Cross(hyp["no"])
        cross.scale(1.5)

        self.play(
            ShowCreation(rect),
            Write(hyp),
        )
        self.wait()
        self.play(ShowCreation(cross))
        self.play(Write(correction))
        self.wait()
