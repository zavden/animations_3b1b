# ==============================================================================
# Scene:      TwoThousandBinaryChoices
# Source:     videos/_2022/puzzles/subsets.py (lines 693-749)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoThousandBinaryChoices.py TwoThousandBinaryChoices -w -m --fps 15
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


def get_integer_parts(set_tex):
    result = VGroup(*(
        sm for sm in set_tex
        if isinstance(sm, Integer)
    ))
    if len(result) == 0:
        result.move_to(set_tex)
    return result


class TwoThousandBinaryChoices(InteractiveScene):
    def construct(self):
        # Build parts
        full_set = get_set_tex(range(1, 2001), max_shown=25)
        full_set.set_width(0.9 * FRAME_WIDTH)
        full_set.center()
        self.add(full_set)

        elems = get_integer_parts(full_set)
        elem_rects = VGroup(*(
            SurroundingRectangle(elem, buff=0.05).round_corners()
            for elem in elems
        ))
        elem_rects.set_stroke(BLUE, 2)

        twos = VGroup(*(
            Integer(2).match_width(elems[1]).next_to(er, UP)
            for er in elem_rects
        ))
        dots = VGroup(*(
            Tex("\\cdot").move_to(midpoint(t1.get_right(), t2.get_left()))
            for t1, t2 in zip(twos, twos[1:])
        ))
        dots.replace_submobject(-1, Tex("\\dots").move_to(dots[-1]))
        dots.add_to_back(VMobject())

        choices = Text("choices").match_height(twos)
        VGroup(twos, dots, choices).set_color(TEAL)

        # Label choices
        words = Text("2,000 Binary choices")
        words.set_color(TEAL)
        words.next_to(full_set, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            LaggedStartMap(ShowCreationThenFadeOut, elem_rects, lag_ratio=0.05),
            FadeIn(words, 0.5 * DOWN)
        )
        self.wait()

        # Go through all choices
        self.add(choices)
        for rect, two, dot in zip(elem_rects, twos, dots):
            choices.next_to(two, RIGHT, buff=0.2)
            marks = VGroup(Checkmark(), Exmark())
            marks.scale(0.5)
            marks.next_to(rect, DOWN, SMALL_BUFF)
            self.add(two, dot)
            include = random.random() < 0.5
            if include:
                self.add(rect)
                marks.submobjects.reverse()
            self.play(ShowSubmobjectsOneByOne(marks.copy(), remover=True, run_time=0.5))
            self.add(marks[-1])
            self.wait(0.25)
        self.remove(choices)
        self.wait()
