# ==============================================================================
# Scene:      GuessSine
# Source:     videos/_2025/laplace/shm.py (lines 1398-1453)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GuessSine.py GuessSine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GuessSine(InteractiveScene):
    func_name = R"\sin"

    def construct(self):
        # Set up
        self.frame.set_height(9, about_edge=LEFT)
        func_name = self.func_name
        func_tex = Rf"{func_name}(\omega t)"

        t2c = {R"\omega": PINK, "x(t)": TEAL, "x''(t)": RED}
        equation = Tex(R"m x''(t) + k x(t) = 0", t2c=t2c)
        equation.to_edge(LEFT)
        guess_words = TexText(Rf"Try $x(t) = {func_tex}$", t2c=t2c, font_size=36)

        arrow = Arrow(guess_words.get_left(), guess_words.get_right(), buff=-0.1, thickness=6)
        arrow.next_to(equation, RIGHT)
        guess_words.next_to(arrow, UP, SMALL_BUFF)

        self.add(equation)
        self.add(arrow)
        self.add(guess_words)

        # Sub
        sub = Tex(fR"-m \omega^2 {func_tex}  + k {func_tex} = 0", t2c=t2c)
        sub.next_to(arrow, RIGHT)
        simple_sub = Tex(Rf"\left(-m \omega^2 + k\right) {func_tex} = 0", t2c=t2c)
        simple_sub.next_to(arrow, RIGHT)
        implies = Tex(R"\Rightarrow", font_size=72)
        implies.next_to(simple_sub, RIGHT)

        t2c[R"\ding{51}"] = GREEN
        t2c["Valid"] = GREEN
        result = TexText(R"\ding{51} Valid if $\omega = \sqrt{k / m}$", t2c=t2c, font_size=36)
        result.next_to(simple_sub, DOWN)

        simple_sub.shift(0.05 * UP)
        blank_sub = sub.copy()
        blank_sub[func_tex].set_opacity(0)
        func_parts = sub[func_tex]

        self.play(LaggedStart(
            TransformMatchingTex(equation.copy(), blank_sub, path_arc=30 * DEG, run_time=2),
            FadeTransform(guess_words[func_tex][0].copy(), func_parts[0]),
            FadeTransform(guess_words[func_tex][0].copy(), func_parts[1]),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(
            TransformMatchingTex(blank_sub, simple_sub),
            Transform(func_parts[0], simple_sub[func_tex][0], path_arc=-30 * DEG),
            Transform(func_parts[1], simple_sub[func_tex][0], path_arc=-30 * DEG),
            run_time=1
        )
        self.wait()
        self.play(FadeIn(result, 0.5 * UP))
        self.wait()
