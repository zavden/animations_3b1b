# ==============================================================================
# Scene:      Thumbnail1
# Source:     videos/_2020/med_test.py (lines 59-175)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail1.py Thumbnail1 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Defines `clipboard` (in the original it was not defined on that branch: UnboundLocalError) and removes the embed()
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


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


# Scenes
class Thumbnail1(Scene):
    def construct(self):
        # New
        bg = FullScreenFadeRectangle()
        bg.set_fill(BLACK, 1)
        bg.set_gloss(0.2)
        self.add(bg)

        pre_pop = VGroup(*(WomanIcon() for x in range(5 * 6)))
        pre_pop.arrange_in_grid(5, 6, fill_rows_first=False)
        pre_pop.set_height(4)
        pre_pop[:5].shift(MED_LARGE_BUFF * LEFT)
        pre_pop[:5].set_fill(YELLOW)
        pre_pop[5:].set_fill(GREY_C)

        post_pop = pre_pop.copy()
        post_pop.set_opacity(0.1)
        for icon in (*post_pop[:4], *post_pop[5::5]):
            rect = SurroundingRectangle(icon, buff=0.01)
            rect.set_stroke(GREEN, 5)
            icon.set_opacity(1)
            plus = OldTex("+")
            plus.set_color(GREEN)
            plus.set_width(rect.get_width() / 2)
            plus.move_to(rect.get_corner(UR))
            plus.shift(0.05 * UR)
            icon.set_stroke(BLACK, 2, background=True)
            icon.push_self_into_submobjects()
            icon.add_to_back(rect, plus)
            icon.set_stroke(background=True)

        for pop in pre_pop, post_pop:
            colon = OldTex(":", font_size=96)
            colon.move_to(pop[:10])
            pop.add(colon)

        arrow = Arrow(LEFT, RIGHT, thickness=0.1)
        arrow.scale(1.75)

        group = VGroup(pre_pop, arrow, post_pop)
        group.arrange(RIGHT, buff=1.0)
        group.to_edge(UP)
        post_pop.align_to(pre_pop, DOWN)

        self.add(group)

        # Or try something else...
        self.remove(group)
        randy = Randolph(color=SICKLY_GREEN, mode="sick")
        randy.set_height(4)
        randy.next_to(ORIGIN, RIGHT, buff=0.5).to_edge(UP)
        # CHANGE: in the original `clipboard` was not defined on this branch (UnboundLocalError)
        clipboard = get_covid_clipboard("Virus")
        clipboard.set_height(4)
        clipboard.next_to(ORIGIN, LEFT, buff=0.5).to_edge(UP)
        self.add(randy)
        self.add(clipboard)
        #

        new_bayes_rule = OldTexText(
            "Post = (Prior)(Bayes factor)",
            tex_to_color_map={
                "(Prior)": YELLOW,
                "(Bayes factor)": BLUE,
            }
        )
        new_bayes_rule.set_width(FRAME_WIDTH - 1)
        new_bayes_rule.move_to(2 * DOWN)

        self.add(new_bayes_rule)

        new_rule_words = OldTexText("Bayes rule redesigned")
        new_rule_words.scale(1.75)
        new_rule_words.next_to(new_bayes_rule, DOWN, MED_LARGE_BUFF)
        new_rule_words.set_fill(GREY_A)
        self.add(new_rule_words)

        # CHANGE: the embed() (interactive session) is removed so that the render finishes
        return

        # Old
        title = OldTexText("Interpreting medical tests", font_size=90)
        title.to_edge(UP)
        self.add(title)

        factor = OldTex(
            "{P(+ \\,|\\, \\text{Virus}) \\over P(+ \\,|\\, \\text{No virus})}",
            tex_to_color_map={
                "+": GREEN,
                "\\text{Virus}": YELLOW,
                "\\text{No virus}": GREY_B,
            }
        )
        factor.scale(2)
        rect = SurroundingRectangle(factor, buff=MED_SMALL_BUFF)
        rect.set_stroke(BLUE, 3)
        factor.add(rect)
        self.add(factor)

        clipboard = get_covid_clipboard("Virus")
        clipboard[2][0].set_stroke(GREEN, 8)
        clipboard[2].scale(0.9)
        clipboard.set_height(4)
        clipboard.next_to(factor, LEFT, LARGE_BUFF)
        VGroup(clipboard, factor).next_to(title, DOWN, buff=0.7)

        self.add(clipboard)

        brace = Brace(factor, DOWN, buff=0.4)
        brace.stretch(1.5, 1, about_edge=UP)
        text = brace.get_text("How much your belief should change", buff=0.4)
        text.scale(1.5, about_edge=UP)
        text.shift_onto_screen()
        text.match_color(rect)
        brace.add(text)
        self.add(brace)

        self.embed()
