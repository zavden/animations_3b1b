# ==============================================================================
# Scene:      IntroduceFelix
# Source:     videos/_2018/quaternions.py (lines 2962-3059)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceFelix.py IntroduceFelix -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Felix(PiCreature):
    CONFIG = {
        "color": GREEN_D
    }


class IntroduceFelix(PiCreatureScene, SpecialThreeDScene):
    def setup(self):
        PiCreatureScene.setup(self)
        SpecialThreeDScene.setup(self)

    def construct(self):
        self.introduce_felix()
        self.add_plane()
        self.show_in_three_d()

    def introduce_felix(self):
        felix = self.felix = self.pi_creature

        arrow = Vector(DL, color=WHITE)
        arrow.next_to(felix, UR)

        label = OldTexText("Felix the Flatlander")
        label.next_to(arrow.get_start(), UP)

        self.add(felix)
        self.play(
            felix.change, "wave_1", label,
            Write(label),
            GrowArrow(arrow),
        )
        self.play(Blink(felix))
        self.play(felix.change, "thinking", label)

        self.to_fade = VGroup(label, arrow)

    def add_plane(self):
        plane = NumberPlane(y_radius=10)
        axes = self.get_axes()
        to_fade = self.to_fade
        felix = self.felix

        self.add(axes, plane, felix)
        self.play(
            ShowCreation(axes),
            ShowCreation(plane),
            FadeOut(to_fade),
        )
        self.wait()

        self.plane = plane
        self.axes = axes

    def show_in_three_d(self):
        felix = self.pi_creature
        plane = self.plane
        axes = self.axes

        # back_plane = Rectangle().replace(plane, stretch=True)
        # back_plane.shade_in_3d = True
        # back_plane.set_fill(GREY_B, opacity=0.5)
        # back_plane.set_sheen(1, UL)
        # back_plane.shift(SMALL_BUFF * IN)
        # back_plane.set_stroke(width=0)
        # back_plane = ParametricSurface(
        #     lambda u, v: u * RIGHT + v * UP
        # )
        # back_plane.replace(plane, stretch=True)
        # back_plane.set_stroke(width=0)
        # back_plane.set_fill(GREY_B, opacity=0.5)

        sphere = self.get_sphere()
        # sphere.set_fill(BLUE_E, 0.5)

        self.move_camera(
            phi=70 * DEGREES,
            theta=-110 * DEGREES,
            added_anims=[FadeOut(plane)],
            run_time=2
        )
        self.begin_ambient_camera_rotation()
        self.add(axes, sphere)
        self.play(
            Write(sphere),
            felix.change, "confused"
        )
        self.wait()

        axis_angle_pairs = [
            (RIGHT, 90 * DEGREES),
            (OUT, 45 * DEGREES),
            (UR + OUT, 120 * DEGREES),
            (RIGHT, 90 * DEGREES),
        ]
        for axis, angle in axis_angle_pairs:
            self.play(Rotate(
                sphere, angle=angle, axis=axis,
                run_time=2,
            ))
        self.wait(2)

    #
    def create_pi_creature(self):
        return Felix().move_to(4 * LEFT + 2 * DOWN)
