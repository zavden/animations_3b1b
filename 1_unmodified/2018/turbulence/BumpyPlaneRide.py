# ==============================================================================
# Scene:      BumpyPlaneRide
# Source:     videos/_2018/turbulence.py (lines 792-808)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BumpyPlaneRide.py BumpyPlaneRide -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BumpyPlaneRide(Scene):
    def construct(self):
        plane = SVGMobject(file_name="plane2")
        self.add(plane)

        total_time = 0
        while total_time < 10:
            point = 2 * np.append(np.random.random(2), 2) + DL
            point *= 0.2
            time = 0.2 * random.random()
            total_time += time
            arc = PI * random.random() - PI / 2
            self.play(
                plane.move_to, point,
                run_time=time,
                path_arc=arc
            )
