# ==============================================================================
# Scene:      AssumeOrderDoesntMatter
# Source:     videos/_2018/eop/independence.py (lines 3132-3230)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AssumeOrderDoesntMatter.py AssumeOrderDoesntMatter -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_slot_group(
    bool_list, 
    buff = MED_LARGE_BUFF, 
    include_qs = True,
    min_bool_list_len = 3,
    ):
    if len(bool_list) < min_bool_list_len:
        bool_list += [None]*(min_bool_list_len - len(bool_list))
    n = len(bool_list)

    lines = VGroup(*[
        Line(ORIGIN, MED_LARGE_BUFF*RIGHT)
        for x in range(n)
    ])
    lines.arrange(RIGHT, buff = buff)
    if include_qs:
        labels = VGroup(*[
            OldTexText("Q%d"%d) for d in range(1, n+1)
        ])
    else:
        labels = VGroup(*[VectorizedPoint() for d in range(n)])
    for label, line in zip(labels, lines):
        label.scale(0.7)
        label.next_to(line, DOWN, SMALL_BUFF)
    slot_group = VGroup()
    slot_group.lines = lines
    slot_group.labels = labels
    slot_group.content = VGroup()
    slot_group.digest_mobject_attrs()
    slot_group.to_edge(RIGHT)
    slot_group.bool_list = bool_list

    total_height = FRAME_Y_RADIUS
    base = 2.3

    for i, line in enumerate(lines):
        if i >= len(bool_list) or bool_list[i] is None:
            mob = VectorizedPoint()
        elif bool_list[i]:
            mob = OldTex("\\checkmark")
            mob.set_color(GREEN)
            slot_group.shift(total_height*DOWN / (base**(i+1)))
        else:
            mob = OldTex("\\times")
            mob.set_color(RED)
            slot_group.shift(total_height*UP / (base**(i+1)))
        mob.next_to(line, UP, SMALL_BUFF)
        slot_group.content.add(mob)
    return slot_group


def get_probability_of_slot_group(bool_list, conditioned_list = None):
    filler_tex = "Fi"*max(len(bool_list), 3)
    if conditioned_list is None:
        result = OldTex("P(", filler_tex, ")")
    else:
        result = OldTex("P(", filler_tex, "|", filler_tex, ")")
    fillers = result.get_parts_by_tex(filler_tex)
    for filler, bl in zip(fillers, [bool_list, conditioned_list]):
        slot_group = get_slot_group(
            bl, buff = SMALL_BUFF, include_qs = False,
        )
        slot_group.replace(filler, dim_to_match = 0)
        slot_group.shift(0.5*SMALL_BUFF*DOWN)
        index = result.index_of_part(filler)
        result.submobjects[index] = slot_group
    return result


class AssumeOrderDoesntMatter(Scene):
    def construct(self):
        self.force_skipping()

        self.add_title()
        self.show_equality()
        self.mention_correlation()

        self.revert_to_original_skipping_status()
        self.coming_soon()

    def add_title(self):
        title = OldTexText(
            "Softer simplifying assumption: " +\
            "Order doesn't matter"
        )
        title.to_edge(UP)

        self.add(title)
        self.title = title

    def show_equality(self):
        n = 3
        prob_groups = VGroup(*[
            VGroup(*list(map(
                get_probability_of_slot_group,
                [t for t in it.product(*[[True, False]]*n) if sum(t) == k]
            )))
            for k in range(n+1)
        ])
        for prob_group in prob_groups:
            for prob in prob_group[:-1]:
                equals = OldTex("=")
                equals.next_to(prob, RIGHT)
                prob.add(equals)
            prob_group.arrange(RIGHT)
            max_width = FRAME_WIDTH - 1
            if prob_group.get_width() > max_width:
                prob_group.set_width(max_width)
        prob_groups.arrange(DOWN, buff = 0.7)
        prob_groups.next_to(self.title, DOWN, MED_LARGE_BUFF)

        self.play(FadeIn(
            prob_groups[1],
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(2)
        self.play(FadeIn(
            VGroup(prob_groups[0], *prob_groups[2:]),
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait()

        self.prob_groups = prob_groups

    def mention_correlation(self):
        assumption_group = VGroup(*self.get_top_level_mobjects())
        question = OldTexText(
            "But what is ", "``correlation''", "?",
            arg_separator = ""
        )
        question.set_color(BLUE)
        question.to_edge(UP)
        bottom = question.get_bottom()

        self.play(
            Write(question),
            assumption_group.next_to, bottom, DOWN, LARGE_BUFF
        )
        self.wait()

        self.assumption_group = assumption_group
        self.question = question

    def coming_soon(self):
        self.play(
            LaggedStartMap(
                ApplyMethod, self.assumption_group,
                lambda m : (m.shift, FRAME_HEIGHT*DOWN),
                remover = True,
            ),
            ApplyMethod(
                self.question.center,
                rate_func = squish_rate_func(smooth, 0.5, 1),
                run_time = 2
            )
        )

        part = self.question.get_part_by_tex("correlation")
        brace = Brace(part, UP)
        words = brace.get_text("Coming soon!")
        self.play(
            GrowFromCenter(brace),
            part.set_color, YELLOW
        )
        self.play(Write(words))
        self.wait()
