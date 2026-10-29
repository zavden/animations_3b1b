# ==============================================================================
# Scene:      TwoFlipsEqualsRotation
# Source:     videos/_2025/grover/state_vectors.py (lines 2863-2938)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoFlipsEqualsRotation.py TwoFlipsEqualsRotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoFlipsEqualsRotation(InteractiveScene):
    def construct(self):
        # Set up planes
        plane = NumberPlane((-2, 2), (-2, 2))
        plane.background_lines.set_stroke(BLUE, 1, 1)
        plane.faded_lines.set_stroke(BLUE, 1, 0.25)
        plane.axes.set_opacity(0.5)

        randy = Randolph(mode="pondering", height=3)

        ghost_plane = plane.copy()
        ghost_plane.fade(0.5)
        self.add(ghost_plane)

        plane2 = plane.copy()
        ghost_plane2 = ghost_plane.copy()
        randy2 = randy.copy()
        VGroup(plane2, ghost_plane2, randy2).next_to(plane, RIGHT, buff=3)

        self.add(plane, randy)

        # Show flips
        theta = 15 * DEG
        h_flip_line = DashedLine(plane.get_left(), plane.get_right())
        diag_flip_line = h_flip_line.copy().rotate(theta)
        flip_lines = VGroup(h_flip_line, diag_flip_line)
        flip_lines.set_stroke(WHITE, 4)

        for line in flip_lines:
            self.play(ShowCreation(line, run_time=0.5))
            self.play(
                randy.animate.flip(axis=line.get_vector(), about_point=plane.get_origin()),
                plane.animate.flip(axis=line.get_vector(), about_point=plane.get_origin()),
            )
        self.wait()

        # Show rotation
        arcs = VGroup(
            Arc(0, 90 * DEG, radius=1),
            Arc(180 * DEG, 90 * DEG, radius=1),
        )
        for arc, vect in zip(arcs, [UR, DL]):
            arc.set_stroke(WHITE, 5)
            arc.move_to(plane2.get_corner(vect))
            arc.add_tip()

        self.play(
            self.frame.animate.move_to(midpoint(plane.get_center(), plane2.get_center())),
            FadeIn(ghost_plane2),
            FadeIn(plane2),
            FadeIn(randy2),
        )
        self.play(
            Rotate(Group(plane2, Point(), randy2), 2 * theta, about_point=plane2.get_center()),
            *map(FadeIn, arcs)
        )
        self.wait()

        # Show angle
        arc = Arc(0, theta, radius=1.0)
        theta_label = Tex(R"\theta", font_size=30)
        theta_label.set_backstroke(BLACK, 3)
        theta_label.next_to(arc, RIGHT, SMALL_BUFF)
        theta_label.shift(0.025 * UP)

        rot_arc = Arc(0, 2 * theta, arc_center=plane2.get_center())
        two_theta_label = Tex(R"2 \theta")
        two_theta_label.set_backstroke(BLACK, 3)
        two_theta_label.next_to(rot_arc, RIGHT, SMALL_BUFF)

        self.play(ShowCreation(arc), Write(theta_label), run_time=1)
        self.play(
            TransformFromCopy(arc, rot_arc),
            TransformFromCopy(theta_label, two_theta_label),
        )
        self.wait()
