# ==============================================================================
# Scene:      JingleAnimation
# Source:     videos/_2021/quick_eigen.py (lines 1353-1420)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JingleAnimation.py JingleAnimation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


class JingleAnimation(Scene):
    def construct(self):
        form = OldTex("m \\pm \\sqrt{m^2 - p}")[0]
        form.set_height(2)
        m, old_pm, sqrt, root, m2, squared, minus, p = form
        VGroup(m, m2).set_color(MEAN_COLOR)
        VGroup(p).set_color(PROD_COLOR)
        m.refresh_bounding_box()  # Why?
        p.refresh_bounding_box()  # Why?

        pm = VGroup(OldTex("+"), OldTex("-"))
        pm.arrange(DOWN, buff=0)
        pm.replace(old_pm)
        pm.save_state()
        pm.scale(1.5)
        pm.arrange(DOWN, buff=2)

        mean = Text("mean", color=WHITE).next_to(m, DOWN)
        product = Text("product", color=WHITE).next_to(p, DOWN)
        plus_word = Text("plus", color=YELLOW).next_to(pm, UP)
        minus_word = Text("minus", color=YELLOW).next_to(pm, DOWN)

        def snap(t):
            return t**5

        self.play(FadeIn(m, scale=0.5, rate_func=snap, run_time=0.5))
        self.add(mean)
        self.wait(0.4)
        self.add(pm[0], plus_word)
        self.wait(0.2)
        self.add(pm[1], minus_word)
        self.wait(0.2)
        self.play(
            Restore(pm, rate_func=smooth, run_time=0.5),
            FadeOut(VGroup(plus_word, minus_word, mean), run_time=0.5),
        )

        sqrt_outline = sqrt.copy()
        sqrt_outline.set_stroke(YELLOW, 10)
        sqrt_outline.set_fill(opacity=0)
        sqrt_outline.insert_n_curves(100)
        root.save_state()
        root.stretch(0, 0, about_edge=LEFT)
        self.play(
            FadeIn(sqrt, rate_func=squish_rate_func(smooth, 0.25, 0.75)),
            VShowPassingFlash(sqrt_outline, time_width=2),
            Restore(root, rate_func=squish_rate_func(snap, 0.25, 1)),
            run_time=1,
        )
        self.play(
            TransformFromCopy(m, m2, path_arc=-120 * DEGREES, rate_func=smooth, run_time=0.6),
        )
        self.play(FadeTransform(m2.copy(), squared, run_time=0.5))
        minus.save_state()
        minus.stretch(0, 0, about_edge=LEFT)
        self.play(Restore(minus), run_time=0.5, rate_func=smooth)
        self.wait(0.2)
        self.play(
            FadeIn(p, scale=0.5, rate_func=snap, run_time=0.5),
        )
        self.add(product)
        self.wait(0.4)
        self.play(
            Flash(p, flash_radius=0.8 * p.get_height(), run_time=0.5),
        )
        self.wait(0.3)
        self.remove(product)
        self.wait()
