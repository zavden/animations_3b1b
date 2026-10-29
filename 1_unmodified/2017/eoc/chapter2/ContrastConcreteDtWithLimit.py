# ==============================================================================
# Scene:      ContrastConcreteDtWithLimit
# Source:     videos/_2017/eoc/chapter2.py (lines 1981-2041)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastConcreteDtWithLimit.py ContrastConcreteDtWithLimit -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

TIME_COLOR = YELLOW


class ContrastConcreteDtWithLimit(Scene):
    def construct(self):
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        self.add(v_line)

        l_title = OldTexText("""
            If $dt$ has a
            specific size.
        """)
        VGroup(*l_title[2:4]).set_color(TIME_COLOR)
        r_title = OldTex("dt \\to 0")
        VGroup(*r_title[:2]).set_color(TIME_COLOR)
        for title, vect in (l_title, LEFT), (r_title, RIGHT):
            title.to_edge(UP)
            title.shift(FRAME_X_RADIUS*vect/2)
            self.add(title)

        l_formula = OldTex("""
            \\frac{d(t^3)}{dt} = 
            \\frac{
                t^3+
                3t^2 \\, dt + 
                3t \\, (dt)^2 + 
                (dt)^3
                - t^3
            }{dt}
        """)
        VGroup(*it.chain(
            l_formula[6:8],
            l_formula[15:17],
            l_formula[21:23],
            l_formula[27:29],
            l_formula[35:37],
        )).set_color(TIME_COLOR)
        l_formula.set_width(FRAME_X_RADIUS-MED_LARGE_BUFF)
        l_formula.to_edge(LEFT)

        l_brace = Brace(l_formula, DOWN)
        l_text = l_brace.get_text("Messy")
        l_text.set_color(RED)

        r_formula = OldTex(
            "\\frac{d(t^3)}{dt} = 3t^2"
        )
        VGroup(*r_formula[6:8]).set_color(TIME_COLOR)
        r_formula.shift(FRAME_X_RADIUS*RIGHT/2)
        r_brace = Brace(r_formula, DOWN)
        r_text = r_brace.get_text("Simple")
        r_text.set_color(GREEN)

        triplets = [
            (l_formula, l_brace, l_text),
            (r_formula, r_brace, r_text),
        ]
        for formula, brace, text in triplets:
            self.play(Write(formula, run_time = 1))
            self.play(
                GrowFromCenter(brace),
                Write(text)
            )
            self.wait(2)
