# ==============================================================================
# Scene:      Thumbnail3
# Source:     videos/_2020/med_test.py (lines 231-269)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail3.py Thumbnail3 -w -m --fps 15
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


class Thumbnail3(Scene):
    def construct(self):
        bg = FullScreenFadeRectangle()
        bg.set_fill(BLACK, 1)
        # bg.set_gloss(0.4)
        self.add(bg)

        # Just the clipboard
        clipboard = get_covid_clipboard("Cancer", color=GREEN)
        clipboard[2][0].set_stroke(GREEN, 8)
        clipboard[2].scale(0.9)
        clipboard.set_height(7)
        clipboard.center().to_edge(LEFT, buff=1.0)
        self.add(clipboard)

        clipback = VMobject()
        clipback.set_points(clipboard[1].get_subpaths()[0])
        clipback.set_stroke(BLACK, 0)
        clipback.set_fill(GREY_E, 1)
        self.add(clipback, clipboard)

        # Title
        words = VGroup(
            VGroup(
                OldTex("90\\%").scale(1.8).set_color(GREEN),
                OldTexText("test accuracy", alignment="")
            ).arrange(DOWN, aligned_edge=LEFT, buff=SMALL_BUFF),
            VGroup(
                OldTex("9\\%").scale(1.8).set_color(RED),
                OldTexText("chance it's true", alignment="")
            ).arrange(DOWN, aligned_edge=LEFT, buff=SMALL_BUFF),
            Text("...how?")
        )
        words.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        # words.set_width(FRAME_WIDTH - clipboard.get_width() - 1.5)
        words.set_height(FRAME_HEIGHT - 2)
        words.to_edge(RIGHT, buff=1.0)
        words.set_stroke(BLACK, 10, background=True)
        self.add(words)
