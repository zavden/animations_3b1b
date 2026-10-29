# ==============================================================================
# Scene:      MedicalTestsMatter
# Source:     videos/_2020/med_test.py (lines 1387-1435)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MedicalTestsMatter.py MedicalTestsMatter -w -m --fps 15
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


class MedicalTestsMatter(Scene):
    def construct(self):
        randy = Randolph(height=3)
        randy.to_corner(DL)
        randy.shift(2 * RIGHT)

        clipboard = get_covid_clipboard()
        clipboard.next_to(randy, RIGHT)
        clipboard.set_y(0)

        clipboard_words = VGroup(
            OldTex("-", color=RED),
            OldTexText("SARS\\\\CoV-2"),
            OldTexText("Not Detected", color=RED),
        )
        for m1, m2 in zip(clipboard_words, clipboard[2]):
            m1.replace(m2, 0)

        clipboard.remove(clipboard[2])

        self.add(randy)
        self.play(
            FadeIn(clipboard, shift=LEFT),
            randy.change, 'guilty'
        )
        self.play(
            Write(clipboard_words),
            randy.change, "hooray", clipboard,
        )
        self.play(Blink(randy))

        question = OldTexText("What does\\\\really this mean?")
        question.next_to(clipboard, RIGHT, buff=1.5)
        question.shift(1.5 * UP)
        q_arrow = Arrow(
            question.get_bottom(), clipboard.get_right(),
            path_arc=-30 * DEGREES,
            buff=0.3,
        )

        self.play(
            FadeIn(question, shift=0.25 * UP),
            DrawBorderThenFill(q_arrow),
            randy.change, "confused",
        )
        self.play(randy.look_at, clipboard.get_top())
        self.play(Blink(randy))
        self.play(randy.look_at, clipboard.get_center())
        self.wait(3)
