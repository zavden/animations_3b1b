# ==============================================================================
# Scene:      AltThumbnail
# Source:     videos/_2022/puzzles/subsets.py (lines 5489-5550)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltThumbnail.py AltThumbnail -w -m --fps 15
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


def get_subsets(full_set):
    return list(it.chain(*(
        it.combinations(full_set, k)
        for k in range(len(full_set) + 1)
    )))


class AltThumbnail(InteractiveScene):
    def construct(self):
        # Organize sets
        subsets = [
            subset
            for subset in get_subsets(range(1, 10))
            if sum(subset) % 5 == 0
        ]
        n_shown = 28
        shown_sets = VGroup(*(get_set_tex(ss) for ss in subsets[:n_shown]))
        shown_sets.arrange(DOWN, aligned_edge=LEFT)
        shown_sets[n_shown // 2:].next_to(shown_sets[:n_shown // 2], RIGHT, MED_LARGE_BUFF)
        shown_sets.refresh_bounding_box()
        shown_sets.set_height(FRAME_HEIGHT - 1)
        shown_sets.center().to_edge(LEFT)

        dots = OldTex("\\vdots")
        dots.replace(shown_sets[-1], dim_to_match=1)
        shown_sets.replace_submobject(-1, dots)

        self.add(shown_sets)

        # Phrase
        text = Text("Use complex numbers", font_size=90)
        text.set_color(YELLOW)
        text.set_x(2)
        text.to_edge(UP)
        text.set_backstroke(width=20)

        subtext = Text("...of course")
        subtext.next_to(text, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)

        self.add(text)
        self.add(subtext)

        # Unit circle
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            background_line_style=dict(stroke_color=BLUE_D, stroke_width=3),
            faded_line_ratio=1,
            axis_config=dict(stroke_color=GREY_B),
        )
        plane.set_width(9.5)
        plane.match_x(text)
        plane.to_edge(UP, buff=0)

        circle = Circle(radius=get_norm(plane.n2p(1) - plane.n2p(0)))
        circle.move_to(plane.n2p(0))
        circle.set_stroke(WHITE, 2)

        points = [plane.n2p(np.exp(complex(0, angle))) for angle in np.arange(0, TAU, TAU / 5)]
        glow_dots = GlowDots(points, radius=0.5)
        dots = DotCloud(points, radius=0.05, color=YELLOW)
        lines = VGroup(*(Line(plane.n2p(0), point) for point in points))
        lines.set_stroke(YELLOW, 4)

        self.add(plane)
        self.add(circle)
        self.add(lines)
        self.add(dots)
        self.add(glow_dots)
        self.add(text, subtext)
