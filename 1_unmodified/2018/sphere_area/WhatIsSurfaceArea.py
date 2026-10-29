# ==============================================================================
# Scene:      WhatIsSurfaceArea
# Source:     videos/_2018/sphere_area.py (lines 2321-2381)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsSurfaceArea.py WhatIsSurfaceArea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIsSurfaceArea(SpecialThreeDScene):
    CONFIG = {
        "change_power": True,
    }

    def construct(self):
        title = OldTexText("What is surface area?")
        title.scale(1.5)
        title.to_edge(UP)
        title.shift(0.035 * RIGHT)
        self.add_fixed_in_frame_mobjects(title)

        power_tracker = ValueTracker(1)
        surface = always_redraw(
            lambda: self.get_surface(
                radius=3,
                amplitude=1,
                power=power_tracker.get_value()
            )
        )

        pieces = surface.copy()
        pieces.clear_updaters()
        random.shuffle(pieces.submobjects)

        self.set_camera_to_default_position()
        self.begin_ambient_camera_rotation()
        # self.add(self.get_axes())
        self.play(LaggedStartMap(
            DrawBorderThenFill, pieces,
            lag_ratio=0.2,
        ))
        self.remove(pieces)
        self.add(surface)
        if self.change_power:
            self.play(
                power_tracker.set_value, 5,
                run_time=2
            )
            self.play(
                power_tracker.set_value, 1,
                run_time=2
            )
        self.wait(2)

    def get_surface(self, radius, amplitude, power):
        def alt_pow(x, y):
            return np.sign(x) * (np.abs(x) ** y)
        return ParametricSurface(
            lambda u, v: radius * np.array([
                v * np.cos(TAU * u),
                v * np.sin(TAU * u),
                0,
            ]) + amplitude * np.array([
                0,
                0,
                (v**2) * alt_pow(np.sin(5 * TAU * u), power),
            ]),
            resolution=(100, 20),
            v_min=0.01
        )
