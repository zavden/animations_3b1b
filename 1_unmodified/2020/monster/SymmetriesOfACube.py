# ==============================================================================
# Scene:      SymmetriesOfACube
# Source:     videos/_2020/monster.py (lines 856-1029)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SymmetriesOfACube.py SymmetriesOfACube -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class SymmetriesOfACube(ThreeDScene):
    def construct(self):
        # Setup
        frame = self.camera.frame
        light = self.camera.light_source
        light.move_to(5 * LEFT + 20 * DOWN + 10 * OUT)

        plane = NumberPlane(x_range=(-10, 10), y_range=(-10, 10))
        plane.shift(IN)

        cube = get_cube(color=BLUE_D, opacity=1)
        cube.set_gloss(0.5)
        cube.set_shadow(0.2)

        frame.set_euler_angles(
            phi=70 * DEGREES,
            theta=-30 * DEGREES,
        )
        frame.add_updater(lambda m, dt, sc=self: m.set_theta(-30 * DEGREES * np.cos(sc.time * 0.05)))
        self.add(frame)

        self.add(plane)
        self.add(cube)

        # Ask about structure
        question = OldTexText("What structure is being preserved?")
        question.set_height(0.7)
        question.to_edge(UP)
        question.fix_in_frame()

        def get_rotation(deg, axis, cube=cube):
            return Rotate(cube, deg * DEGREES, axis=axis, run_time=1.5)

        pairs = [
            (90, UP),
            (90, RIGHT),
            (90, OUT),
            (120, [1, 1, 1]),
            (120, [1, -1, 1]),
            (180, UP),
        ]
        for deg, axis in pairs:
            self.play(get_rotation(deg, axis))
            if axis is pairs[1][1]:
                self.play(FadeIn(question, DOWN))
            self.wait()

        # Count cube symmetries
        count_label = OldTexText("24 ", "symmetries")
        count_label.set_color_by_tex("24", YELLOW)
        count_label.set_height(0.7)
        count_label.fix_in_frame()
        count_label.to_edge(UP)

        self.play(
            FadeIn(count_label, DOWN),
            FadeOut(question, UP),
        )
        self.play(get_rotation(120, [1, -1, -1]))
        self.wait()
        self.play(get_rotation(90, LEFT))
        self.wait()
        self.play(get_rotation(120, [1, -1, -1]))
        self.wait()
        self.play(get_rotation(180, OUT))
        self.wait()

        # Bigger group
        reflection_plane = Square3D(resolution=(10, 10))
        reflection_plane.set_width(4)
        reflection_plane.move_to(cube)
        reflection_plane.set_color(GREY, opacity=0.75)
        reflection_plane.rotate(PI / 2, DOWN)

        cross24 = Cross(count_label[0])
        cross24.fix_in_frame()
        label48 = OldTex("48")
        label48.set_color(GREEN)
        label48.match_height(count_label[0])
        label48.move_to(count_label[0], DOWN)
        label48.fix_in_frame()

        self.play(FadeInFromLarge(reflection_plane))
        self.play(
            ShowCreation(cross24),
            ApplyMethod(cube.stretch, -1, 0),
        )
        self.wait()
        self.play(
            Rotate(reflection_plane, PI / 2, axis=UP)
        )
        self.play(
            ApplyMethod(cube.stretch, -1, 2),
        )
        self.wait()
        self.play(Rotate(reflection_plane, PI / 4, UP))
        self.play(
            cube.stretch, -1, 2,
            cube.rotate, PI / 2, UP,
        )
        self.wait()
        self.add(count_label[0], cross24)
        self.play(
            count_label[0].shift, 2 * LEFT,
            cross24.shift, 2 * LEFT,
            FadeIn(label48, UP),
        )
        self.play(
            reflection_plane.rotate, PI / 4, UP,
            reflection_plane.rotate, PI / 2, OUT,
        )
        self.play(
            cube.stretch, -1, 1,
        )
        self.wait()
        self.play(FadeOut(reflection_plane))
        self.wait()

        # Permute faces
        cross48 = Cross(label48)
        cross48.fix_in_frame()
        self.play(ShowCreation(cross48))
        label48.add(cross48)

        label24 = count_label[0]
        label24.add(cross24)
        count_label.remove(label24)

        def explostion_transform(self=self, cube=cube):
            cube_copy = cube.copy()
            self.play(
                cube.space_out_submobjects, 1.5,
                cube.shift, 0.5 * OUT,
            )
            exploded_cube_copy = cube.copy()
            self.play(LaggedStart(*[
                Rotate(
                    face,
                    axis=face.get_center() - cube.get_center(),
                    angle=random.choice([0, PI / 2, -PI / 2, PI])
                )
                for face in cube
            ]))
            perm = list(range(6))
            random.shuffle(perm)
            globals()['perm'] = perm  # TODO
            self.play(LaggedStart(*[
                Transform(face, cube[perm[i]])
                for i, face in enumerate(cube)
            ], lag_ratio=0.1))
            cube.become(exploded_cube_copy)
            self.play(Transform(cube, cube_copy))
            self.wait()

        for x in range(3):
            explostion_transform()

        # Largest size
        count = Integer(188743680)
        count.fix_in_frame()
        old_counts = VGroup(label24, label48)
        old_counts.generate_target()
        old_counts.target.to_edge(LEFT)
        count.match_height(old_counts)
        count.next_to(old_counts.target, RIGHT, buff=LARGE_BUFF)
        count.set_color(BLUE_B)
        self.play(
            MoveToTarget(old_counts),
            FadeIn(count),
            count_label.next_to, count, RIGHT,
        )
        for x in range(3):
            explostion_transform()
        self.wait(2)
