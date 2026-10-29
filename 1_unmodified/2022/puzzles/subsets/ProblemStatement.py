# ==============================================================================
# Scene:      ProblemStatement
# Source:     videos/_2022/puzzles/subsets.py (lines 4238-4413)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProblemStatement.py ProblemStatement -w -m --fps 15
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


def get_integer_parts(set_tex):
    result = VGroup(*(
        sm for sm in set_tex
        if isinstance(sm, Integer)
    ))
    if len(result) == 0:
        result.move_to(set_tex)
    return result


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


def get_sum_wrapper(set_tex):
    wrapper = VGroup(
        OldTex("\\text{sum}\\big(\\big) = ")[0],
        Integer(sum(set_tex.values))
    )
    wrapper.set_height(1.25 * set_tex.get_height())
    wrapper[0][:4].next_to(set_tex, LEFT, SMALL_BUFF)
    wrapper[0][4:].next_to(set_tex, RIGHT, SMALL_BUFF)
    wrapper[1].next_to(wrapper[0][-1], RIGHT, buff=0.2)
    return wrapper


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


class ProblemStatement(TeacherStudentsScene):
    def construct(self):
        # Title
        title = Text("Useless puzzles with useful lessons", font_size=60)
        title.to_edge(UP)
        title.set_color(BLUE_C)
        underline = Underline(title, buff=-0.05)
        underline.insert_n_curves(20)
        underline.set_stroke(width=[1, 3, 3, 3, 1])
        words = VGroup(*(
            title.get_part_by_text(text)
            for text in title.get_text().split(" ")
        ))

        morty = self.teacher

        self.play(
            LaggedStart(*(
                FadeInFromPoint(word, morty.get_corner(UL))
                for word in words
            )),
            morty.change("raise_right_hand", title),
            self.change_students("happy", "thinking", "happy", look_at=title)
        )
        self.remove(words)
        self.add(title)
        self.play(ShowCreation(underline))
        self.wait(2)
        self.play_student_changes("pondering", "erm", "tease", look_at=title)
        self.wait(3)

        # Statement
        statement = get_question_title()
        set_tex = statement[1]

        self.play(
            FadeIn(statement),
            self.change_students(*3 * ["pondering"], look_at=statement),
            FadeOut(VGroup(title, underline), UP)
        )
        self.wait()
        self.play(
            LaggedStart(*(
                FlashAround(int_part)
                for int_part in get_integer_parts(set_tex)
            ), lag_ratio=0.05, run_time=3),
            self.change_students("erm", "sassy", "confused", look_at=statement),
        )
        self.wait(2)

        # Example subsets
        subsets = VGroup(
            get_set_tex([3, 1, 4]),
            get_set_tex([2, 3, 5]),
            get_set_tex(range(1, 2000, 2)),
        )
        subsets.move_to(UP)
        sum_wrappers = VGroup(*map(get_sum_wrapper, subsets))
        mode_triples = [
            ("erm", "pondering", "plain"),
            ("pondering", "thinking", "pondering"),
            ("thinking", "happy", "thinking"),
        ]

        sum_groups = VGroup()
        for subset, sum_wrapper, mode_triple in zip(subsets, sum_wrappers, mode_triples):
            self.play(
                morty.change("tease", subset),
                self.change_students(*mode_triple, look_at=subset),
                set_tex_transform(set_tex, subset),
            )
            elem_rects = VGroup(*(
                SurroundingRectangle(
                    get_part_by_value(set_tex, value)
                ).set_stroke(TEAL, 2).round_corners()
                for value in subset.values
            ))
            self.play(LaggedStartMap(ShowCreation, elem_rects, lag_ratio=0.5))

            self.wait()
            self.play(
                Write(sum_wrapper),
                morty.change("hooray" if subset is subsets[-1] else "tease", subset),
            )
            self.wait(2)
            mark = Checkmark() if sum(subset.values) % 5 == 0 else Exmark()
            sum_wrapper.refresh_bounding_box()
            mark.next_to(sum_wrapper, RIGHT)
            self.play(Write(mark))
            self.wait()
            anims = [FadeOut(elem_rects)]

            sum_group = VGroup(subset, sum_wrapper, mark)

            if subset is subsets[0]:
                self.play(
                    sum_group.animate.scale(0.5).to_edge(LEFT).set_y(2),
                    *anims
                )
            else:
                self.play(
                    sum_group.animate.scale(0.5).next_to(sum_groups, DOWN, MED_LARGE_BUFF, LEFT),
                    *anims
                )
            sum_groups.add(sum_group)

        self.play(
            self.change_students(
                "erm", "confused", "hesitant",
                look_at=statement,
            )
        )

        # Who cares?
        statement.generate_target()
        statement.target.scale(0.5)
        statement.target.to_corner(UL)
        title.set_opacity(0)
        title.scale(0.5)
        title.generate_target()
        title.target.set_opacity(1)
        title.target.scale(2)
        title.target.next_to(self.hold_up_spot, UP, MED_LARGE_BUFF)
        title.target.to_edge(RIGHT)

        self.play(
            PiCreatureSays(
                self.students[2], "Who cares?", target_mode="angry",
                bubble_config=dict(direction=LEFT),
            ),
            morty.change("guilty"),
            MoveToTarget(statement),
            FadeOut(sum_groups, LEFT)
        )
        self.wait()
        self.play(
            RemovePiCreatureBubble(
                self.students[2],
                target_mode="plain",
                look_at=ORIGIN,
            ),
            morty.change("sassy", self.students[2].eyes),
            self.change_students(
                "pondering", "pondering",
                look_at=ORIGIN,
            ),
            MoveToTarget(title),
        )
        self.play(Blink(morty))
        self.play(
            FlashAround(title, time_width=1),
            morty.change("raise_right_hand"),
        )
        self.wait()
        return

        # Start simpler
        small_set = get_set_tex(range(1, 6))
        small_set.to_edge(UP)

        case_words = Text("Start simple")
        case_words.next_to(small_set, DOWN)
        case_words.set_color(BLUE)

        self.play(
            statement.animate.set_y(0),
            set_tex_transform(set_tex, small_set),
            LaggedStartMap(
                FadeOut, self.pi_creatures, shift=DOWN,
            ),
            FadeOut(self.background),
            Write(case_words),
            run_time=2,
        )
        self.wait()
        self.play(FadeOut(statement), FadeOut(case_words))
