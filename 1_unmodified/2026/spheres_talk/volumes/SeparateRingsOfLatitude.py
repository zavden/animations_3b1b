# ==============================================================================
# Scene:      SeparateRingsOfLatitude
# Source:     videos/_2026/spheres_talk/volumes.py (lines 954-994)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeparateRingsOfLatitude.py SeparateRingsOfLatitude -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SeparateRingsOfLatitude(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        sphere = Sphere(radius=1)
        sphere.set_color(BLUE_E)
        sphere.always_sort_to_camera(self.camera)

        n_rings = 50
        rings = VGroup(
            Circle(radius=math.sqrt(1 - z**2)).move_to(z * OUT)
            for z in np.linspace(-1, 1, n_rings)
        )
        rings.set_stroke(BLUE, 2, 0.5)

        frame.reorient(4, 78, 0, (-0.03, 0.01, 0.03), 2.88)
        self.add(sphere)
        self.play(
            sphere.animate.set_opacity(0.2),
            LaggedStartMap(FadeIn, rings),
            run_time=3
        )
        self.wait()
        self.play(
            rings[n_rings // 2].animate.set_stroke(YELLOW, 3, 1),
            rings[:n_rings // 2].animate.set_stroke(opacity=0.25),
            rings[n_rings // 2 + 1:].animate.set_stroke(opacity=0.25),
        )
        self.wait()

        # Move up and down
        z_tracker = ValueTracker(0)
        get_z = z_tracker.get_value
        equator = rings[n_rings // 2]
        equator.add_updater(
            lambda m: m.set_width(2 * math.sqrt(1 - get_z()**2)).move_to(get_z() * OUT)
        )

        self.play(z_tracker.animate.set_value(0.5), run_time=4)
        self.play(z_tracker.animate.set_value(-0.5), run_time=6)
        self.play(z_tracker.animate.set_value(0), run_time=4)
