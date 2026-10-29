# ==============================================================================
# Scene:      ZooOfGroups
# Source:     videos/_2020/monster.py (lines 746-853)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ZooOfGroups.py ZooOfGroups -w -m --fps 15
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


def get_snowflake(height=2):
    snowflake = SVGMobject("snowflake")
    snowflake.set_fill(GREY_C, 1)
    snowflake.set_gloss(1)
    snowflake.set_shadow(0.2)
    snowflake.set_stroke(WHITE, 1)
    snowflake.set_height(height)
    return snowflake


def get_cube(color=BLUE_D, opacity=1, height=2, frame=None):
    poor_cube = Cube()
    cube = Cube(square_resolution=(10, 10))
    cube.set_color(color, opacity)
    cube.center()

    for face, p_face in zip(cube, poor_cube):
        face.add(*[
            Line3D(p_face.get_points()[i], p_face.get_points()[j], width=0.02, color=GREY_B)
            for i, j in [(0, 1), (1, 3), (3, 2), (2, 0)]
        ])

    cube.set_height(height)
    return cube


class ZooOfGroups(ThreeDScene):
    def construct(self):
        self.camera.light_source.move_to([-10, 5, 20])

        dot_pair = VGroup(Dot(), Dot())
        dot_pair.set_height(0.5)
        dot_pair.arrange(RIGHT, buff=LARGE_BUFF)
        dot_pair.set_color(GREY_B)

        snowflake = get_snowflake(height=2)

        k4_axes = Group(
            Line3D(LEFT, RIGHT, color=RED),
            Line3D(DOWN, UP, color=GREEN),
            Line3D(IN, OUT, color=BLUE),
        )
        k4_axes.set_height(3)

        quat_group = OldTex("\\{1, -1, i , -i\\\\j, -j, k, -k\\}")

        cube = get_cube(color=BLUE_D, opacity=1)
        cube.rotate(15 * DEGREES, OUT)
        cube.rotate(80 * DEGREES, LEFT)

        sphere = Sphere()
        sphere = Group(
            sphere,
            SurfaceMesh(sphere, resolution=(21, 11))
        )
        sphere[1].set_stroke(WHITE, 0.5, 0.5)
        sphere.rotate(90 * DEGREES, LEFT)
        sphere.rotate(0.2 * DEGREES, RIGHT)
        sphere[0].set_sort_to_camera()
        sphere.rotate(90 * DEGREES, UP)
        sphere.set_height(3)

        circle = Circle()
        circle.set_height(3)

        monster_object = OldTex("196{,}", "883")
        monster_object.arrange(DOWN, buff=0, aligned_edge=LEFT)
        monster_object.set_height(1.5)
        monster_object.add(Eyes(monster_object))
        monster_object[-1].scale(0.8, about_edge=DR)

        qubit = OldTex(
            "\\alpha|0\\rangle + \\beta|1\\rangle",
            tex_to_color_map={"\\alpha": BLUE, "\\beta": YELLOW}
        )
        qubit.set_height(1)
        qubit.set_height(1)

        groups = Group(
            Group(OldTex("C_2"), dot_pair),
            Group(OldTex("D_6"), snowflake),
            Group(OldTex("K_4"), k4_axes),
            Group(OldTex("Q_8"), quat_group),
            Group(OldTex("S_4"), cube),
            Group(OldTex("SO(3)"), sphere),
            Group(OldTex("\\mathds{R}^+ / \\mathds{Z}"), circle),
            Group(OldTex("SU(2)"), qubit),
            Group(get_monster(), monster_object),
        )

        for group in groups:
            group[0].set_height(1)
            group.arrange(RIGHT, buff=LARGE_BUFF)

        groups[-1][0].scale(2)

        groups.arrange_in_grid(3, 3)
        groups.set_width(FRAME_WIDTH - 1)
        groups[:3].shift(0.5 * UP)
        groups[-3:].shift(0.5 * DOWN)

        self.play(LaggedStart(*[
            FadeIn(group[0], -0.5 * group.get_center())
            for group in groups
        ]))
        self.play(LaggedStart(*[
            FadeInFromLarge(group[1])
            for group in groups
        ]))
        self.play(LaggedStart(
            Rotate(dot_pair, PI),
            Blink(monster_object[-1]),
            Rotate(cube, PI / 2, axis=cube[0].get_center() - cube[-1].get_center()),
            Rotate(snowflake, 120 * DEGREES),
            Rotate(k4_axes, PI, axis=RIGHT),
            Rotate(sphere, 170 * DEGREES, axis=UP),
            run_time=3,
            lag_ratio=0.1,
        ))
        self.wait()

        self.play(
            groups[-1].scale, 3,
            groups[-1].center,
            groups[-1].space_out_submobjects, 1.5,
            *[
                FadeOut(mob, mob.get_center() - groups[-1].get_center())
                for mob in groups[:-1]
            ]
        )
        self.play(monster_object[-1].look_at, groups[-1][0])
        self.play(Blink(monster_object[-1]))
        self.play(blink_monster(groups[-1][0]))
        self.wait()
