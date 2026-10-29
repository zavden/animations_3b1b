# ==============================================================================
# Scene:      AskAboutCubeDiagonals
# Source:     videos/_2020/monster.py (lines 2784-2841)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutCubeDiagonals.py AskAboutCubeDiagonals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_glassy_cube(frame):
    verts = np.array(list(it.product(*3 * [[-1, 1]])))
    edges = [
        (v1, v2)
        for v1, v2 in it.combinations(verts, 2)
        if sum(v1 == v2) == 2
    ]
    corner_dots = Group(*[
        Sphere(resolution=(51, 26),).set_height(0.25).move_to(vert)
        for vert in verts
    ])
    corner_dots.set_color(GREY_B)
    edge_rods = Group(*[
        Line3D(v1, v2)
        for v1, v2 in edges
    ])

    faces = Cube(square_resolution=(10, 10))
    faces.set_height(2)
    faces.set_color(BLUE_E, 0.3)
    faces.add_updater(lambda m, f=frame: m.sort(lambda p: np.dot(p, [np.sign(f.euler_angles[0]) * 0.2, -1, 0.2])))

    cube = Group(corner_dots, edge_rods, faces)
    cube.corner_dots = corner_dots
    cube.edge_rods = edge_rods
    cube.faces = faces
    return cube


def get_permutation_arrows(mobs, permutation, arc=PI / 2):
    arrows = VGroup()
    for i in range(len(permutation)):
        j = permutation[i]
        u = -1 if mobs[i].get_x() < mobs[j].get_x() else 1
        arrow = Arrow(
            mobs[i].get_edge_center(u * UP),
            mobs[j].get_edge_center(u * UP),
            buff=SMALL_BUFF,
            path_arc=arc,
        )
        arrow.insert_n_curves(10)
        arrow.set_stroke(BLACK, 2, background=True)
        arrow.set_fill(BLUE, 0.8)
        arrows.add(arrow)
    return arrows


def permutation_animation(mobs, perm=None, arc=PI / 2, lag_factor=3, run_time=None):
    if perm is None:
        targets = list(mobs)
        random.shuffle(targets)
    else:
        targets = [mobs[i] for i in perm]

    kw = {"lag_ratio": lag_factor / len(mobs)}
    if run_time is not None:
        kw["run_time"] = run_time
    return LaggedStart(
        *[
            ApplyMethod(m1.move_to, m2, path_arc=arc)
            for m1, m2 in zip(mobs, targets)
        ],
        **kw
    )


class CubeRotations(ThreeDScene):
    def construct(self):
        # Set frame motion
        frame = self.camera.frame
        frame.set_euler_angles(phi=80 * DEGREES)
        frame.add_updater(lambda m, sc=self: m.set_euler_angles(theta=-20 * DEGREES * np.cos(0.1 * sc.time)))
        self.add(frame)

        # Setup cube
        cube = get_glassy_cube(frame)
        cube.set_height(3)
        axes = ThreeDAxes(axis_config={"include_tip": False})
        axes.apply_depth_test()

        self.add(axes)
        self.add(cube)

        # Apply rotations
        quats = self.get_quaternions()
        self.wait()
        for quat in quats:
            angle, axis = angle_axis_from_quaternion(quat)

            line = Line3D(-5 * axis, 5 * axis, prefered_creation_axis=0)
            line.set_color(YELLOW)
            if angle < 1e-6:
                line.scale(0)
            # line.apply_depth_test()
            deg_label = Integer(int(np.round(angle / DEGREES)), unit="^\\circ")
            deg_label.scale(2)
            deg_label.to_edge(UP)
            deg_label.shift(2 * LEFT)
            deg_label.fix_in_frame()

            self.add(line, *self.mobjects)
            self.play(ShowCreation(line), FadeIn(deg_label))
            self.play(Rotate(cube, angle, axis=axis))
            line.scale(-1)
            self.play(Uncreate(line), FadeOut(deg_label))

    def get_quaternions(self, n_rotations=30):
        ijk = [
            quaternion_from_angle_axis(90 * DEGREES, axis)
            for axis in [RIGHT, UP, OUT]
        ]
        result = []
        for x in range(n_rotations):
            n = random.randint(1, 10)
            curr = quaternion_from_angle_axis(0, RIGHT)
            for y in range(n):
                curr = quaternion_mult(curr, random.choice(ijk))
            result.append(curr)

        # Add on those rotations around diagonals for the end
        for oi in [OUT, IN]:
            for vect in [UL, UR, DR, DL]:
                result.append(quaternion_from_angle_axis(120 * DEGREES, vect + oi))
        return result


class QuadrupletShufflings(CubeRotations):
    def construct(self):
        # Background
        bg_rect = FullScreenFadeRectangle()
        bg_rect.set_fill(GREY_E, 1)
        bg_rect.set_stroke(width=0)
        self.add(bg_rect)

        # Setup dots
        dots = VGroup(*[Dot() for x in range(4)])
        dots.set_height(0.5)
        dots.arrange(RIGHT, buff=MED_LARGE_BUFF)
        dots.set_color(GREY_B)

        for n, dot in enumerate(dots):
            label = Integer(n + 1)
            label.set_height(0.25)
            label.set_color(BLACK)
            label.move_to(dot)
            dot.add(label)

        self.add(dots)
        self.wait()

        # Permutations
        for quat in self.get_quaternions():
            perm = self.quaternion_to_perm(quat)

            arrows = get_permutation_arrows(dots, perm)
            self.play(FadeIn(arrows))
            self.play(permutation_animation(dots, perm, lag_factor=0.2, run_time=1))
            self.play(FadeOut(arrows))

    def quaternion_to_perm(self, quat):
        angle, axis = angle_axis_from_quaternion(quat)

        base_vects = [UL, UR, DR, DL]
        rot_vects = [
            rotate_vector(v + OUT, angle, axis)
            for v in base_vects
        ]
        perm = []
        for vect in rot_vects:
            if vect[2] < 0:
                vect *= -1
            vect[2] = 0
            i = np.argmin([get_norm(vect - bv) for bv in base_vects])
            perm.append(i)
        return perm


class AskAboutCubeDiagonals(QuadrupletShufflings):
    def construct(self):
        # Setup
        frame = self.camera.frame
        frame.set_euler_angles(phi=80 * DEGREES)
        frame.add_updater(lambda m, sc=self: m.set_euler_angles(theta=-20 * DEGREES * np.cos(0.1 * sc.time)))

        cube = get_glassy_cube(frame)
        cube.set_height(3)
        axes = ThreeDAxes(axis_config={"include_tip": False})

        colors = [RED, GREEN, BLUE, YELLOW]
        diagonals = Group(*[
            Line3D(vect + OUT, -vect - OUT, color=color)
            for color, vect in zip(colors, [UL, UR, DR, DL])
        ])
        diagonals.match_height(cube.edge_rods)

        diag_markers = Group(*[
            Line3D(ORIGIN, UP, color=color)
            for color in colors
        ])
        diag_markers.arrange(RIGHT, buff=MED_LARGE_BUFF)
        diag_markers.to_corner(UL, buff=LARGE_BUFF)
        diag_markers.fix_in_frame()

        # Color corners
        cds = cube.corner_dots
        for diag in diagonals:
            globals()['diag'] = diag
            Group(*[
                cds[np.argmin([get_norm(cd.get_center() - diag.get_points()[i]) for cd in cds])]
                for i in [0, -1]
            ]).match_color(diag)

        cube.add_to_back(diagonals)

        # Rotations
        self.add(axes, cube)
        self.add(diag_markers)
        self.add(frame)
        for quat in self.get_quaternions():
            angle, axis = angle_axis_from_quaternion(quat)
            perm = self.quaternion_to_perm(quat)
            perm_arrows = get_permutation_arrows(diag_markers, perm)
            perm_arrows.fix_in_frame()

            self.play(FadeIn(perm_arrows))
            self.play(
                Rotate(cube, angle, axis=axis),
                permutation_animation(diag_markers, perm, lag_factor=0.1),
                run_time=2,
            )
            self.play(FadeOut(perm_arrows))
            self.wait()

            inv_perm = self.quaternion_to_perm(quaternion_conjugate(quat))
            diag_markers.set_submobjects([diag_markers[i] for i in inv_perm])
