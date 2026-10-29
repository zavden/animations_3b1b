# ==============================================================================
# Scene:      WhatAboutANegativeResult
# Source:     videos/_2020/med_test.py (lines 4544-4655)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAboutANegativeResult.py WhatAboutANegativeResult -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_covid_clipboard(disease_name="SARS\\\\CoV-2", sign="+", report="Detected", color=GREEN):
    clipboard = SVGMobject("clipboard")
    clipboard.set_stroke(width=0)
    clipboard.set_fill(interpolate_color(GREY_BROWN, WHITE, 0.5), 1)
    clipboard.set_width(2.5)

    result = OldTexText(
        sign + "\\\\",
        disease_name + "\\\\",
        report,
    )
    result[0].scale(1.5, about_point=result[1].get_top())
    result[0].set_fill(color)
    result[0].set_stroke(color, 2)
    result[2].set_width(1.2 * result[1].get_width())
    result[-1].set_fill(color)
    result.set_width(clipboard.get_width() * 0.7)
    result.move_to(clipboard)
    result.shift(0.2 * DOWN)
    clipboard.add(result)
    return clipboard


class WhatAboutANegativeResult(Scene):
    def construct(self):
        # Test results
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.set_stroke(GREY_B, 2)

        randys = VGroup(Randolph(), Randolph())
        randys.set_height(2)
        clipboards = VGroup(
            get_covid_clipboard("Cancer", "+", "Detected", GREEN),
            get_covid_clipboard("Cancer", "$-$", "Not Detected", RED),
        )

        for randy, clipboard, y in zip(randys, clipboards, [2, -2]):
            randy.set_y(y)
            randy.to_edge(LEFT)
            clipboard.match_height(randy)
            clipboard.next_to(randy, RIGHT)

        self.add(randys, h_line)
        self.play(
            FadeIn(clipboards[0], LEFT),
            randys[0].change, "horrified", clipboards[0],
            randys[1].change, "guilty", clipboards[0],
        )
        self.play(Blink(randys[0]))
        self.play(
            FadeIn(clipboards[1], LEFT),
            randys[1].change, "hooray", clipboards[1]
        )
        self.play(Blink(randys[1]))
        self.wait()

        # Formulas
        t2c = {
            "+": GREEN,
            "-": RED,
            "=": WHITE,
            "\\approx": WHITE,
            "\\over": WHITE,
            "\\text{Cancer}": YELLOW,
            "\\text{No cancer}": GREY_B,
            "90\\%": GREEN,
            "9\\%": GREEN_D,
            "10\\%": RED_D,
            "91\\%": RED,
        }
        equations = VGroup(
            OldTex(
                "={P(+ \\,|\\, \\text{Cancer}) \\over P(+ \\,|\\, \\text{No cancer})}",
                "={90\\% \\over 9\\%} = 10",
                tex_to_color_map=t2c,
            ),
            OldTex(
                "={P(- \\,|\\, \\text{Cancer}) \\over P(- \\,|\\, \\text{No cancer})}",
                "={10\\% \\over 91\\%} \\approx {1 \\over 9}",
                tex_to_color_map=t2c,
            ),
        )

        for equation, clipboard in zip(equations, clipboards):
            bf = OldTexText("Bayes\\\\Factor")
            bf.next_to(equation, LEFT)
            equation.add_to_back(bf)
            equation.next_to(clipboard, RIGHT, MED_LARGE_BUFF)

        self.play(
            *(
                FadeIn(equation, lag_ratio=0.1, run_time=2)
                for equation in equations
            ),
            randys[0].change, "pondering", equations[0],
            randys[1].change, "thinking", equations[0],
        )
        self.wait()

        # Highlight parts
        eq = equations[1]
        frac_parts = VGroup(eq[2:7], eq[8:13])
        rects = VGroup(*(
            SurroundingRectangle(part, buff=0.1, stroke_color=TEAL, stroke_width=3)
            for part in frac_parts
        ))

        self.play(ShowCreationThenFadeOut(rects[0]))
        self.wait()
        self.play(ShowCreationThenFadeOut(rects[1]))
        self.wait()

        fnr = eq.get_part_by_tex("10\\%")
        fnr_word = OldTexText("FNR", font_size=36)
        fnr_word.next_to(fnr, UP, buff=0.8)
        fnr_arrow = Arrow(fnr_word.get_bottom(), fnr.get_top(), buff=0.1)

        spec = eq.get_part_by_tex("91\\%")
        spec_word = OldTexText("Specificity", font_size=36)
        spec_word.next_to(spec, DOWN, buff=0.8)
        spec_arrow = Arrow(spec_word.get_top(), spec.get_bottom(), buff=0.1)

        self.play(
            FadeIn(fnr_word, 0.5 * UP),
            GrowArrow(fnr_arrow),
        )
        self.play(
            FadeIn(spec_word, 0.5 * DOWN),
            GrowArrow(spec_arrow),
        )
        self.wait()
        for randy in randys:
            self.play(Blink(randy))
        self.wait()
