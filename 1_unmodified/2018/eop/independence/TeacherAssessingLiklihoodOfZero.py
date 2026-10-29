# ==============================================================================
# Scene:      TeacherAssessingLiklihoodOfZero
# Source:     videos/_2018/eop/independence.py (lines 1973-2042)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TeacherAssessingLiklihoodOfZero.py TeacherAssessingLiklihoodOfZero -w -m --fps 15
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


class TeacherAssessingLiklihoodOfZero(TeacherStudentsScene):
    def construct(self):
        self.add_title()
        self.fade_other_students()
        self.show_independence_probability()
        self.teacher_reacts()

    def add_title(self):
        title = OldTex("P(", "\\text{Correct}", ")", "=", "0.65")
        title.to_edge(UP)
        title.set_color_by_tex("Correct", GREEN)
        q_mark = OldTex("?")
        q_mark.next_to(title[-2], UP, SMALL_BUFF)
        title.add(q_mark)

        self.add(title)
        self.title = title

    def fade_other_students(self):
        for student in self.students[0::2]:
            student.fade(0.7)
            self.pi_creatures.remove(student)

    def show_independence_probability(self):
        prob = get_probability_of_slot_group(3*[False])
        rhs = OldTex("=", "(0.35)", "^3", "\\approx 4.3\\%")
        rhs.set_color_by_tex("0.35", RED)
        rhs.next_to(prob, RIGHT)
        prob.add(rhs)
        prob.next_to(self.teacher, UP+LEFT)
        words = OldTexText("Assuming independence")
        words.next_to(prob, UP)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(words),
            Write(prob)
        )
        self.wait()

        self.ind_group = VGroup(prob, words)

    def teacher_reacts(self):
        ind_group = self.ind_group
        box = SurroundingRectangle(ind_group)
        box.set_stroke(WHITE, 0)
        ind_group.add(box)
        ind_group.generate_target()
        ind_group.target.scale(0.7)
        ind_group.target.to_corner(UP+RIGHT, MED_SMALL_BUFF)
        ind_group.target[-1].set_stroke(WHITE, 2)

        randy = self.students[1]

        self.teacher_says(
            "Highly unlikely",
            target_mode = "sassy",
            added_anims = [MoveToTarget(ind_group)],
            run_time = 2,
        )
        self.play(randy.change, "sad")
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(
                self.teacher, target_mode = "guilty",
            ),
            PiCreatureSays(randy, "Wait!", target_mode = "surprised"),
            run_time = 1
        )
        self.wait(1)
