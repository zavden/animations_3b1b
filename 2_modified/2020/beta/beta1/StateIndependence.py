# ==============================================================================
# Scene:      StateIndependence
# Source:     videos/_2020/beta/beta1.py (lines 3242-3281)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl StateIndependence.py StateIndependence -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - In ManimGL Arrow is a single shape without a .tip attribute; the rotation of the tip is omitted
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"


def get_checks_and_crosses(bools, width=12):
    result = VGroup()
    for positive in bools:
        if positive:
            mob = OldTex(CMARK_TEX)
            mob.set_color(GREEN)
        else:
            mob = OldTex(XMARK_TEX)
            mob.set_color(RED)
        mob.positive = positive
        mob.set_width(0.5)
        result.add(mob)
    result.arrange(RIGHT, buff=MED_SMALL_BUFF)
    result.set_width(width)
    return result


def get_random_checks_and_crosses(n=50, s=0.95, width=12):
    return get_checks_and_crosses(
        bools=(np.random.random(n) < s),
        width=width
    )



# ----- From _2020/beta/beta1.py -----

class StateIndependence(Scene):
    def construct(self):
        row = get_random_checks_and_crosses()
        row.to_edge(UP)
        # self.add(row)

        arrows = VGroup()
        for m1, m2 in zip(row, row[1:]):
            arrow = Arrow(
                m1.get_bottom() + 0.025 * DOWN,
                m2.get_bottom(),
                path_arc=145 * DEGREES,
                max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5,
            )
            # CHANGE: In ManimGL Arrow is a single shape without a .tip attribute; the rotation of the tip is omitted
            pass
            arrow.shift(SMALL_BUFF * DOWN)
            arrow.set_color(YELLOW)
            arrows.add(arrow)

        words = OldTexText("No influence")
        words.set_height(0.25)
        words.next_to(arrows[0], DOWN)

        self.play(
            ShowCreation(arrows[0]),
            FadeIn(words)
        )
        for i in range(10):
            self.play(
                words.next_to, arrows[i + 1], DOWN,
                FadeOut(arrows[i]),
                ShowCreation(arrows[i + 1])
            )
            last_arrow = arrows[i + 1]

        self.play(
            FadeOut(words),
            FadeOut(last_arrow),
        )
