# ==============================================================================
# Scene:      MonstrousMoonshine
# Source:     videos/_2020/monster.py (lines 4300-4479)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MonstrousMoonshine.py MonstrousMoonshine -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - monster.svg (free replacement) has different point indices for the eyes: _eye_points finds them by geometry
# ==============================================================================

from manim_imports_ext import *

def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


def _eye_points(mob):
    # CHANGE: monster.svg is a free replacement and its eyes are not at points 498:528 / 582:612; they are found as the two small subpaths at the top
    pts = mob.get_points()
    ends = mob.get_subpath_end_indices_from_points(pts)
    starts = [0, *(ends[:-1] + 2)]
    cy = mob.get_center()[1]
    eyes = [
        pts[a:b + 1] for a, b in zip(starts, ends)
        if np.ptp(pts[a:b + 1, 0]) < 0.1 * mob.get_width() and pts[a:b + 1, 1].mean() > cy
    ]
    eyes.sort(key=lambda p: p[:, 0].mean())
    return eyes[:2]


def blink_monster(monster):
    monster.generate_target()
    left_eye_points, right_eye_points = _eye_points(monster.target[0])
    for points in left_eye_points, right_eye_points:
        points[:, 1] = points[0, 1]
    return MoveToTarget(monster, rate_func=squish_rate_func(there_and_back, 0.4, 0.6))


def get_named_image(name, height=3):
    image = ImageMobject(name)
    image.set_height(height)

    name = OldTexText(name)
    name.match_width(image)
    name.next_to(image, DOWN)
    group = Group(image, name)
    return group


class MonstrousMoonshine(Scene):
    def construct(self):
        # Time line
        decades = list(range(1970, 2030, 10))
        timeline = NumberLine(
            (decades[0], decades[-1], 1),
            big_tick_numbers=decades,
            tick_size=0.075,
            width=13,
        )
        timeline.add_numbers(decades, group_with_commas=False)
        timeline.move_to(DOWN)
        self.add(timeline)

        triangle = Triangle()
        triangle.rotate(PI)
        triangle.set_height(0.25)
        triangle.set_fill(BLUE_C, 1)
        triangle.set_stroke(WHITE, 0)
        triangle.move_to(timeline.n2p(2020), DOWN)
        self.add(triangle)

        self.play(
            triangle.move_to, timeline.n2p(1978), DOWN,
            run_time=3,
        )

        # McKay
        mckay = get_named_image("John McKay")
        mckay[0].flip()
        mckay.next_to(triangle, UP)

        self.play(FadeIn(mckay, DOWN))
        self.wait()

        theories = VGroup(
            OldTexText("Finite group theory"),
            OldTexText("Galois theory"),
        )
        theories.arrange(RIGHT, buff=1.5)
        theories.next_to(mckay, RIGHT, LARGE_BUFF)
        theories_line, theories_arrow = [
            func(
                *[theory.get_top() for theory in theories],
                path_arc=-90 * DEGREES,
                buff=0.2,
            ).shift(0.25 * UP)
            for func in [Line, Arrow]
        ]
        theories_line.set_stroke(BLUE_C, 6)
        theories_arrow.set_fill(BLUE_C)

        self.play(FadeIn(theories[0], LEFT))
        self.play(
            GrowFromPoint(theories[1], theories_line.get_start(), path_arc=-90 * DEGREES),
            ShowCreationThenFadeOut(theories_line, run_time=2),
            FadeIn(theories_arrow, rate_func=squish_rate_func(smooth, 0.3, 1), run_time=2)
        )
        self.wait()

        theories_group = VGroup(theories, theories_arrow)

        # j function
        j_func = OldTex(
            "j(\\tau)  =q^{-1}+744+196{,}884 q+21{,}493{,}760 q^{2}+864{,}299{,}970 q^{3}+\\cdots\\\\",
            "\\big(q = e^{2\\pi i \\tau}\\big)",
            tex_to_color_map={
                "\\tau": TEAL,
                "q": BLUE,
                "196{,}884": WHITE,
            }
        )
        j_func.scale(0.7)
        j_func[-5:].shift([-0.5, -0.25, 0])
        j_func.next_to(mckay, RIGHT, aligned_edge=DOWN)
        j_func.shift(0.5 * UP)

        special_num = j_func.get_part_by_tex("196{,}884")
        special_num_underline = Underline(special_num)
        special_num_underline.set_stroke(YELLOW, 3)

        self.play(
            theories_group.scale, 0.5, {"about_edge": UL},
            theories_group.to_edge, UP,
            Write(j_func)
        )
        self.wait()
        self.play(
            ShowCreation(special_num_underline),
            special_num.set_color, YELLOW,
        )
        self.wait()

        j_coloring = ImageMobject("J_Invariant_Coloring")
        j_coloring.set_width(FRAME_WIDTH)
        j_coloring.to_edge(DOWN, buff=0)
        j_coloring.set_opacity(0.25)
        self.add(j_coloring, *self.mobjects)
        self.play(FadeIn(j_coloring))
        self.wait(0.5)
        self.play(FadeOut(j_coloring), FadeOut(special_num_underline))
        self.wait()

        # Conway
        conway = get_named_image("John Conway")
        conway[0].flip()
        conway.move_to(mckay)
        conway.to_edge(RIGHT)
        moonshine = OldTexText("Moonshine!")
        moonshine.set_height(0.6)
        moonshine.next_to(conway, LEFT, MED_LARGE_BUFF, aligned_edge=UP)
        moonshine.set_color(YELLOW)

        self.play(
            FadeOut(timeline, DOWN),
            FadeOut(triangle, DOWN),
            j_func.to_edge, DOWN,
            FadeOut(theories_group),
            FadeIn(conway, DOWN),
        )
        self.play(Write(moonshine))
        self.wait()

        # Conjecture
        conjecture = OldTexText("Monstrous ", "moonshine\\\\", " conjecture")
        conjecture_icon = VGroup(
            get_monster().set_height(1),
            OldTex("\\leftrightarrow"),
            OldTex("j(\\tau)", tex_to_color_map={"\\tau": TEAL}),
        )
        conjecture_icon.arrange(RIGHT, buff=SMALL_BUFF)
        conjecture_icon.set_height(1.5)
        conjecture_icon.next_to(timeline.n2p(1979), UP, MED_LARGE_BUFF)
        conjecture.next_to(conjecture_icon, UP, MED_LARGE_BUFF)

        self.play(
            FadeIn(timeline, DOWN),
            FadeIn(triangle, DOWN),
            FadeOut(mckay, UP),
            Transform(
                moonshine,
                moonshine.copy().replace(conjecture[1], stretch=True).fade(1),
                remover=True,
            ),
            ReplacementTransform(
                conjecture[1].copy().replace(moonshine, stretch=True).fade(1),
                conjecture[1],
            ),
            Write(conjecture[0::2]),
        )
        self.play(
            FadeIn(conjecture_icon, lag_ratio=0.1),
            triangle.move_to, timeline.n2p(1979), DOWN,
        )
        self.play(blink_monster(conjecture_icon[0]))
        self.wait()

        conjecture_group = VGroup(conjecture, conjecture_icon)

        # Borcherds
        borcherds = get_named_image("Richard Borcherds")
        borcherds.next_to(timeline.n2p(1992), UP, MED_LARGE_BUFF)

        self.play(
            conjecture_group.scale, 0.5, {"about_edge": DOWN},
            triangle.move_to, timeline.n2p(1992), DOWN,
            FadeOut(conway, RIGHT),
            FadeIn(borcherds, 2 * LEFT)
        )
        self.wait(2)
        self.play(
            triangle.move_to, timeline.n2p(1998), DOWN,
            MaintainPositionRelativeTo(borcherds, triangle),
        )

        medal = ImageMobject("Fields Medal")
        medal.set_height(1)
        medal.move_to(borcherds.get_corner(UR), LEFT)
        self.play(FadeIn(medal, DOWN))
        self.wait()
