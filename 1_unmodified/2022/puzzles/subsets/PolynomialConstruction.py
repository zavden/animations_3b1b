# ==============================================================================
# Scene:      PolynomialConstruction
# Source:     videos/_2022/puzzles/subsets.py (lines 1744-1846)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PolynomialConstruction.py PolynomialConstruction -w -m --fps 15
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


class PolynomialConstruction(InteractiveScene):
    def construct(self):
        # (1 + x)
        set_group = VGroup(
            get_set_tex([]),
            get_set_tex([1]),
        )
        set_group.scale(0.5)
        curr_poly = Tex("(1 + x^1)")
        curr_poly[0].set_opacity(0)
        curr_poly[-1].set_opacity(0)

        for st, sym in zip(set_group, curr_poly[1::2]):
            st.next_to(sym, DOWN, MED_LARGE_BUFF)

        self.add(curr_poly, set_group)

        # Expand via subset iteration process
        for n in range(2, 8):
            cp_l, cp_r = curr_poly.replicate(2)
            sg_l, sg_r = set_group.replicate(2)
            plus = Tex("+")
            cp_l.next_to(plus, LEFT, LARGE_BUFF)
            cp_r.next_to(plus, RIGHT, LARGE_BUFF)
            sg_l.match_x(cp_l)
            sg_r.match_x(cp_r)

            self.remove(curr_poly, set_group)
            added_anims = []
            if n == 5:
                added_anims.append(self.camera.frame.animate.set_height(10))
            if n >= 6:
                added_anims.append(self.camera.frame.animate.scale(1.4))
                VGroup(cp_l, sg_l).shift(LEFT)
                VGroup(cp_r, sg_r).shift(RIGHT)
            self.play(
                TransformFromCopy(curr_poly, cp_l),
                TransformFromCopy(curr_poly, cp_r),
                TransformFromCopy(set_group, sg_l),
                TransformFromCopy(set_group, sg_r),
                *added_anims
            )
            self.wait()
            new_term = Tex(f"x^{n}")
            new_poly = Tex("".join([
                f"\\left(1 + x^{k}\\right)"
                for k in range(1, n + 1)
            ]))
            new_term.next_to(cp_r, LEFT, SMALL_BUFF)
            new_term.align_to(cp_r.family_members_with_points()[1], DOWN)
            new_sets = VGroup(*(
                get_set_tex([*st.values, n])
                for st in sg_r
            ))
            anims = [Write(new_term), Write(plus)]
            for ns, s in zip(new_sets, sg_r):
                ns.match_height(s)
            new_sets.arrange_in_grid(
                n_cols=2**int(np.ceil(np.log2(len(new_sets)) / 2))
            )
            new_sets.move_to(sg_r)
            for ns, s in zip(new_sets, sg_r):
                anims.append(set_tex_transform(s, ns))
            if n == 2:
                anims.append(cp_r.animate.set_opacity(1))

            self.remove(sg_r)
            self.play(*anims)
            self.wait()

            new_set_group = VGroup(*sg_l, *new_sets)
            new_set_group.generate_target()
            new_set_group.target.arrange_in_grid(
                n_cols=2**int(np.ceil(np.log2(len(new_set_group)) / 2))
            )
            new_set_group.target.next_to(new_poly, DOWN, MED_LARGE_BUFF)

            group = VGroup(cp_l, cp_r, plus, new_term)
            self.play(group.animate.shift(2 * UP))
            group_copy = group.copy()

            self.add(group_copy)
            self.play(
                LaggedStart(
                    Transform(
                        cp_l, new_poly[:-6].copy().set_opacity(0),
                        path_arc=30 * DEGREES,
                        remover=True,
                    ),
                    ReplacementTransform(new_term, new_poly[-3:-1]),
                    ReplacementTransform(cp_r, new_poly[:-6], path_arc=30 * DEGREES),
                    ReplacementTransform(plus, new_poly[-4], path_arc=45 * DEGREES),
                    Write(new_poly[-6:-4]),
                    Write(new_poly[-1]),
                ),
                MoveToTarget(new_set_group),
                run_time=2,
            )
            self.add(new_poly)
            set_group = new_set_group
            curr_poly = new_poly
            self.play(FadeOut(group_copy))
            self.wait()
