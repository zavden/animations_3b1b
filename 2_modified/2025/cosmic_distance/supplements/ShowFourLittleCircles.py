# ==============================================================================
# Scene:      ShowFourLittleCircles
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 828-854)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowFourLittleCircles.py ShowFourLittleCircles -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - LunarEclipseComposite.jpg is looked up next to this file (before: Grant's video output folder) and is a placeholder composite.
#
# Placeholder assets (not Grant's originals):
#   - LunarEclipseComposite.jpg (placeholder lunar eclipse composite: Earth's shadow and five moons placed where the scene draws the circles)
# ==============================================================================

from manim_imports_ext import *

class ShowFourLittleCircles(InteractiveScene):
    def construct(self):
        # Add image
        # CHANGE: the image lived next to Grant's video output; now there is a placeholder composite next to this file.
        image_path = Path(__file__).parent / "LunarEclipseComposite.jpg"
        image = ImageMobject(str(image_path))
        image.set_height(FRAME_HEIGHT)
        self.add(image)

        # Circles
        lil_circle = Circle(radius=0.62)
        lil_circle.move_to([-1.00, -0.167, 0.])
        lil_circle.set_stroke(YELLOW, 2)
        lil_circle.set_anti_alias_width(10)

        four_circles = lil_circle.get_grid(4, 1, buff=0)
        four_circles.rotate(8 * DEG)
        four_circles.move_to([1.503, -0.043, 0.])

        self.play(ShowCreation(lil_circle))
        self.wait()
        self.play(LaggedStart(
            (TransformFromCopy(lil_circle, circ)
            for circ in four_circles),
            lag_ratio=0.25,
            run_time=3
        ))
        self.wait()
