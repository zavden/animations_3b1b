# ==============================================================================
# Scene:      RotationalSum
# Source:     videos/_2022/puzzles/subsets.py (lines 5199-5314)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationalSum.py RotationalSum -w -m --fps 15
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


class RotationalSum(InteractiveScene):
    n_iterations = 40

    def construct(self):
        # Intro
        outer_r = 3
        inner_r = 2.0
        circle = Circle(radius=outer_r)
        circle.set_stroke(GREY_B, 2)
        points = outer_r * compass_directions(5)
        values = VGroup(*(
            Integer(0, edge_to_fix=ORIGIN).move_to(point)
            for point in points
        ))
        values[0].edge_to_fix = LEFT
        rects = VGroup(*(BackgroundRectangle(v) for v in values))
        rects.set_fill(BLACK, 1)

        def update_rects(rects):
            for rect, value in zip(rects, values):
                rect.replace(value, stretch=True)
                rect.set_width(value.get_width() + SMALL_BUFF)

        rects.add_updater(update_rects)

        def update_values(values):
            for v in values:
                v.set_max_width(1, about_edge=v.edge_to_fix)

        values.add_updater(update_values)

        values[0].increment_value()

        self.add(circle)
        self.add(rects, values)

        # Add labels
        labels = VGroup(*(
            OldTexText(f"sum $\\equiv$ {n}\\\\mod 5", font_size=30)
            for n in range(5)
        ))
        colors = [YELLOW, *color_gradient([BLUE_B, BLUE_D], 4)]
        for label, rect, color in zip(labels, rects, colors):
            label.set_fill(color)
            label.add_background_rectangle()
            # label.next_to(rect, DOWN, SMALL_BUFF)
            label.next_to(rect, normalize(rect.get_center()), SMALL_BUFF)
        labels[0].next_to(rects[0], DR, SMALL_BUFF)

        self.add(labels)

        # Corner set
        set_tex = get_set_tex([])
        set_tex.scale(0.75)
        set_tex.to_corner(UL)
        set_tex.shift(LEFT)
        self.camera.frame.move_to(LEFT)

        self.add(set_tex)

        # Iterative all
        for n in range(1, self.n_iterations + 1):
            value_copies = values.copy()
            to_add = [0] * 5
            for i, vc in enumerate(value_copies):
                new_i = (i + n) % 5
                vc.move_to((inner_r / outer_r) * points[new_i])
                to_add[new_i] = vc.get_value()
                vc.target = VectorizedPoint(values[new_i].get_center())
                vc.target.set_opacity(0)

            reduced_n = n % 5
            path_arc = min(reduced_n * TAU / 5, TAU / 3)

            rot_label = Text(f"Add {n}", font_size=30)
            arcs = VGroup(Arc(0, path_arc), Arc(TAU / 2, path_arc))
            for arc in arcs:
                arc.add_tip(width=0.1, length=0.1)
            if reduced_n == 0:
                arcs.set_opacity(0)

            new_set_tex = get_set_tex([*set_tex.values, n])
            new_set_tex.match_height(set_tex)
            new_set_tex.move_to(set_tex, LEFT)

            self.remove(set_tex)
            self.play(
                TransformFromCopy(
                    values, value_copies,
                    path_arc=-path_arc
                ),
                FadeIn(rot_label),
                TransformMatchingTex(
                    set_tex, new_set_tex,
                    fade_transform_mismatches=(len(set_tex) == len(new_set_tex)),
                    remover=True,
                ),
                *map(ShowCreation, arcs)
            )
            set_tex = new_set_tex
            self.add(set_tex)

            self.play(*map(FadeOut, [rot_label, *arcs]))
            self.play(
                *(
                    ChangeDecimalToValue(
                        v, v.get_value() + ta, time_span=(0.5, 1),
                    )
                    for v, ta in zip(values, to_add)
                ),
                *(
                    MoveToTarget(vc, remover=True)
                    for v, vc in zip(values, value_copies)
                ),
            )
            self.wait()
