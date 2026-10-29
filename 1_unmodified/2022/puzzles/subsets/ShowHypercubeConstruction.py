# ==============================================================================
# Scene:      ShowHypercubeConstruction
# Source:     videos/_2022/puzzles/subsets.py (lines 1548-1666)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowHypercubeConstruction.py ShowHypercubeConstruction -w -m --fps 15
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


class ShowHypercubeConstruction(InteractiveScene):
    def construct(self):
        # Intro
        v1 = np.array([1.5, 1.5, 0.5])
        v2 = np.array([-2.5, 0.5, 1.5])
        vects = 1.5 * np.array([
            RIGHT, UP, OUT,
            v1, v2,
            1.5 * (v1 + 2 * OUT), 2 * (v2 + 2 * UP),
            5 * v1, 5 * v2,
        ])
        colors = [GREEN_D, TEAL, BLUE_D, RED, PINK] * 2
        curr_sets = VGroup(get_set_tex([]))
        lines = VGroup()
        frame = self.camera.frame

        self.play(Write(curr_sets))
        self.wait()

        # Grow new sets
        indices = list(range(1, 10))
        for n, vect, color in zip(indices, vects, colors):
            new_sets = VGroup(*(
                get_set_tex([*st.values, n])
                for st in curr_sets
            ))
            for ns in new_sets:
                for value, c in zip(indices, colors):
                    if value in ns.values:
                        get_part_by_value(ns, value).set_color(c)
                ns.set_backstroke()
                if n >= 3:
                    ns.rotate(70 * DEGREES, RIGHT)
            curr_set_copies = curr_sets.copy()
            curr_sets.generate_target()
            new_lines = VGroup()
            line_copies = VGroup()
            for ns, cst, csc in zip(new_sets, curr_sets.target, curr_set_copies):
                ns.move_to(cst)
                ns.shift(vect)
                cst.shift(-vect)
                csc.move_to(ns)
                new_lines.add(Line(
                    cst.get_center(), ns.get_center(),
                    # buff=MED_SMALL_BUFF + ns.length_over_dim(np.argmax(vect)),
                    buff=MED_SMALL_BUFF + ns.get_height(),
                    stroke_color=color,
                    stroke_width=2,
                ))
            line_copies = lines.copy()
            diff = new_sets[0].get_width() - curr_sets[0].get_width()
            for line in line_copies:
                if abs(line.get_vector()[0]) > 1e-2:
                    line.set_width(line.get_width() - diff)
                line.set_stroke(width=(1, 5, 5, 5, 1))
            lines.generate_target()
            line_copies.shift(vect)
            lines.target.shift(-vect)
            anims = [
                MoveToTarget(curr_sets),
                TransformFromCopy(curr_sets, curr_set_copies),
                MoveToTarget(lines),
                TransformFromCopy(lines, line_copies),
                *map(GrowFromCenter, new_lines),
            ]
            if n == 3:
                anims.append(ApplyMethod(
                    frame.reorient, 10, 70,
                    run_time=2,
                ))
                for st in [*curr_set_copies, *curr_sets.target]:
                    st.rotate(70 * DEGREES, RIGHT)
                frame.add_updater(lambda m, dt: frame.increment_theta(0.01 * dt))
            if n >= 4:
                anims.append(frame.animate.scale(1.5).reorient(-10, 70).move_to(2 * IN))
            self.play(*anims)
            self.remove(curr_set_copies)
            self.play(*(
                set_tex_transform(csc, ns)
                for csc, ns in zip(curr_set_copies, new_sets)
            ))
            self.wait()

            curr_sets.set_submobjects([*curr_sets, *new_sets])
            curr_sets.set_backstroke()
            lines.set_submobjects([*lines, *line_copies, *new_lines])
            self.add(lines, curr_sets)
            if n == 3:
                for i in range(1, 4):
                    self.highlight_direction(curr_sets, lines, i)
        self.wait(5)

    def styling(self):
        # Style (To insert above)
        everything = VGroup(*curr_sets.family_members_with_points(), *lines.family_members_with_points())
        everything.sort(lambda p: -get_norm(p - self.frame.get_implied_camera_location()))
        self.add(*everything)
        for line in lines.family_members_with_points():
            line.insert_n_curves(20)
            line.set_stroke(width=(1, 7, 7, 7, 1))

        curr_sets.set_fill(border_width=1.5)

    def highlight_direction(self, set_texs, lines, index):
        anims = []
        for line in lines:
            if np.argmax(line.get_vector()) == index - 1:
                anims.append(ShowCreation(line))
        self.play(LaggedStart(*anims, lag_ratio=0.25, run_time=1))
        anims = []
        for st in set_texs:
            if index in st.values:
                part = get_part_by_value(st, index)
                outline = part.family_members_with_points()[0].copy()
                outline.set_fill(opacity=0)
                outline.set_stroke(YELLOW, 5)
                anims.append(VShowPassingFlash(outline, time_width=2))
        self.play(LaggedStart(*anims, lag_ratio=0.1, run_time=2))
        self.wait()
