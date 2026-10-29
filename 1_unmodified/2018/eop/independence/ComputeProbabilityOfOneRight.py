# ==============================================================================
# Scene:      ComputeProbabilityOfOneRight
# Source:     videos/_2018/eop/independence.py (lines 1643-1652)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComputeProbabilityOfOneRight.py ComputeProbabilityOfOneRight -w -m --fps 15
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


class ComputeProbabilityOfOneWrong(Scene):
    CONFIG = {
        "score" : 2,
        "final_result_rhs_tex" : [
            "3", "(0.8)", "^2", "(0.2)", "=", "0.384",
        ],
        "default_bool" : True,
        "default_p" : "0.8",
        "default_q" : "0.2",
    }
    def construct(self):
        self.show_all_three_patterns()
        self.show_final_result()

    def show_all_three_patterns(self):
        probabilities = VGroup()
        point_8s = VGroup()
        point_2s = VGroup()
        for i in reversed(list(range(3))):
            bool_list = [self.default_bool]*3
            bool_list[i] = not self.default_bool
            probs = ["(%s)"%self.default_p]*3
            probs[i] = "(%s)"%self.default_q
            lhs = get_probability_of_slot_group(bool_list)
            rhs = OldTex("=", *probs)
            rhs.set_color_by_tex("0.8", GREEN)
            rhs.set_color_by_tex("0.2", RED)
            point_8s.add(*rhs.get_parts_by_tex("0.8"))
            point_2s.add(*rhs.get_parts_by_tex("0.2"))
            rhs.next_to(lhs, RIGHT)
            probabilities.add(VGroup(lhs, rhs))
        probabilities.arrange(DOWN, buff = LARGE_BUFF)
        probabilities.center()

        self.play(Write(probabilities[0]))
        self.wait(2)
        for i in range(2):
            self.play(ReplacementTransform(
                probabilities[i].copy(),
                probabilities[i+1]
            ))
        self.wait()
        for group in point_8s, point_2s:
            self.play(LaggedStartMap(
                Indicate, group,
                rate_func = there_and_back,
                lag_ratio = 0.7
            ))
            self.wait()

    def show_final_result(self):
        result = OldTex(
            "P(", "\\text{Score} = %s"%self.score, ")", "=",
            *self.final_result_rhs_tex
        )
        result.set_color_by_tex_to_color_map({
            "0.8" : GREEN,
            "0.2" : RED,
            "Score" : YELLOW,
        })
        result[-1].set_color(YELLOW)
        result.set_color_by_tex("0.8", GREEN)
        result.set_color_by_tex("0.2", RED)
        result.to_edge(UP)

        self.play(Write(result))
        self.wait()


class ComputeProbabilityOfOneRight(ComputeProbabilityOfOneWrong):
    CONFIG = {
        "score" : 1,
        "final_result_rhs_tex" : [
            "3", "(0.8)", "(0.2)", "^2", "=", "0.096",
        ],
        "default_bool" : False,
        "default_p" : "0.2",
        "default_q" : "0.8",
    }
