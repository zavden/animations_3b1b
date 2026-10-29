# ==============================================================================
# Scene:      AnswerGuess
# Source:     videos/_2022/puzzles/subsets.py (lines 473-598)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AnswerGuess.py AnswerGuess -w -m --fps 15
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


def get_part_by_value(set_tex, value):
    try:
        return next(sm for sm in set_tex if isinstance(sm, Integer) and sm.get_value() == value)
    except StopIteration:
        return VMobject().move_to(set_tex)


def get_brackets(set_tex):
    return VGroup(set_tex[0], set_tex[-1])


def set_tex_transform(set_tex1, set_tex2):
    bracket_anim = TransformFromCopy(
        get_brackets(set_tex1),
        get_brackets(set_tex2),
    )
    matching_anims = [
        TransformFromCopy(
            get_part_by_value(set_tex1, value),
            get_part_by_value(set_tex2, value),
        )
        for value in filter(
            lambda v: v in set_tex2.values,
            set_tex1.values,
        )
    ]
    mismatch_animations = [
        FadeInFromPoint(
            get_part_by_value(set_tex2, value),
            set_tex1.get_center()
        )
        for value in set(set_tex2.values).difference(set_tex1.values)
    ]
    anims = [bracket_anim, *matching_anims, *mismatch_animations]
    if len(set_tex2.values) > 1:
        commas = []
        for st in set_tex1, set_tex2:
            if len(st.values) > 1:
                commas.append(st[2:-1:2])
            else:
                commas.append(Tex(",").set_opacity(0).move_to(st, DOWN))
        comma_animations = TransformFromCopy(*commas)
        anims.append(comma_animations)
    for part in set_tex2:
        if isinstance(part, Tex) and part.get_tex() == "\\dots":
            anims.append(FadeInFromPoint(part, set_tex1.get_bottom()))
    return AnimationGroup(*anims)


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


def massive_int(num, n_cols=42, width=7):
    total = VGroup(*(Integer(int(digit)) for digit in str(num)))
    total.arrange_in_grid(h_buff=SMALL_BUFF, v_buff=1.5 * SMALL_BUFF, n_cols=n_cols)
    for n in range(len(total) - 3, -3, -3):
        comma = Tex(",")
        triplet = total[n:n + 3]
        triplet.arrange_to_fit_width(
            triplet.get_width() - 2 * comma.get_width(),
            about_edge=LEFT
        )
        comma.move_to(triplet.get_corner(DR) + 1.5 * comma.get_width() * RIGHT)
        total.insert_submobject(n + 3, comma)
    total[-1].set_opacity(0)
    total.set_width(width)
    return total


class AnswerGuess(InteractiveScene):
    def construct(self):
        # Count total
        title = get_question_title()

        count = VGroup(Text("Total subsets: "), Tex("2^{2{,}000}"))
        count[0].set_color(TEAL)
        count.arrange(RIGHT, buff=MED_SMALL_BUFF, aligned_edge=DOWN)
        count.scale(60 / 48)
        count.next_to(title, DOWN, LARGE_BUFF)

        self.add(title)
        self.wait()
        self.play(Write(count[0]))
        self.play(
            GrowFromCenter(count[1][0]),
            FadeTransform(title[1][-6:-1].copy(), count[1][1:]),
        )
        self.wait()

        # Ask about why
        count_rect = SurroundingRectangle(count, buff=MED_SMALL_BUFF)
        count_rect.set_stroke(TEAL, 2)
        randy = Randolph(height=1.5)
        randy.flip()
        randy.next_to(count_rect, RIGHT, LARGE_BUFF).shift(0.5 * DOWN)
        randy.get_bubble(Text("Why?", font_size=24), direction=LEFT, height=1.0, width=1.0)

        self.play(
            ShowCreation(count_rect),
            VFadeIn(randy),
            randy.change("maybe", count_rect),
            Write(randy.bubble),
            Write(randy.bubble.content),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("thinking").look(DL))
        self.play(Blink(randy))
        randy.add(randy.bubble, randy.bubble.content)
        self.wait()
        self.play(*map(FadeOut, [randy, count_rect]))

        # Show total digits
        count.generate_target()
        count.target.to_edge(LEFT)
        eq = Tex("=")
        eq.next_to(count.target, RIGHT).match_y(count[1][0])

        total = massive_int(2**2000)
        total.next_to(eq, RIGHT).align_to(count, UP)

        self.play(MoveToTarget(count), Write(eq))
        self.play(ShowIncreasingSubsets(total, run_time=5))
        self.wait()
        self.play(
            FadeOut(total, 0.1 * DOWN, lag_ratio=0.01),
            FadeOut(eq),
        )

        # Guess 1 / 5
        guess = VGroup(Text("Guess: "), Tex("\\approx \\frac{1}{5} \\cdot 2^{2{,}000}"))
        guess[0].set_color(YELLOW)
        guess.arrange(RIGHT)
        guess.next_to(count, RIGHT, buff=2.5)
        guess.match_y(count[0])

        self.play(Write(guess[0]))
        self.play(TransformMatchingShapes(count[1].copy(), guess[1], path_arc=30 * DEGREES))
        self.wait()

        # Simplify
        small_set = get_set_tex(range(1, 6))
        small_set.to_edge(UP)
        simplify = Text("Simplify!")
        simplify.next_to(small_set, DOWN, MED_LARGE_BUFF)
        simplify.set_color(YELLOW)

        self.play(
            LaggedStartMap(
                FadeOut, VGroup(count, guess),
                lag_ratio=0.25,
                run_time=1,
            )
        )
        self.remove(title)
        self.play(
            FadeOut(title[0], scale=0.5),
            FadeOut(title[2], scale=0.5),
            set_tex_transform(title[1], small_set),
            FadeIn(simplify, scale=2)
        )
        self.wait()

        # Ask questions
        kw = dict(t2c={
            "construct": YELLOW,
            "organize": TEAL,
        })
        questions = VGroup(
            Text("What are all\nthe subsets?", **kw),
            Text("How do you\norganize them?", **kw),
            Text("How do you\nconstruct them?", **kw),
        )
        questions.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        questions.to_edge(LEFT).to_edge(DOWN, buff=LARGE_BUFF)

        self.play(FadeTransform(simplify, questions[0]))
        self.wait()
        self.play(Write(questions[1], run_time=1))
        self.wait()
        self.play(
            TransformFromCopy(
                questions[1].get_part_by_text("How do you"),
                questions[2].get_part_by_text("How do you"),
            ),
            TransformFromCopy(
                questions[1][-5:],
                questions[2][-5:],
            ),
            FadeTransform(
                questions[1].get_part_by_text("organize").copy(),
                questions[2].get_part_by_text("construct"),
            )
        )
        self.wait()
