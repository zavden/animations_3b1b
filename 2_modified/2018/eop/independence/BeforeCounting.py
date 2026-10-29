# ==============================================================================
# Scene:      BeforeCounting
# Source:     videos/_2018/eop/independence.py (lines 720-745)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BeforeCounting.py BeforeCounting -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import once_useful_constructs.combinatorics explicitly (PascalsTriangle came from the Cairo big import pile)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: PascalsTriangle came from once_useful_constructs.combinatorics via the Cairo big import pile; import it explicitly
from once_useful_constructs.combinatorics import *

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


class BeforeCounting(TeacherStudentsScene):
    def construct(self):
        triangle = PascalsTriangle(nrows = 7)
        triangle.set_height(4)
        triangle.next_to(self.teacher, UP+LEFT)

        prob = get_probability_of_slot_group([True, True, False])
        prob.to_edge(UP)
        brace = Brace(prob, DOWN)
        q_marks = brace.get_text("???")

        self.teacher.change_mode("raise_right_hand")
        self.add(triangle)
        self.play_student_changes(*["hooray"]*3)
        self.play(
            triangle.scale, 0.5,
            triangle.to_corner, UP+RIGHT,
            self.teacher.change_mode, "sassy"
        )
        self.play_student_changes(*["confused"]*3)
        self.play(Write(prob))
        self.play(
            GrowFromCenter(brace),
            LaggedStartMap(FadeIn, q_marks)
        )
        self.wait(2)
