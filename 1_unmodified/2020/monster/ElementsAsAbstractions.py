# ==============================================================================
# Scene:      ElementsAsAbstractions
# Source:     videos/_2020/monster.py (lines 1764-2041)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ElementsAsAbstractions.py ElementsAsAbstractions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_snowflake(height=2):
    snowflake = SVGMobject("snowflake")
    snowflake.set_fill(GREY_C, 1)
    snowflake.set_gloss(1)
    snowflake.set_shadow(0.2)
    snowflake.set_stroke(WHITE, 1)
    snowflake.set_height(height)
    return snowflake


def get_rot_icon(degrees, mobject, mini_mob_height=1.25):
    mini_mob = mobject.copy()
    temp_height = 1.75
    mini_mob.set_height(temp_height)
    mini_mob.set_stroke(width=0)
    mini_mob.center()
    angle = min(degrees * DEGREES, 170 * DEGREES)
    arc1 = Arrow(
        RIGHT, rotate_vector(RIGHT, angle),
        path_arc=angle,
        buff=0
    )
    arc2 = arc1.copy().rotate(PI, about_point=ORIGIN)
    label = Integer(degrees, unit="^\\circ")
    label.set_height(0.25)
    half_vect = rotate_vector(RIGHT, angle / 2)
    label.next_to(half_vect, half_vect, buff=MED_SMALL_BUFF)
    icon = VGroup(mini_mob, arc1, arc2, label)
    icon.scale(mini_mob_height / temp_height)
    return icon


def get_flip_icon(angle, mobject, opacity=0.75, mini_mob_height=1.25):
    mini_mob = mobject.copy()
    mini_mob.set_stroke(width=0)
    mini_mob.set_fill(opacity=opacity)
    mini_mob.set_height(mini_mob_height)
    mini_mob.center()
    sym_line = DashedLine(LEFT, RIGHT)
    sym_line.set_stroke(WHITE, 2)
    sym_line.set_width(1.2 * mini_mob_height)
    sym_line.rotate(angle)
    sym_line.move_to(mini_mob)
    back_line = sym_line.copy()
    back_line.set_stroke(BLACK, 5)
    return VGroup(mini_mob, back_line, sym_line)


class ElementsAsAbstractions(TeacherStudentsScene):
    def construct(self):
        # Three
        self.teacher_says("Three")
        self.wait()

        s_copies = self.students.copy()
        s_copies.scale(0.3)
        bubble = self.students[0].get_bubble(
            s_copies,
            width=5,
            height=4,
        )
        self.play(
            self.students[0].change, "pondering",
            Write(bubble),
            FadeIn(bubble.content, lag_ratio=0.3),
        )
        self.wait(2)

        numeral = Integer(3)
        numeral.replace(bubble.content, dim_to_match=1)
        bubble.content.generate_target()
        for pi in bubble.content.target:
            pi.change("horrified")
            pi.shift(UP)
            pi.set_opacity(0)

        self.play(MoveToTarget(bubble.content))
        self.remove(bubble.content)
        self.play(
            Write(numeral),
            self.students[0].change, "happy", numeral,
        )
        self.look_at(numeral)
        self.wait(2)

        # Element of D6
        self.camera.light_source.set_x(0)
        snowflake = get_snowflake()
        rot_icon = get_rot_icon(60, snowflake)
        inclusion = VGroup(
            rot_icon,
            OldTex("\\in").scale(2),
            OldTex("D_6").scale(2),
        )
        inclusion.arrange(RIGHT)
        inclusion.next_to(self.hold_up_spot, UL, MED_LARGE_BUFF)

        self.play(
            LaggedStart(
                FadeOut(self.teacher.bubble),
                FadeOut(self.teacher.bubble.content),
                FadeOut(bubble),
                FadeOut(numeral),
                FadeIn(inclusion, DOWN),
            ),
            self.teacher.change, "raise_right_hand",
        )
        self.look_at(inclusion)
        self.wait()
        self.play(Rotate(rot_icon[0], 60 * DEGREES))
        self.wait()

        rot_icon.generate_target()
        rot_icon.target.to_corner(UL)
        r_sym = OldTex("r").scale(2)
        r_sym.move_to(rot_icon, RIGHT)

        self.look_at(
            rot_icon.target,
            added_anims=[MoveToTarget(rot_icon)],
        )
        self.look_at(
            r_sym,
            added_anims=[Write(r_sym)]
        )
        self.play_all_student_changes(
            "confused",
            look_at=r_sym,
        )
        self.wait(2)
        inclusion.remove(rot_icon)
        inclusion.add(r_sym)

        # Back to 3
        numeral.move_to(self.hold_up_spot, DOWN)

        self.play(
            inclusion.to_edge, LEFT,
            inclusion.set_color, GREY_B,
            Write(numeral),
            self.change_students(*3 * ["pondering"], look_at=numeral),
            self.teacher.change, "tease", numeral,
        )
        self.wait(2)

        # Operations
        add = OldTex("3", "+", "5", "=", "8")
        mult = OldTex("3", "\\cdot", "5", "=", "15")
        ops = VGroup(add, mult)
        ops.match_height(numeral)
        ops.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        ops.to_corner(UR, buff=LARGE_BUFF)

        self.remove(numeral)
        self.play(
            LaggedStart(*[
                TransformFromCopy(numeral[0], form[0])
                for form in ops
            ]),
            *[
                ApplyMethod(pi.look_at, ops)
                for pi in self.pi_creatures
            ]
        )
        self.play(
            LaggedStart(*[
                Write(form[1:])
                for form in ops
            ])
        )
        self.wait(3)

        # Literal forms
        quincunx = VGroup(*[Dot() for x in range(5)])
        quincunx[:4].arrange_in_grid()
        quincunx.space_out_submobjects(0.7)
        triplet = VGroup(quincunx[0], quincunx[3], quincunx[4]).copy()
        triplet.set_color(BLUE)
        octet = VGroup(*[Dot() for x in range(9)])
        octet.arrange_in_grid(3, 3)
        octet.remove(octet[4])
        octet.space_out_submobjects(0.5)

        sum_dots = VGroup(triplet, quincunx, octet)
        for sd, sym in zip(sum_dots, ops[0][0::2]):
            sd.move_to(sym)

        octet.shift(SMALL_BUFF * RIGHT)

        quincunx_trip = VGroup(*[quincunx.copy() for x in range(3)])
        quincunx_trip.arrange(RIGHT, buff=MED_LARGE_BUFF)
        for quin in quincunx_trip:
            rect = SurroundingRectangle(quin)
            rect.set_stroke(BLUE, 3)
            quin.add(rect)
        quincunx_trip.move_to(ops[1][2], RIGHT)

        fifteen = VGroup(*[Dot() for x in range(15)])
        fifteen.arrange_in_grid(3, 5)
        fifteen.space_out_submobjects(0.5)
        fifteen.move_to(ops[1][4], LEFT)

        mult_dots = VGroup(quincunx_trip, fifteen)

        self.play(
            FadeOut(ops[0][0::2], UP),
            FadeIn(sum_dots, DOWN),
        )
        self.play(
            FadeOut(VGroup(*ops[1][:3], ops[1][4]), UP),
            FadeIn(mult_dots, DOWN),
            self.change_students(*3 * ["erm"], look_at=mult_dots),
        )
        self.wait(4)
        self.play(
            LaggedStart(*[
                ApplyMethod(mob.scale, 0, remover=True)
                for mob in [*sum_dots, *mult_dots]
            ]),
            LaggedStart(*[
                FadeIn(mob)
                for mob in [*ops[0][0::2], *ops[1][:3], ops[1][4]]
            ]),
            self.change_students(*3 * ["happy"]),
        )
        self.wait(2)

        # Show group sum
        flip_icon = get_flip_icon(0, snowflake)
        rhs_icon = get_flip_icon(30 * DEGREES, snowflake)
        rot_icon.generate_target()

        group_prod = VGroup(
            rot_icon.target,
            OldTex("\\times").scale(2),
            flip_icon,
            OldTex("=").scale(2),
            rhs_icon
        )
        group_prod.set_gloss(0)
        for icon in group_prod[::2]:
            icon[0].set_stroke(width=0)
            icon[0].set_fill(GREY_A, 1)
        group_prod.arrange(RIGHT)
        group_prod.to_edge(UP)

        self.play(
            FadeOut(ops, RIGHT),
            FadeOut(inclusion, LEFT),
            MoveToTarget(rot_icon),
            LaggedStartMap(FadeIn, group_prod[1:], lag_ratio=0.5, run_time=2),
            self.change_students(
                "sassy", "erm", "confused",
                look_at=group_prod,
            ),
            self.teacher.change, "raise_right_hand",
        )
        group_prod.replace_submobject(0, rot_icon)
        self.add(group_prod)
        self.wait(2)

        # Show successive actions
        snowflake = get_snowflake()
        snowflake.move_to(0.5 * UP)
        snowflake.match_x(group_prod[1])
        alt_flake = snowflake.copy()
        alt_flake.match_x(rhs_icon)

        self.play(
            TransformFromCopy(rot_icon[0], snowflake)
        )

        def get_numbers(flake):
            vect = 1.2 * (flake.get_top() - flake.get_center())
            points = VGroup(*[
                VectorizedPoint(rotate_vector(vect, angle))
                for angle in np.arange(0, TAU, TAU / 6)
            ])
            points.move_to(flake)
            numbers = VGroup(*[Integer(i + 1) for i in range(6)])
            numbers.scale(0.5)
            for num, point in zip(numbers, points):
                num.point = point
                num.add_updater(lambda m: m.move_to(m.point))
            flake.add(points)
            return numbers

        sn_nums = get_numbers(snowflake)
        as_nums = get_numbers(alt_flake)

        self.play(
            FadeIn(sn_nums, lag_ratio=0.1),
            self.change_students(*3 * ["pondering"], look_at=snowflake)
        )
        self.add(*sn_nums)
        self.play(
            Rotate(snowflake, PI, RIGHT),
            ShowCreationThenFadeAround(flip_icon),
        )
        self.wait()
        self.play(
            Rotate(snowflake, 60 * DEGREES),
            ShowCreationThenFadeAround(rot_icon),
        )
        self.wait()

        self.look_at(
            alt_flake,
            added_anims=[TransformFromCopy(rhs_icon[0], alt_flake)]
        )
        self.play(FadeIn(as_nums, lag_ratio=0.1))
        self.add(*as_nums)

        line = rhs_icon.submobjects[-1].copy()
        line.scale(2)
        line.set_stroke(YELLOW, 3)
        line.move_to(alt_flake)
        self.play(ShowCreation(line))
        self.play(
            Rotate(alt_flake, PI, axis=line.get_vector())
        )
        self.play(
            FadeOut(line),
            self.change_students(*3 * ["thinking"])
        )
        self.wait(3)
