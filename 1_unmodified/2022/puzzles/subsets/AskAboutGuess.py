# ==============================================================================
# Scene:      AskAboutGuess
# Source:     videos/_2022/puzzles/subsets.py (lines 752-842)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutGuess.py AskAboutGuess -w -m --fps 15
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


class AskAboutGuess(InteractiveScene):
    def construct(self):
        # Number line
        virt_N = 64
        line = NumberLine(
            (0, virt_N, 1),
            tick_size=0.02,
            longer_tick_multiple=4,
            big_tick_numbers=range(0, virt_N + virt_N // 8, virt_N // 8),
            width=FRAME_WIDTH - 2
        )

        line.move_to(2.0 * DOWN)

        kw = dict(font_size=24)
        line_labels = VGroup(
            Tex("0", **kw),
            Tex("2^{1{,}998}", **kw),
            Tex("2^{1{,}999}", **kw),
            Tex("3 \\cdot 2^{1{,}998}", **kw),
            Tex("2^{2{,}000}", **kw),
        )
        for n, label in zip(np.linspace(0, virt_N, 5), line_labels):
            label.next_to(line.n2p(n), DOWN, MED_SMALL_BUFF)

        self.add(line)
        self.add(line_labels)

        # Set label
        title = get_question_title()
        title.to_edge(UP)
        self.add(title)
        # set_tex = get_set_tex(range(1, 2001), max_shown=21)
        # set_tex.scale(0.75)
        # set_tex.to_edge(UP)
        # self.add(set_tex)

        # Arrow with labels
        right_arrow = Vector(DOWN, color=BLUE)
        right_arrow.next_to(line.n2p(virt_N), UP, buff=0)
        right_label = Text("Total number\nof subsets", font_size=36)
        right_label.next_to(right_arrow, UP)
        right_label.shift_onto_screen(buff=MED_SMALL_BUFF)

        left_arrow = right_arrow.copy()
        left_arrow.set_color(YELLOW)
        left_arrow.next_to(line.n2p(virt_N / 5), UP, buff=0)
        left_label = OldTexText("Guess: ", "$\\frac{1}{5} \\cdot 2^{2{,}000}$", font_size=36)
        left_label.next_to(left_arrow, UP)

        self.add(right_label)
        self.add(right_arrow)

        self.play(
            TransformFromCopy(right_arrow, left_arrow),
            FadeTransform(right_label.copy(), left_label),
        )
        self.wait()

        # Not an integer
        guess_part = left_label[1]
        guess_rect = SurroundingRectangle(guess_part, buff=SMALL_BUFF)
        guess_rect.round_corners()
        guess_rect.set_stroke(RED, 2)
        nonint = Text("Not an integer!", color=RED)
        nonint.next_to(guess_rect, UP)

        self.play(
            ShowCreation(guess_rect),
            Write(nonint)
        )
        self.wait()

        # More or less
        dot = GlowDot(color=TEAL)
        dot.move_to(line.n2p(virt_N / 5))
        tip = Triangle(start_angle=-PI / 2)
        tip.set_stroke(width=0)
        tip.set_fill(TEAL, 1)
        tip.set_height(0.1)
        tip.add_updater(lambda t: t.move_to(dot.get_center(), DOWN))

        self.play(FadeIn(dot), FadeIn(tip))
        for dist in [0.2, 1.5]:
            for vect in [RIGHT, 2 * LEFT]:
                self.play(dot.animate.shift(dist * vect))
                self.add(Group(dot, tip).copy().clear_updaters().set_opacity(0.5))
            self.wait()
        for n in range(40):
            dot.move_to(line.n2p(virt_N / 5 + random.uniform(-8, 8)))
            self.wait(0.25)
