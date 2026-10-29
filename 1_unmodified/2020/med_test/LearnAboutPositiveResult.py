# ==============================================================================
# Scene:      LearnAboutPositiveResult
# Source:     videos/_2020/med_test.py (lines 1278-1312)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LearnAboutPositiveResult.py LearnAboutPositiveResult -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WomanIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("woman_icon", **kwargs)
        self.remove(self[0])


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


class LearnAboutPositiveResult(Scene):
    def construct(self):
        doctors = VGroup(
            SVGMobject("female_doctor"),
            SVGMobject("male_doctor"),
        )
        for doc in doctors:
            doc.remove(doc[0])
            doc.set_height(3)
        doctors.set_stroke(width=0)
        doctors.set_fill(GREY_C)
        doctors.set_gloss(0.5)
        doctors.arrange(RIGHT, buff=3)
        doctors.move_to(DOWN)

        self.add(doctors)

        bubbles = VGroup(*(ThoughtBubble(height=2, width=2) for x in range(2)))
        bubbles[1].flip()
        for bubble, doc in zip(bubbles, doctors):
            bubble.pin_to(doc)
            icon = WomanIcon()
            icon.set_height(0.5)
            bubble.add_content(icon)
            bubble.add(icon)

        self.play(LaggedStartMap(FadeIn, bubbles))

        clipboard = get_covid_clipboard("Cancer")
        clipboard.move_to(DOWN)
        clipboard[2].set_opacity(0)

        self.play(FadeIn(clipboard, UP))
        self.play(clipboard[2].set_opacity, 1)
        self.wait()
