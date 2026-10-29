# ==============================================================================
# Scene:      CoordinateFree
# Source:     videos/_2017/highD.py (lines 3296-3321)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CoordinateFree.py CoordinateFree -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CoordinateFree(PiCreatureScene):
    def construct(self):
        plane = NumberPlane(x_radius = 2.5, y_radius = 2.5)
        plane.add_coordinates()
        plane.to_corner(UP+LEFT)
        self.add(plane)

        circles = VGroup(*[
            Circle(color = YELLOW).move_to(
                plane.coords_to_point(*coords)
            )
            for coords in it.product(*2*[[-1, 1]])
        ])
        inner_circle = Circle(
            radius = np.sqrt(2)-1,
            color = GREEN
        ).move_to(plane.coords_to_point(0, 0))

        self.add_foreground_mobjects(circles, inner_circle)

        self.play(PiCreatureSays(
            self.pi_creature, "Lose the \\\\ coordinates!",
            target_mode = "hooray"
        ))
        self.play(FadeOut(plane, run_time = 2))
        self.wait(3)
