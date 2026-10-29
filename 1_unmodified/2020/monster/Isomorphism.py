# ==============================================================================
# Scene:      Isomorphism
# Source:     videos/_2020/monster.py (lines 2634-2772)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Isomorphism.py Isomorphism -w -m --fps 15
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


class Isomorphism(Scene):
    def construct(self):
        # Frame
        frame = self.camera.frame
        frame.focal_distance = 20

        # Rotation equation
        def get_rot_icon(angle=0, axis=OUT, frame=frame):
            cube = get_glassy_cube(frame)
            cube.set_height(1)
            arc_arrows = VGroup(*[
                Arrow(
                    u * RIGHT,
                    u * rotate_vector(RIGHT, 160 * DEGREES),
                    buff=0,
                    path_arc=160 * DEGREES,
                    width=0.05,
                )
                for u in [1, -1]
            ])
            arc_arrows.set_color(GREY_B)
            axis_line = DashedLine(IN, OUT)
            axis_line.set_stroke(YELLOW, 2)

            rot_icon = Group(arc_arrows, axis_line, cube)
            rot_icon.set_gloss(0.5)
            rot_icon.apply_depth_test()

            rot_icon.rotate(angle, axis)
            rot_icon.rotate(-15 * DEGREES, OUT)
            rot_icon.rotate(75 * DEGREES, LEFT)

            return rot_icon

        rot_icon_equation = Group(
            get_rot_icon(90 * DEGREES, UP),
            OldTex("\\times").scale(2),
            get_rot_icon(90 * DEGREES, RIGHT),
            OldTex("=").scale(2),
            get_rot_icon(0, OUT),
        )
        rot_icons = rot_icon_equation[0::2]
        rot_icon_equation.arrange(RIGHT, buff=LARGE_BUFF)
        rot_icon_equation.shift(1.5 * UP)

        icon_labels = VGroup(*[
            OldTexText(f"$180^\\circ$ about\\\\{axis} axis")
            for axis in "xyz"
        ])
        for icon, label in zip(rot_icon_equation[0::2], icon_labels):
            icon[-1][-1].set_opacity(0.5)
            label.scale(0.8)
            label.move_to(icon)
            label.to_edge(UP)
            icon.add(label)

        # Permutation equation
        dots = VGroup(*[Dot() for x in range(4)])
        dots.set_height(0.4)
        dots.set_color(GREY_B)
        dots.arrange(RIGHT)
        # for n, dot in enumerate(dots):
        #     label = Integer(n + 1)
        #     label.set_color(BLACK)
        #     label.set_height(0.6 * dot.get_height())
        #     label.move_to(dot)
        #     dot.add(label)

        perms = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [2, 3, 0, 1],
        ]
        perm_terms = VGroup()
        for perm in perms:
            perm_term = VGroup(dots.copy(), get_permutation_arrows(dots, perm))
            perm_term.perm = perm
            perm_terms.add(perm_term)
        perm_equation = VGroup(
            perm_terms[0],
            OldTex("\\times").scale(2),
            perm_terms[1],
            OldTex("=").scale(2),
            perm_terms[2],
        )
        perm_equation.arrange(RIGHT, buff=LARGE_BUFF)
        perm_equation.move_to(2 * DOWN)

        # Bijection lines
        bij_lines = VGroup()
        for m1, m2 in zip(rot_icons, perm_terms):
            line = Line(m1.get_bottom(), m2.get_top(), buff=0.2)
            line.set_angle(-PI / 2, about_point=line.get_center())
            bij_lines.add(line)

        bij_lines.set_color(GREEN)

        rot_icons[-1].match_x(bij_lines[2])

        # Add terms
        self.add(rot_icons)
        for rot_icon, line, perm_term in zip(rot_icons, bij_lines, perm_terms):
            self.play(
                # FadeIn(rot_icon),
                GrowFromPoint(line, line.get_top()),
                FadeIn(perm_term, 2 * UP),
            )
        self.wait()
        self.play(Write(VGroup(
            *rot_icon_equation[1::2],
            *perm_equation[1::2],
        )))
        self.wait(2)

        # Composition
        rot_anims = [
            AnimationGroup(
                Rotate(rot_icon[2], PI, axis=rot_icon[1].get_vector()),
                ShowCreationThenFadeAround(rot_icon[-1]),
            )
            for rot_icon in rot_icons
        ]
        perm_anims = [
            permutation_animation(perm_term[0], perm_term.perm, lag_factor=0.1)
            for perm_term in perm_terms
        ]

        self.play(rot_anims[1])
        self.play(rot_anims[0])
        self.wait()
        self.play(rot_anims[2])
        self.wait()
        self.play(LaggedStartMap(ShowCreation, bij_lines, lag_ratio=0.5))
        self.wait()
        self.play(perm_anims[1])
        self.play(perm_anims[0])
        self.wait()
        self.play(perm_anims[2])
        self.wait()
