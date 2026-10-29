# ==============================================================================
# Scene:      ShowSphereVolumeDerivative
# Source:     videos/_2026/spheres_talk/volumes.py (lines 807-863)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSphereVolumeDerivative.py ShowSphereVolumeDerivative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowCircleAreaDerivative(InteractiveScene):
    def construct(self):
        # Shrinking difference
        r = 2
        dr_tracker = ValueTracker(0.5)
        get_dr = dr_tracker.get_value

        circle = self.get_circle(r)
        dA_group = always_redraw(lambda: self.get_dA_group(r, get_dr()))

        self.add(circle)
        self.add(dA_group)

        # Shrink
        dr_tracker.set_value(0)
        self.play(dr_tracker.animate.set_value(0.5), run_time=2)
        self.wait()
        self.play(dr_tracker.animate.set_value(0.1), run_time=3)
        self.wait()

    def get_circle(self, r, fill_color=TEAL_E, fill_opacity=0.75, label="A"):
        result = VGroup()

        circle = Circle(radius=r)
        circle.set_fill(fill_color, fill_opacity)
        circle.set_stroke(WHITE, 0)
        result.add(circle)

        circle_label = Tex(label, font_size=72)
        circle_label.shift(0.5 * r * UP)
        result.add(circle_label)

        rad_line = Line(ORIGIN, r * RIGHT)
        rad_line.rotate(-45 * DEG, about_point=ORIGIN)
        r_label = Tex(R"r")
        r_label.next_to(rad_line.get_center(), UR, SMALL_BUFF)
        result.add(rad_line, r_label)

        return result

    def get_dA_group(self, r, dr, fill_color=RED_E, fill_opacity=0.5, label_color=WHITE):
        annulus = Annulus(r, r + dr)
        annulus.set_fill(fill_color, fill_opacity)
        annulus.set_stroke(width=0)
        line = Line(r * RIGHT, (r + dr) * RIGHT)
        dr_label = Tex(R"dr")
        dr_label.set_fill(label_color)
        dr_label.set_max_width(0.5 * line.get_width())
        dr_label.next_to(line, UP, buff=SMALL_BUFF)

        return VGroup(annulus, line, dr_label)


class ShowSphereVolumeDerivative(ShowCircleAreaDerivative):
    def construct(self):
        # Set up
        frame = self.frame
        self.set_floor_plane("xz")

        r = 3
        dr_tracker = ValueTracker(0)
        get_dr = dr_tracker.get_value

        circle = self.get_circle(r, label="V", fill_opacity=1)
        dV_group = always_redraw(lambda: self.get_dA_group(r, get_dr()))

        inner_sphere = Sphere(radius=r)
        inner_sphere.set_color(TEAL_E, 1)
        inner_sphere.set_clip_plane(IN, r)
        sphere_mesh = SurfaceMesh(inner_sphere, resolution=(51, 26))
        sphere_mesh.set_stroke(WHITE, 1, 0.2)
        sphere_mesh.rotate(90 * DEG, RIGHT)

        def get_outer_sphere():
            sphere = Sphere(radius=r + get_dr())
            sphere.set_color(RED_E, 0.5)
            sphere.set_clip_plane(IN, 0)
            sphere.set_sort_to_camera()
            return sphere

        outer_sphere = always_redraw(get_outer_sphere)

        self.add(circle)
        self.add(inner_sphere, sphere_mesh)

        frame.reorient(-75, -21, 0, ORIGIN, 8.73)
        self.play(
            frame.animate.reorient(42, -15, 0, ORIGIN, 8.73),
            inner_sphere.animate.set_clip_plane(IN, 0),
            run_time=3,
        )
        self.add(inner_sphere, circle, sphere_mesh)
        self.play(FadeIn(circle))
        self.wait()

        # Show dV
        self.add(outer_sphere)
        self.add(dV_group)
        sphere_mesh.add_updater(lambda m: m.set_width(2 * (r + get_dr())).move_to(ORIGIN))
        self.play(dr_tracker.animate.set_value(0.5), run_time=2)
        self.wait()
        self.play(dr_tracker.animate.set_value(0.1), run_time=3)
        self.wait()

        # Clean shrinking
        self.clear()
        self.add(outer_sphere, sphere_mesh, dV_group)
        dV_group.add_updater(lambda m: m[1:].set_opacity(0))
        dr_tracker.set_value(0.5)
        self.play(dr_tracker.animate.set_value(0.0), run_time=5)
