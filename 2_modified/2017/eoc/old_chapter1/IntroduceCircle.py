# ==============================================================================
# Scene:      IntroduceCircle
# Source:     videos/_2017/eoc/old_chapter1.py (lines 359-447)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceCircle.py IntroduceCircle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
# ==============================================================================

from manim_imports_ext import *

class IntroduceCircle(Scene):
    def construct(self):
        circle = Circle(radius = 3, color = WHITE)
        circle.to_edge(LEFT)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_color(MAROON_B)
        R = OldTex("R").next_to(radius, UP)

        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
        area, circumference = words = VGroup(*list(map(OldTexText, [
            "Area =", "Circumference ="
        ])))
        area.set_color(BLUE)
        circumference.set_color(YELLOW)

        words.arrange(DOWN, aligned_edge = LEFT)
        words.next_to(circle, RIGHT)
        words.to_edge(UP)
        pi_R, pre_squared = OldTex("\\pi R", "{}^2")
        squared = OldTex("2").replace(pre_squared)
        area_form = VGroup(pi_R, squared)
        area_form.next_to(area, RIGHT)
        two, pi_R = OldTex("2", "\\pi R")
        circum_form = VGroup(pi_R, two)
        circum_form.next_to(circumference, RIGHT)

        derivative = OldTex(
            "\\frac{d}{dR}", "\\pi R^2", "=", "2\\pi R"
        )
        integral = OldTex(
            "\\int_0^R", "2\\pi r", "\\, dR = ", "\\pi R^2"
        )
        up_down_arrow = OldTex("\\Updownarrow")
        calc_stuffs = VGroup(derivative, up_down_arrow, integral)
        calc_stuffs.arrange(DOWN)
        calc_stuffs.next_to(words, DOWN, buff = LARGE_BUFF, aligned_edge = LEFT)

        brace = Brace(calc_stuffs, RIGHT)
        to_be_explained = brace.get_text("To be \\\\ explained")
        VGroup(brace, to_be_explained).set_color(GREEN)

        self.play(ShowCreation(radius), Write(R))
        self.play(
            Rotate(radius, 2*np.pi, about_point = circle.get_center()),
            ShowCreation(circle)
        )
        self.play(
            FadeIn(area),
            Write(area_form),
            circle.set_fill, area.get_color(), 0.5,
            Animation(radius),
            Animation(R),
        )
        self.wait()
        self.play(
            circle.set_stroke, circumference.get_color(),
            FadeIn(circumference),
            Animation(radius),
            Animation(R),
        )
        self.play(Transform(
            area_form.copy(),
            circum_form,
            path_arc = -np.pi/2,
            run_time = 3
        ))
        self.wait()
        self.play(
            area_form.copy().replace, derivative[1],
            circum_form.copy().replace, derivative[3],
            Write(derivative[0]),
            Write(derivative[2]),
            run_time = 1
        )
        self.wait()
        self.play(
            area_form.copy().replace, integral[3],
            Transform(circum_form.copy(), integral[1]),
            Write(integral[0]),
            Write(integral[2]),
            run_time = 1
        )
        self.wait()
        self.play(Write(up_down_arrow))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(to_be_explained)
        )
        self.wait()
