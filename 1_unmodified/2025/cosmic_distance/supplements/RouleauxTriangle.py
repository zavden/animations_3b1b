# ==============================================================================
# Scene:      RouleauxTriangle
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 540-587)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RouleauxTriangle.py RouleauxTriangle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RouleauxTriangle(InteractiveScene):
    def construct(self):
        # Add triangle
        arcs = VGroup(
            Arc(30 * DEG + x * 120 * DEG, 60 * DEG, radius=1)
            for x in range(3)
        )
        arcs[1].shift(arcs[0].get_end() - arcs[1].get_start())
        arcs[2].shift(arcs[0].get_start() - arcs[2].get_end())
        arcs.center()
        shape = VMobject()
        for arc in arcs:
            shape.append_vectorized_mobject(arc)

        shape.set_fill(BLUE_E, 1)
        shape.set_stroke(WHITE, 2)
        shape.set_height(3)
        shape.move_to(UP)

        shape.set_shading(0.25, 0.25, 0)

        self.add(shape)

        # Show the projection
        v_lines = DashedLine(3 * UP, 3 * DOWN).replicate(2)
        v_lines.arrange(RIGHT, buff=shape.get_width())
        v_lines.move_to(shape, UP)
        v_lines.set_stroke(GREY_C, 1)

        projection = shape.copy()
        projection.stretch(0, 1)
        projection.move_to(v_lines.get_bottom())

        self.play(
            *map(ShowCreation, v_lines),
            TransformFromCopy(shape, projection),
            run_time=2
        )
        self.wait()

        # Rotate
        shape_center = np.array([0, shape.get_y(), 0])
        shape.add_updater(lambda m: m.move_to(shape_center))
        self.play(
            Rotate(shape, PI, run_time=6),
            # self.frame.animate.set_gamma(PI),
            run_time=6
        )
