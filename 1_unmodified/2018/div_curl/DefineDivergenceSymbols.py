# ==============================================================================
# Scene:      DefineDivergenceSymbols
# Source:     videos/_2018/div_curl.py (lines 1605-1655)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineDivergenceSymbols.py DefineDivergenceSymbols -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineDivergenceSymbols(Scene):
    def construct(self):
        tex_mob = OldTex(
            "\\text{div}",
            "\\textbf{F}",
            "(x, y)",
            "=",
        )
        div, F, xy, eq = tex_mob
        output = DecimalNumber(0, include_sign=True)
        output.next_to(tex_mob, RIGHT)
        time_tracker = ValueTracker()
        always_shift(time_tracker, rate=1)
        self.add(time_tracker)
        output_animation = ContinualChangingDecimal(
            output, lambda a: 3 * np.cos(int(time_tracker.get_value())),
        )

        F.set_color(BLUE)
        xy.set_color(YELLOW)

        F_brace = Brace(F, UP, buff=SMALL_BUFF)
        F_label = F_brace.get_text(
            "Vector field function",
        )
        F_label.match_color(F)
        xy_brace = Brace(xy, DOWN, buff=SMALL_BUFF)
        xy_label = xy_brace.get_text("Some point")
        xy_label.match_color(xy)
        output_brace = Brace(output, UP, buff=SMALL_BUFF)
        output_label = output_brace.get_text(
            "Measure of how much \\\\ "
            "$(x, y)$ ``generates'' fluid"
        )
        brace_label_pairs = [
            (F_brace, F_label),
            (xy_brace, xy_label),
            (output_brace, output_label),
        ]

        self.add(tex_mob, output_animation)
        fade_anims = []
        for brace, label in brace_label_pairs:
            self.play(
                GrowFromCenter(brace),
                FadeInFromDown(label),
                *fade_anims
            )
            self.wait(2)
            fade_anims = list(map(FadeOut, [brace, label]))
        self.wait()
