# ==============================================================================
# Scene:      HighlightAnswerParts
# Source:     videos/_2022/puzzles/subsets.py (lines 5317-5342)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighlightAnswerParts.py HighlightAnswerParts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_set_tex(values, max_shown=7, **kwargs):
    if len(values) > max_shown:
        value_mobs = [
            *map(Integer, values[:max_shown - 2]),
            Tex("\\dots"),
            Integer(values[-1], group_with_commas=False),
        ]
    else:
        value_mobs = list(map(Integer, values))

    commas = Tex(",").replicate(len(value_mobs) - 1)
    result = VGroup()
    result.add(Tex("\\{"))
    result.add(*it.chain(*zip(value_mobs, commas)))
    if len(value_mobs) > 0:
        result.add(value_mobs[-1].align_to(value_mobs[0], UP))
    result.add(Tex("\\}"))
    result.arrange(RIGHT, buff=SMALL_BUFF)
    if len(values) > 0:
        commas.set_y(value_mobs[0].get_y(DOWN))
    if len(values) > max_shown:
        result[-4].match_y(commas)
    result.values = values
    return result


def get_question_title():
    st = "$\\{1, 2, 3, 4, 5, \\dots, 2{,}000\\}$"
    question = OldTexText(
        f"Find the number of subsets of {st},\\\\"
        " the sum of whose elements is divisible by 5",
        isolate=[st]
    )
    set_tex = get_set_tex(range(1, 2001))
    set_tex.set_color(BLUE)
    set_tex.replace(question.get_part_by_tex(st))
    question.replace_submobject(1, set_tex)
    question.to_edge(UP)
    return question


class HighlightAnswerParts(InteractiveScene):
    def construct(self):
        self.add(get_question_title())

        frac = "\\frac{1}{5}"
        e1 = "2^{2{,}000}"
        e2 = "4 \\cdot 2^{400}"
        answer = Tex(
            f"{frac} \\Big({e1} + {e2} \\Big)",
            isolate=[frac, e1, e2],
            font_size=60
        )
        answer.move_to(UP)
        p1 = VGroup(answer.select_part(frac), answer.select_part(e1))
        p2 = answer.select_part(e2)

        p1_rect = SurroundingRectangle(p1)
        p2_rect = SurroundingRectangle(p2)

        self.add(answer)
        self.wait()
        self.play(ShowCreation(p1_rect))
        self.wait()
        self.play(ShowCreation(p2_rect), FadeOut(p1_rect))
        self.wait()
        self.play(FadeOut(p2_rect))
