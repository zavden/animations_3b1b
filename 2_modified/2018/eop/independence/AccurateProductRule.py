# ==============================================================================
# Scene:      AccurateProductRule
# Source:     videos/_2018/eop/independence.py (lines 1301-1470)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AccurateProductRule.py AccurateProductRule -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cube replaced by CairoCube (GL Cube is a surface group without set_fill/stretch_to_fit)
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


class AccurateProductRule(SampleSpaceScene, ThreeDScene):
    def construct(self):
        self.setup_terms()
        self.add_sample_space()
        self.wait()
        self.show_first_division()
        self.show_second_division()
        self.move_to_third_dimension()
        self.show_final_probability()
        self.show_confusion()

    def setup_terms(self):
        filler_tex = "Filler"
        lhs = OldTex("P(", filler_tex, ")", "=")
        p1 = OldTex("P(", filler_tex, ")")
        p2 = OldTex("P(", filler_tex, "|", filler_tex, ")")
        p3 = OldTex("P(", filler_tex, "|", filler_tex, ")")
        terms = VGroup(lhs, p1, p2, p3)
        terms.arrange(RIGHT, buff = SMALL_BUFF)
        terms.to_edge(UP, buff = LARGE_BUFF)

        kwargs = {"buff" : SMALL_BUFF, "include_qs" : False}
        slot_group_lists = [
            [get_slot_group([True, True, False], **kwargs)],
            [get_slot_group([True], **kwargs)],
            [
                get_slot_group([True, True], **kwargs),
                get_slot_group([True], **kwargs),
            ],
            [
                get_slot_group([True, True, False], **kwargs),
                get_slot_group([True, True], **kwargs),
            ],
        ]
        for term, slot_group_list in zip(terms, slot_group_lists):
            parts = term.get_parts_by_tex(filler_tex)
            for part, slot_group in zip(parts, slot_group_list):
                slot_group.replace(part, dim_to_match = 0)
                term.submobjects[term.index_of_part(part)] = slot_group
        # terms[2][1].content[0].set_fill(BLACK, 0)
        # VGroup(*terms[3][1].content[:2]).set_fill(BLACK, 0)

        value_texs = ["0.8", ">0.8", "<0.2"]
        for term, tex in zip(terms[1:], value_texs):
            term.value = OldTex(tex)
            term.value.next_to(term, UP)

        self.terms = terms
        self.add(terms[0])

    def add_sample_space(self):
        SampleSpaceScene.add_sample_space(self, height = 4, width = 5)
        self.sample_space.to_edge(DOWN)

    def show_first_division(self):
        space = self.sample_space
        space.divide_horizontally(
            [0.8], colors = [GREEN_E, RED_E]
        )
        space.horizontal_parts.fade(0.1)
        top_label = self.terms[1].copy()
        bottom_label = top_label.copy()
        slot_group = get_slot_group([False], buff = SMALL_BUFF, include_qs = False)
        slot_group.replace(bottom_label[1])
        Transform(bottom_label[1], slot_group).update(1)
        braces_and_labels = space.get_side_braces_and_labels(
            [top_label, bottom_label]
        )

        self.play(
            FadeIn(space.horizontal_parts),
            FadeIn(braces_and_labels)
        )
        self.play(ReplacementTransform(
            top_label.copy(), self.terms[1]
        ))
        self.wait()
        self.play(Write(self.terms[1].value))
        self.wait()

        space.add(braces_and_labels)
        self.top_part = space.horizontal_parts[0]

    def show_second_division(self):
        space = self.sample_space
        top_part = self.top_part
        green_red_mix = average_color(GREEN_E, RED_E)
        top_part.divide_vertically(
            [0.9], colors = [GREEN_E, green_red_mix]
        )
        label = self.terms[2].deepcopy()
        braces_and_labels = top_part.get_top_braces_and_labels(
            labels = [label]
        )

        self.play(
            FadeIn(top_part.vertical_parts),
            FadeIn(braces_and_labels)
        )
        self.play(ReplacementTransform(
            label.copy(), self.terms[2]
        ))
        self.wait()
        self.play(Write(self.terms[2].value))
        self.wait()

        space.add(braces_and_labels)
        self.top_left_part = top_part.vertical_parts[0]

    def move_to_third_dimension(self):
        space = self.sample_space
        part = self.top_left_part
        cubes = VGroup(
            # CHANGE: GL Cube is a surface group without set_fill/stretch_to_fit_*; use the VMobject-face cube from cairo_compat (Cairo behaviour)
            CairoCube(fill_color = RED_E),
            CairoCube(fill_color = GREEN_E),
        )
        cubes.set_fill(opacity = 0)
        cubes.stretch_to_fit_width(part.get_width())
        cubes.stretch_to_fit_height(part.get_height())
        cubes[1].move_to(part, IN)
        cubes[0].stretch(0.2, 2)
        cubes[0].move_to(cubes[1].get_edge_center(OUT), IN)
        space.add(cubes)

        self.play(
            space.rotate, 0.9*np.pi/2, LEFT,
            space.rotate, np.pi/12, UP,
            space.to_corner, DOWN+RIGHT, LARGE_BUFF
        )
        space.remove(cubes)
        self.play(
            cubes[0].set_fill, None, 1,
            cubes[0].set_stroke, WHITE, 1,
            cubes[1].set_fill, None, 0.5,
            cubes[1].set_stroke, WHITE, 1,
        )
        self.wait()

        self.cubes = cubes

    def show_final_probability(self):
        cube = self.cubes[0]
        face = cube[2]
        points = face.get_anchors()
        line = Line(points[2], points[3])
        line.set_stroke(YELLOW, 8)
        brace = Brace(line, LEFT)
        label = self.terms[3].copy()
        label.next_to(brace, LEFT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(label),
        )
        self.wait()
        self.play(ReplacementTransform(
            label.copy(), self.terms[3]
        ))
        self.wait()

    def show_confusion(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)

        self.play(FadeIn(randy))
        self.play(randy.change, "confused", self.terms)
        self.play(randy.look_at, self.cubes)
        self.play(Blink(randy))
        self.play(randy.look_at, self.terms)
        self.wait()
