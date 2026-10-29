# ==============================================================================
# Scene:      StatisticalMechanicsIn3d
# Source:     videos/_2023/gauss_int/supplements.py (lines 896-931)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StatisticalMechanicsIn3d.py StatisticalMechanicsIn3d -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class StatisticalMechanicsIn3d(InteractiveScene):
    def construct(self):
        # Test
        n_balls = 200
        self.camera.light_source.move_to([0, -5, 5])
        frame = self.frame
        frame.reorient(20, 70)
        frame.set_height(2)
        frame.move_to([0.5, 0.5, 0.5])

        balls = DotCloud(np.random.random((n_balls, 3)))
        balls.set_radius(0.015)
        balls.make_3d()
        balls.set_shading(0.25, 0.5, 1)

        cube = VCube(side_length=1.0)
        cube.move_to(ORIGIN, [-1, -1, -1])
        cube.set_stroke(BLUE, 2)
        cube.set_fill(opacity=0)
        self.add(cube)

        velocities = np.random.normal(0, 3, (n_balls, 3))

        def update(balls, dt):
            points = balls.get_points()
            new_points = np.clip(points + 0.1 * velocities * dt, 0, 1)
            velocities[new_points <= 0] *= -1
            velocities[new_points >= 1] *= -1
            balls.set_points(new_points)

            return balls

        balls.add_updater(update)

        self.add(balls)
        self.play(frame.animate.reorient(-20), run_time=20)
