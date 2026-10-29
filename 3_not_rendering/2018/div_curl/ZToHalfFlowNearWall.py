# ==============================================================================
# Scene:      ZToHalfFlowNearWall
# Source:     videos/_2018/div_curl.py (lines 4002-4070)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl ZToHalfFlowNearWall.py ZToHalfFlowNearWall -w -m --fps 15
#
# Why it does not render:
#   Broken in the original: construct references an undefined name `planes` (NameError in Cairo too; the same undefined `planes` is in ComplexTransformationScene.paint_plane), and the scene depends on the unported ComplexTransformationScene helper; the intended horizontal-line selection cannot be recovered without guessing.
# ==============================================================================

from manim_imports_ext import *

def derivative(func, dt=1e-7):
    return lambda z: (func(z + dt) - func(z)) / dt


class ZToHalfFlowNearWall(ComplexTransformationScene, MovingCameraScene):
    CONFIG = {
        "num_anchors_to_add_per_line": 200,
        "plane_config": {"y_radius": 8}
    }

    def setup(self):
        MovingCameraScene.setup(self)
        ComplexTransformationScene.setup(self)

    def construct(self):
        # self.camera.frame.shift(2 * UP)
        self.camera.frame.scale(0.5, about_point=ORIGIN)

        plane = NumberPlane(
            x_radius=15,
            y_radius=25,
            y_unit_size=0.5,
            secondary_line_ratio=0,
        )
        plane.next_to(ORIGIN, UP, buff=0.001)
        horizontal_lines = VGroup(*[l for l in list(planes) + [plane.axes[0]] if np.abs(l.get_center()[0]) < 0.1])
        plane.set_stroke(MAROON_B, width=2)
        horizontal_lines.set_stroke(BLUE, width=2)

        self.prepare_for_transformation(plane)
        self.add_transformable_mobjects(plane)

        self.background.set_stroke(width=2)
        for label in self.background.coordinate_labels:
            label.set_stroke(width=0)
            label.scale(0.75, about_edge=UR)

        words = OldTexText("(Idealized) Flow \\\\", "near a wall")
        words.scale(0.75)
        words.add_background_rectangle_to_submobjects()
        words.next_to(0.75 * UP, LEFT, MED_LARGE_BUFF)
        equation = OldTex("z \\rightarrow z^{1/2}")
        equation.scale(0.75)
        equation.add_background_rectangle()
        equation.next_to(words, UP)

        self.apply_complex_function(
            lambda x: x**(1. / 2),
            added_anims=[Write(equation)]
        )
        self.play(Write(words, run_time=1))

        def func(point):
            z = R3_to_complex(point)
            d_half = derivative(lambda z: z**2)
            return complex_to_R3(d_half(z).conjugate())

        stream_lines = StreamLines(
            func,
            start_points_generator_config={
                "x_min": 0.01,
                "y_min": 0.01,
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            virtual_time=3,
            stroke_width=2,
            max_magnitude=10,
        )
        stream_line_animation = AnimatedStreamLines(stream_lines)

        self.add(stream_line_animation)
        self.wait(7)
