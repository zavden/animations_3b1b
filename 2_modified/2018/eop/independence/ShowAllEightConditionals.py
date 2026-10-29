# ==============================================================================
# Scene:      ShowAllEightConditionals
# Source:     videos/_2018/eop/independence.py (lines 1472-1534)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowAllEightConditionals.py ShowAllEightConditionals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_slot_group: bool_list converted to a list before padding (tuple + list TypeError)
# ==============================================================================

from manim_imports_ext import *

def get_slot_group(
    bool_list, 
    buff = MED_LARGE_BUFF, 
    include_qs = True,
    min_bool_list_len = 3,
    ):
    if len(bool_list) < min_bool_list_len:
        # CHANGE: bool_list can be a tuple here; convert to list before padding it (Python 3 does not mix tuple and list)
        bool_list = list(bool_list) + [None]*(min_bool_list_len - len(bool_list))
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


class ShowAllEightConditionals(Scene):
    def construct(self):
        self.show_all_conditionals()
        self.suggest_independence()

    def show_all_conditionals(self):
        equations = VGroup()
        filler_tex = "Filler"
        for bool_list in it.product(*[[True, False]]*3):
            equation = OldTex(
                "P(", filler_tex, ")", "=",
                "P(", filler_tex, ")",
                "P(", filler_tex, "|", filler_tex, ")",
                "P(", filler_tex, "|", filler_tex, ")",
            )
            sub_bool_lists = [
                bool_list[:n] for n in (3, 1, 2, 1, 3, 2)
            ]
            parts = equation.get_parts_by_tex(filler_tex)
            for part, sub_list in zip(parts, sub_bool_lists):
                slot_group = get_slot_group(
                    sub_list, 
                    buff = SMALL_BUFF,
                    include_qs = False
                )
                slot_group.replace(part, dim_to_match = 0)
                index = equation.index_of_part(part)
                equation.submobjects[index] = slot_group
            equations.add(equation)
        equations.arrange(DOWN)

        rect = SurroundingRectangle(
            VGroup(*equations[0][7:], *equations[-1][7:]),
            buff = SMALL_BUFF
        )
        rect.shift(0.5*SMALL_BUFF*RIGHT)

        self.play(LaggedStartMap(
            FadeIn, equations,
            run_time = 5,
            lag_ratio = 0.3
        ))
        self.wait()
        self.play(ShowCreation(rect, run_time = 2))
        self.play(FadeOut(rect))
        self.wait()

    def suggest_independence(self):
        full_screen_rect = FullScreenFadeRectangle()
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)


        self.play(
            FadeIn(full_screen_rect),
            FadeIn(randy)
        )
        self.play(PiCreatureSays(
            randy, "Let's just assume \\\\ independence.",
            target_mode = "shruggie"
        ))
        self.play(Blink(randy))
        self.wait()
