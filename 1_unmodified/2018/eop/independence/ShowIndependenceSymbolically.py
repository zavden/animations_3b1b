# ==============================================================================
# Scene:      ShowIndependenceSymbolically
# Source:     videos/_2018/eop/independence.py (lines 1536-1573)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowIndependenceSymbolically.py ShowIndependenceSymbolically -w -m --fps 15
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


class ShowIndependenceSymbolically(Scene):
    def construct(self):
        filler_tex = "Filler"
        rhs = OldTex("=", "0.8")
        rhs.set_color_by_tex("0.8", YELLOW)
        rhs.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        lhs = OldTex("P(", filler_tex, "|", filler_tex, ")")
        lhs.next_to(rhs, LEFT)
        VGroup(lhs, rhs).scale(1.5)
        for part in lhs.get_parts_by_tex(filler_tex):
            slot_group = get_slot_group(
                [True, True, True],
                buff = SMALL_BUFF,
                include_qs = False,
            )
            slot_group.replace(part, dim_to_match = 0)
            lhs.submobjects[lhs.index_of_part(part)] = slot_group
        VGroup(*lhs[1].content[:2]).set_fill(BLACK, 0)
        condition = lhs[3]
        condition.content[2].set_fill(BLACK, 0)
        bool_lists = [
            [False], [True, False], [False, True], [True],
        ]
        arrow = Arrow(UP, DOWN)
        arrow.next_to(condition, UP)
        arrow.set_color(RED)
        words = OldTexText("Doesn't matter")
        words.set_color(RED)
        words.next_to(arrow, UP)

        self.add(rhs, lhs, arrow, words)
        self.wait()
        for bool_list in bool_lists:
            slot_group = get_slot_group(bool_list, SMALL_BUFF, False)
            slot_group.replace(condition)
            slot_group.move_to(condition, DOWN)
            self.play(Transform(condition, slot_group))
            self.wait()
