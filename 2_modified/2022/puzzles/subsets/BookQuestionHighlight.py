# ==============================================================================
# Scene:      BookQuestionHighlight
# Source:     videos/_2022/puzzles/subsets.py (lines 4477-4525)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BookQuestionHighlight.py BookQuestionHighlight -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - BookQuestion.jpg (placeholder book page, raster_images/; make_puzzles_assets.py)
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


class BookQuestionHighlight(InteractiveScene):
    def construct(self):
        # Temp
        img = ImageMobject("/Users/grant/Dropbox/3Blue1Brown/videos/2022/puzzles/subsets/images/BookQuestion.jpg")
        img.set_height(FRAME_HEIGHT)
        self.disable_interaction(img)

        # Highlight
        rect = FullScreenFadeRectangle(fill_color=BLACK, fill_opacity=0.975)
        lil_rect = Rectangle(5, 0.55)
        lil_rect.move_to([-0.2, 0, 0])
        lil_rect.reverse_points()
        rect.append_vectorized_mobject(lil_rect)

        self.play(
            FlashAround(
                lil_rect,
                color=BLACK,
                stroke_width=5,
                time_width=1.5,
                buff=0,
                run_time=2,
            ),
            FadeIn(rect, time_span=(0.5, 2)),
        )
        self.wait()

        # Title
        title = get_question_title()
        title.set_backstroke(width=7)

        self.play(
            FadeTransform(lil_rect.copy().set_opacity(0), title)
        )
        self.wait()
        self.play(
            LaggedStart(*(
                FlashAround(int_part)
                for int_part in get_integer_parts(title[1])
            ), lag_ratio=0.05, run_time=3),
        )
        self.wait(2)

        last_part = title[-1][-12:]
        self.play(
            FlashUnder(last_part, color=TEAL, buff=0, time_width=1.5, run_time=2),
            last_part.animate.set_fill(TEAL),
        )
        self.wait()
