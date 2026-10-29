# ==============================================================================
# Scene:      CompareFreqDecays1to4
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 850-853)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareFreqDecays1to4.py CompareFreqDecays1to4 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareFreqDecays1to2(Scene):
    CONFIG = {
        "freqs": [1, 2]
    }

    def construct(self):
        background = FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        )

        screens = VGroup(*[
            ScreenRectangle(
                height=4,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=1,
                stroke_color=WHITE,
            )
            for x in range(2)
        ])
        screens.arrange(RIGHT)
        screens.set_width(FRAME_WIDTH - 1)

        formulas = VGroup(*[
            self.get_formula(freq)
            for freq in self.freqs
        ])
        for formula, screen in zip(formulas, screens):
            formula.next_to(screen, UP)

        self.add(background)
        self.add(screens)
        self.add(formulas)
        self.wait()

    def get_formula(self, freq):
        f_str = str(freq)
        return OldTex(
            "\\cos\\left(%s \\cdot {x}\\right)" % f_str,
            "e^{-\\alpha \\cdot %s^2 \\cdot {t}}" % f_str,
            tex_to_color_map={
                "{x}": GREEN,
                "{t}": YELLOW,
                f_str: MAROON_B,
            }
        )


class CompareFreqDecays1to4(CompareFreqDecays1to2):
    CONFIG = {
        "freqs": [1, 4],
    }
