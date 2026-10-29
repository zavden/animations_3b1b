# ==============================================================================
# Scene:      RotationIn3dPlane
# Source:     videos/_2021/matrix_exp.py (lines 4977-5046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationIn3dPlane.py RotationIn3dPlane -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RotationIn3dPlane(Scene):
    def construct(self):
        # Axes and frame
        axes = ThreeDAxes()
        axes.set_stroke(width=2)
        axes.set_flat_stroke(False)

        frame = self.camera.frame
        frame.set_height(2.0 * FRAME_HEIGHT)
        frame.reorient(-40, 70)
        frame.add_updater(lambda f, dt: f.increment_theta(0.03 * dt))

        self.add(axes, frame)

        # Plane
        plane = Surface()
        plane.replace(VGroup(axes.x_axis, axes.y_axis), stretch=True)
        plane.set_color(GREY_C, opacity=0.75)
        plane.set_gloss(1)
        grid = NumberPlane((-6, 6), (-5, 5), faded_line_ratio=0)

        radius = 3
        p_vect = Vector(radius * RIGHT, fill_color=BLUE)
        v_vect = p_vect.copy()
        arc = Arc(0, PI / 2, radius=radius / 4)
        circle = Circle(radius=radius)
        circle.set_stroke(WHITE, 2)
        randy = Randolph(mode="pondering")
        randy.set_gloss(0.7)
        rot_group = Group(plane, grid, p_vect, v_vect, arc, circle, randy)

        normal = OUT
        for angle, axis in [(30 * DEGREES, RIGHT), (20 * DEGREES, UP)]:
            rot_group.rotate(angle, axis)
            normal = rotate_vector(normal, angle, axis)

        self.play(
            ShowCreation(plane),
            FadeIn(randy),
        )
        self.play(GrowArrow(p_vect))
        self.wait(2)
        self.play(
            Rotate(v_vect, PI / 2, axis=normal, about_point=axes.get_origin()),
            Rotate(randy, PI / 2, axis=normal, about_point=axes.get_origin()),
            UpdateFromAlphaFunc(v_vect, lambda m, a: m.set_fill(interpolate_color(BLUE, RED, a))),
            ShowCreation(arc),
            run_time=2,
        )
        self.wait(3)
        self.play(
            v_vect.animate.shift(p_vect.get_end() - v_vect.get_start()),
            FadeOut(arc),
            FadeOut(randy),
        )
        rot_group = VGroup(grid, p_vect, v_vect)
        rot_group.set_stroke(background=True)
        self.add(circle, rot_group)
        self.play(
            FadeIn(circle),
            Rotate(
                rot_group,
                2 * TAU,
                axis=normal,
                about_point=axes.get_origin(),
                run_time=4 * TAU,
                rate_func=linear,
            ),
            VFadeIn(grid),
        )
